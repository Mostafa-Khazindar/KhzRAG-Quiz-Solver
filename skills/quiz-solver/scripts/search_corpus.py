# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pymupdf",
#     "bm25s",
# ]
# ///

import os
import fitz  # PyMuPDF
import bm25s
import argparse
import pickle
import time

def ensure_scratch_dir(base_dir):
    scratch_dir = os.path.join(base_dir, ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    return scratch_dir

def extract_pages(pdf_path, center_page_num, output_path):
    try:
        doc = fitz.open(pdf_path)
        new_doc = fitz.open()
        start = max(0, center_page_num - 1)
        end = min(len(doc) - 1, center_page_num + 1)
        new_doc.insert_pdf(doc, from_page=start, to_page=end)
        new_doc.save(output_path)
        new_doc.close()
        doc.close()
        return True
    except Exception as e:
        print(f"Error extracting pages: {e}")
        return False

def get_corpus_manifest(corpus_dir):
    """Returns a dictionary of all files and their last modified timestamps."""
    manifest = {}
    for root, _, files in os.walk(corpus_dir):
        if ".scratch" in root:
            continue
        for file in files:
            ext = file.lower().split('.')[-1]
            if ext in ["pdf", "md", "txt", "csv"]:
                file_path = os.path.join(root, file)
                manifest[file_path] = os.path.getmtime(file_path)
    return manifest

def build_index(corpus_dir):
    print("Parsing documents and building index (This will only happen once)...")
    documents = []
    metadata = []
    
    for root, _, files in os.walk(corpus_dir):
        if ".scratch" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            ext = file.lower().split('.')[-1]
            
            if ext == "pdf":
                try:
                    doc = fitz.open(file_path)
                    total_chars = 0
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        text = page.get_text("text")
                        total_chars += len(text.strip())
                        documents.append(text)
                        metadata.append({"type": "pdf", "file": file_path, "filename": file, "page": page_num})
                    doc.close()
                    if len(doc) > 0 and (total_chars / len(doc)) < 50:
                        print(f"[WARNING] {file} appears to be a scanned image. Text search will likely fail.")
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            elif ext in ["md", "txt", "csv"]:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        chunk_size = 50
                        for i in range(0, len(lines), chunk_size):
                            chunk_lines = lines[i:i + chunk_size]
                            text = "".join(chunk_lines)
                            if text.strip():
                                documents.append(text)
                                metadata.append({
                                    "type": "text", 
                                    "file": file_path, 
                                    "filename": file, 
                                    "start_line": i + 1, 
                                    "end_line": i + len(chunk_lines)
                                })
                except Exception as e:
                    print(f"Error reading text {file}: {e}")

    if not documents:
        return None, None

    # Tokenize and create BM25S index
    corpus_tokens = bm25s.tokenize(documents)
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)
    
    return retriever, metadata

def search_corpus(query, corpus_dir):
    start_time = time.time()
    print(f"--- Ultra-Advanced Hybrid RAG Search (Hyper-Speed) ---")
    print(f"Query: '{query}'")
    
    scratch_dir = ensure_scratch_dir(corpus_dir)
    cache_path = os.path.join(scratch_dir, "search_cache.pkl")
    
    current_manifest = get_corpus_manifest(corpus_dir)
    
    retriever = None
    metadata = None
    
    # Smart Cache Invalidation
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            if cache_data.get('manifest') == current_manifest:
                print("Cache hit! Loading index from disk...")
                retriever = cache_data['retriever']
                metadata = cache_data['metadata']
            else:
                print("Corpus changed. Rebuilding cache...")
        except Exception as e:
            print(f"Cache corrupted. Rebuilding... ({e})")
            
    if retriever is None:
        retriever, metadata = build_index(corpus_dir)
        if retriever is not None:
            # Save to cache
            with open(cache_path, 'wb') as f:
                pickle.dump({
                    'manifest': current_manifest,
                    'retriever': retriever,
                    'metadata': metadata
                }, f)
                
    if retriever is None:
        print("No readable documents found.")
        return

    # Search
    query_tokens = bm25s.tokenize([query])
    results, scores = retriever.retrieve(query_tokens, corpus=metadata, k=3)
    
    print(f"\n--- Top Results (Found in {time.time() - start_time:.3f}s) ---")
    
    # bm25s returns numpy arrays for results and scores.
    # results[0] contains the top k metadata items for the first query.
    for i in range(len(results[0])):
        score = float(scores[0][i])
        if score == 0:
            continue
            
        data = results[0][i]
        print(f"\nResult #{i+1} (Score: {score:.2f})")
        print(f"File: {data['filename']}")
        
        if data["type"] == "pdf":
            print(f"Page: {data['page'] + 1}")
            safe_filename = f"temp_{data['filename']}_pg_{data['page']+1}.pdf"
            safe_path = os.path.join(scratch_dir, safe_filename)
            if extract_pages(data['file'], data['page'], safe_path):
                print(f"[ACTION REQUIRED] AI Agent: Use `view_file` on this path to see the page & images:\n--> {safe_path}")
        
        elif data["type"] == "text":
            print(f"Lines: {data['start_line']} to {data['end_line']}")
            print(f"[ACTION REQUIRED] AI Agent: Use `view_file` on the original file using StartLine and EndLine arguments:\n--> {data['file']} (StartLine: {data['start_line']}, EndLine: {data['end_line']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search a corpus (PDFs and Text) using BM25S with caching.")
    parser.add_argument("query", type=str, help="The search query.")
    parser.add_argument("directory", type=str, help="Directory containing the corpus.")
    args = parser.parse_args()
    
    search_corpus(args.query, args.directory)

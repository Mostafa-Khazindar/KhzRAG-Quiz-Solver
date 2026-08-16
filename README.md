# OmniRAG Quiz Solver: The Ultimate Hybrid-RAG Agent

This repository contains a state-of-the-art [Antigravity](https://antigravity.google) skill designed to turn any AI agent into an expert academic assistant and ultra-fast quiz solver capable of parsing **massive corpora** (hundreds of books, gigabyte-sized PDFs, or giant Markdown codebases).

It is a **100% Dynamic Hybrid System**. It doesn't rely on just one trick; it gives the AI the autonomy to choose the best tool for the job.

## Why this is the "Best of the Best"
- **Hyper-Speed Caching:** It uses smart file-timestamp caching. The first time you ask a question, it builds a local index. The next 100 questions you ask will return results in **milliseconds**, skipping the entire PDF parsing process!
- **Numpy-Powered `bm25s`:** We dropped `rank_bm25` for the cutting-edge `bm25s` library, making the search up to 500x faster on massive corpora.
- **Dynamic Tool Selection (Grep vs. RAG):** The AI intelligently analyzes the user's question and the corpus type. If the corpus is Markdown text or the user wants an exact quote, the AI autonomously switches to native `grep_search` (which is lightning fast). If the corpus contains PDFs or requires conceptual searching, it uses the Python RAG engine.
- **Universal File Support:** The Python search engine (`scripts/search_corpus.py`) doesn't just read PDFs. It now reads `.md`, `.txt`, and `.csv` files, chunking them intelligently by line numbers and feeding precise coordinates back to the AI.
- **Zero-Setup Search Engine:** Powered by `uv` and PEP 723 inline dependencies. You just run it—no virtual environments or `pip install` headaches required.
- **Safe Page Extraction:** When the search engine finds the answer on "Page 455" of a PDF, it safely slices out pages 454-456 into a tiny, safe PDF for the AI to view. This prevents Context Window crashes.
- **Flawless Visual Priority:** Because the AI reads the original PDF pages, **it can see the images, charts, and graphs perfectly**.

## How to install

Clone this repository into your project's `.agents` folder:

```bash
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/YOUR_USERNAME/omnirag-agent.git omni-rag
```
*(Note: You must have Python and `uv` installed on your system to use the advanced massive-corpus search).*

## Directory Structure
- `scripts/search_corpus.py`: The ultra-fast Python search engine (supports PDFs and Text).
- `SKILL.md`: The main orchestrator brain that controls tool selection.
- `examples/perfect_answer.md`: Teaches the AI how to format output via example.
- `references/visual_analysis_guide.md`: Advanced tips for the AI on how to read charts and graphs.

## ⚖️ Legal & Ethical Disclaimer (Please Read)
**1. No Academic Dishonesty:** This tool is designed to assist with research, studying, and locating information rapidly within massive datasets. It is NOT intended to facilitate academic cheating, plagiarism, or unauthorized assistance during closed-book exams. Users are strictly responsible for adhering to their institution's academic integrity policies.
**2. Copyright & Intellectual Property:** This tool processes files provided by the user locally on their machine. The creators and contributors of this software do not condone or support software piracy or copyright infringement. Users must ensure they possess the legal right or appropriate licenses to parse, index, and use the documents (e.g., textbooks, PDFs) they input into this system.
**3. Liability:** Released under the MIT License. The software is provided "as is", without warranty of any kind. The creators assume no liability for how users choose to utilize this software.

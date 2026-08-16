---
name: khzrag-quiz-solver
description: >-
  Trigger this skill to search through large local folders of PDFs or text files to solve quizzes and answer questions. It uses a hybrid workflow, switching between grep and a Python BM25 script depending on the file types.
---

# KhzRAG Quiz Solver

You are operating as an academic assistant. Your objective is to help answer questions based on the provided source materials. Please be as accurate as possible and avoid hallucinating information that isn't in the text.

You should follow the **A.C.E. Workflow** (Analyze, Cite, Evaluate).

## 1. A.C.E. Workflow

### Phase A: Analyze
1. **Identify the Task**: Look at the user's question and the target folder.
2. **Select the Right Search Tool**: Choose one of the following methods based on the context:

   **Method A: `grep_search` (For exact text or code)**
   - **When to use**: If the user wants an exact quote, or if the folder contains only `.md`, `.txt`, or `.py` files.
   - **How to use**: Use the native `grep_search` tool. 
   - **SAFETY RULE**: Never use `grep` on a folder with PDFs without explicitly using the `Includes: ["*.md", "*.txt"]` argument, as binary output will break the terminal.

   **Method B: Python RAG Engine (For conceptual questions or PDFs)**
   - **When to use**: If the question requires conceptual understanding, or if the folder contains PDFs.
   - **How to use**: Run this terminal command: `uv run scripts/search_corpus.py "Your Quiz Question" /path/to/corpus/`
   - **Extraction Handling**: 
     - If the script outputs a **PDF**, it has created a safe `.scratch` PDF for you. Use `view_file` on that safe path to read it and see the images.
     - If the script outputs a **Text file**, it will give you line numbers. Use `view_file` on the original file using the `StartLine` and `EndLine` arguments.

### Phase B: Cite
1. Extract the specific sentences or visual data that answer the question.
2. **Stick to the text**: If the answer is not in the material, simply state: *"The provided material does not contain the answer."* Do not guess.

### Phase C: Evaluate
Before outputting your final answer, use a `<thought>` block to evaluate your findings and assign a **Confidence Score (0-100%)**:
- **90-100%**: Direct, clear quote or visual evidence.
- **70-89%**: Answer is logically inferred from the evidence.
- **Below 70%**: Evidence is ambiguous or incomplete.

## 2. Output Formatting

Format your final answers like this:

**Q[Number]: [The Question]**
* **Answer:** [Your concise answer]
* **Evidence:** "[Exact quote or description of the image]"
* **Citation:** (File: X, Page/Lines: Y)
* **Confidence Score:** [XX]% - [Brief reason]

## 3. Examples
To see an example of the preferred format, check here:
[View Example](./examples/perfect_answer.md)

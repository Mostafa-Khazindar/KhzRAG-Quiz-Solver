# KhzRAG Quiz Solver

![KhzRAG Architecture](https://img.shields.io/badge/Architecture-Agentic%20Hybrid%20RAG-blue?style=for-the-badge) ![Performance](https://img.shields.io/badge/Performance-bm25s-success?style=for-the-badge)

This is a local Python RAG (Retrieval-Augmented Generation) engine integrated with the [Antigravity](https://antigravity.google) framework. It helps AI agents quickly search through large local directories containing PDFs, Markdown, and code to answer questions and solve quizzes.

The goal of this project is to handle the common issue where an LLM's context window crashes when trying to read too many large PDFs at once. 

## Features
- **Dynamic Search Routing:** The AI decides whether to use native `grep` (for fast exact-text matching in code/markdown) or the Python RAG script (for searching inside PDFs and conceptual queries).
- **Local Index Caching:** Built on top of the `bm25s` library. When you query a folder for the first time, it builds a local index. Follow-up queries are much faster since it doesn't need to re-parse the PDFs. It uses a file-timestamp manifest to know when to rebuild the cache.
- **Context-Window Protection:** When the search script finds a relevant page in a large PDF, it extracts just that specific page (and the surrounding pages) into a temporary `.scratch` file. The AI reads this small file instead of the whole book.
- **Image & Diagram Support:** Because the AI views the extracted PDF pages directly, it can see and interpret charts and graphs that normal text-based extraction would miss.

## Installation

Clone this repository into your project's `.agents` folder:

```bash
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/Mostafa-Khazindar/KhzRAG-Quiz-Solver.git khzrag
```
*(Requires Python and `uv`. The search script handles dependencies automatically via PEP 723).*

## Directory Structure
- `scripts/search_corpus.py`: The Python backend for parsing and caching PDFs/text.
- `SKILL.md`: The system prompt that guides the AI's tool selection and workflow.
- `examples/perfect_answer.md`: A basic formatting template for the AI output.
- `references/visual_analysis_guide.md`: Instructions for the AI on how to handle non-searchable images.

## Legal & Ethical Notes
1. **Academic Integrity:** This project is intended as a research and study aid. It is not meant to facilitate cheating or academic dishonesty. Please follow your institution's rules.
2. **Copyright:** Ensure you have the right to parse and index the documents you use with this tool.
3. **Liability:** Released under the MIT License. The software is provided "as is", without warranty of any kind.

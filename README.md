# KhzRAG: Autonomous Hybrid-RAG Agent Architecture

![KhzRAG Architecture](https://img.shields.io/badge/Architecture-Agentic%20Hybrid%20RAG-blue?style=for-the-badge) ![Performance](https://img.shields.io/badge/Performance-Ultra--Fast%20%28bm25s%29-success?style=for-the-badge)

This repository demonstrates advanced AI Orchestration by integrating a state-of-the-art Python RAG engine with the [Antigravity](https://antigravity.google) framework. It is designed to turn any AI agent into an expert academic assistant capable of parsing **massive corpora** (hundreds of books, gigabyte-sized PDFs, or giant Markdown codebases).

This project highlights best practices in **Context-Window Optimization**, **Agentic Tool Selection**, and **Local AI Infrastructure**.

## 🚀 Key Architectural Features
- **Dynamic Tool Selection (Grep vs. RAG):** The AI acts as an orchestrator, intelligently analyzing the user's prompt and the corpus type. If the corpus is Markdown/Code, it autonomously switches to native `grep_search` for instant exact-match retrieval. For PDFs or conceptual queries, it utilizes the Python RAG engine.
- **Hyper-Speed Caching (Zero-Stale Data):** Implements a persistent disk cache with a smart file-timestamp manifest. Initial indexing takes seconds, but subsequent queries bypass parsing entirely, returning results in **milliseconds**.
- **Numpy-Powered `bm25s`:** Drops legacy pure-python implementations for the cutting-edge `bm25s` library, achieving up to 500x faster searches on massive corpora.
- **Context-Window Protection (Safe Extraction):** When the engine locates relevant information on "Page 455" of a massive PDF, it safely extracts only pages 454-456 into a lightweight temporary PDF. The AI reads this micro-document, completely eliminating context-window crashes.
- **Flawless Multi-Modal Vision:** Because the AI reads the original (extracted) PDF pages, **it successfully parses and interprets images, charts, and graphs**—a critical feature that traditional text-only RAG pipelines destroy.

## 💻 Installation & Usage

Clone this repository into your project's `.agents` folder to automatically mount the skill into your Antigravity environment:

```bash
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/Mostafa-Khazindar/KhzRAG-Quiz-Solver.git khzrag
```
*(Note: Requires Python and `uv`. The search engine uses PEP 723 inline dependencies for zero-setup execution).*

## 📂 System Design
- `scripts/search_corpus.py`: The ultra-fast Python search engine (handles PDF/Text chunking and caching).
- `SKILL.md`: The main orchestrator prompt governing the AI's Decision Tree and A.C.E. Workflow (Analyze, Cite, Evaluate).
- `examples/perfect_answer.md`: Few-shot prompting template to enforce strict output formatting.
- `references/visual_analysis_guide.md`: Advanced guardrails for multi-modal image interpretation.

## ⚖️ Legal & Ethical Disclaimer
**1. Purpose:** This tool demonstrates advanced AI retrieval techniques and is designed to assist with legitimate research and data extraction. 
**2. Academic Integrity:** This software is NOT intended to facilitate academic dishonesty. Users are strictly responsible for adhering to their institution's integrity policies.
**3. Copyright:** Users must ensure they possess the legal right to parse and index any proprietary documents inputted into this system.
**4. Liability:** Released under the MIT License. The software is provided "as is", without warranty of any kind.

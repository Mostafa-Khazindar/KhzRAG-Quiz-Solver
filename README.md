# KhzRAG Quiz Solver

![KhzRAG Architecture](https://img.shields.io/badge/Architecture-Agentic%20Hybrid%20RAG-blue?style=for-the-badge) ![Performance](https://img.shields.io/badge/Performance-bm25s-success?style=for-the-badge)

This is a local Python RAG (Retrieval-Augmented Generation) engine integrated with the [Antigravity](https://antigravity.google) framework. It helps AI agents quickly search through large local directories containing PDFs, Markdown, and code to answer questions and solve quizzes.

The goal of this project is to handle the common issue where an LLM's context window crashes when trying to read too many large PDFs at once. 

## Features
- **Dynamic Search Routing:** The AI decides whether to use native `grep` (for fast exact-text matching in code/markdown) or the Python RAG script (for searching inside PDFs and conceptual queries).
- **Local Index Caching:** Built on top of the `bm25s` library. When you query a folder for the first time, it builds a local index. Follow-up queries are much faster since it doesn't need to re-parse the PDFs. It uses a file-timestamp manifest to know when to rebuild the cache.
- **Context-Window Protection:** When the search script finds a relevant page in a large PDF, it extracts just that specific page (and the surrounding pages) into a temporary `.scratch` file. The AI reads this small file instead of the whole book.
- **Image & Diagram Support:** Because the AI views the extracted PDF pages directly, it can see and interpret charts and graphs that normal text-based extraction would miss.

## 📖 Step-by-Step Tutorial (How to use with Antigravity)

Because Antigravity uses an auto-discovery system for skills, you don't need to write any complicated configuration files. Just put the folder in the right place and talk to the AI!

### Step 1: Install the Skill
You can install this skill either **Locally** (for just one project) or **Globally** (so it works everywhere on your computer).

**Option A: Local Installation (Recommended for specific projects)**
Navigate to your project folder in the terminal and run:
```bash
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/Mostafa-Khazindar/KhzRAG-Quiz-Solver.git khzrag
```

**Option B: Global Installation**
If you want KhzRAG available no matter what folder you have open in Antigravity, clone it into your global config directory:
- **Windows:** `C:\Users\YOUR_NAME\.gemini\config\plugins\skills\`
- **Mac/Linux:** `~/.gemini/config/plugins/skills/`

*(Note: You must have Python and `uv` installed on your system. The search script handles all Python dependencies automatically via PEP 723 inline script metadata).*

### Step 2: Prepare your Corpus
Put all your textbooks, PDFs, and Markdown notes into a folder inside your workspace (for example, a folder named `study_materials/`).

### Step 3: Trigger the Skill in Chat
Open the Antigravity chat interface and simply ask the AI to use the skill. You don't need any special commands, just natural language:

> *"Use the khzrag-quiz-solver skill to answer the quiz questions in `exam.md`. The textbooks are located in the `study_materials/` folder."*

The Antigravity AI will instantly detect the `khzrag-quiz-solver` skill, read the instructions in `SKILL.md`, and autonomously run the Python script to find your answers!

## Directory Structure
- `scripts/search_corpus.py`: The Python backend for parsing and caching PDFs/text.
- `SKILL.md`: The system prompt that guides the AI's tool selection and workflow.
- `examples/perfect_answer.md`: A basic formatting template for the AI output.
- `references/visual_analysis_guide.md`: Instructions for the AI on how to handle non-searchable images.

## Legal & Ethical Notes
1. **Academic Integrity:** This project is intended as a research and study aid. It is not meant to facilitate cheating or academic dishonesty. Please follow your institution's rules.
2. **Copyright:** Ensure you have the right to parse and index the documents you use with this tool.
3. **Liability:** Released under the MIT License. The software is provided "as is", without warranty of any kind.

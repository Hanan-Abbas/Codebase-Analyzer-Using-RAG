# 🚀 RepoMind – AI-Powered Codebase Navigator

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**RepoMind** turns any GitHub repository into an interactive knowledge base.  
It clones the repo, indexes the code with embeddings + FAISS, and lets you **chat with the codebase** through a clean web UI or a terminal CLI.  
Over time, RepoMind learns from your feedback and improves the quality of its answers.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone & Create Environment](#clone--create-environment)
  - [Install Dependencies](#install-dependencies)
  - [Configure Environment Variables](#configure-environment-variables)
- [Running the Project](#running-the-project)
  - [Start the FastAPI Backend](#start-the-fastapi-backend)
  - [Open the Web UI](#open-the-web-ui)
  - [Using the CLI](#using-the-cli)
- [How It Works](#how-it-works)
  - [Ingestion Pipeline](#ingestion-pipeline)
  - [Query Pipeline](#query-pipeline)
  - [Feedback & Learning Loop](#feedback--learning-loop)
- [Configuration](#configuration)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

RepoMind is a **repository-aware RAG engine**:

- It clones a GitHub repository locally.
- Scans and chunks code files intelligently.
- Embeds them with Sentence-Transformers.
- Indexes them using **FAISS** for fast semantic search.
- Uses a Groq-hosted LLM (OpenAI-compatible API) to answer natural-language questions about the code.
- Learns from explicit user feedback (👍 / 👎) to improve retrieval quality over time.

You can interact with RepoMind in two ways:

- A **web UI** (`frontend/index.html`) powered by FastAPI endpoints.
- A **terminal-based CLI** (`main.py`) with a Rich-powered chat interface.

---

## Screenshots

> Replace the image placeholders below with your own project screenshots.

### Web UI – Home / Connect Repo

```md
![Web UI – Connect Repository](docs/images/web-home.png)
```

### Web UI – Chat with Codebase

```md
![Web UI – Chat Session](docs/images/web-chat.png)
```

### CLI – Interactive Session

```md
![CLI – RepoMind Terminal Chat](docs/images/cli-chat.png)
```

---

## Features

- **Codebase-Aware Chat**: Ask questions about functions, architecture, and files using natural language.
- **Semantic Code Search**: Retrieves code chunks based on meaning, not just keyword matching.
- **FAISS Vector Indexing**: Efficient nearest-neighbor search over code embeddings.
- **FastAPI Backend**: Production-ready API exposing `/ingest`, `/chat`, `/feedback`, and `/health`.
- **Modern Web UI**:
  - TailwindCSS styling.
  - Markdown rendering (via `marked`).
  - Code highlighting (via `Prism`).
  - Recent repositories list and progress bar for ingestion.
- **CLI Experience**: Rich-based terminal interface for power users.
- **Feedback-Driven Learning**:
  - Users can rate answers in the web UI (👍 / 👎).
  - Feedback is stored in SQLite and used by a `RankingOptimizer` to boost helpful chunks in future queries.
- **Local-First Storage**:
  - Cloned repos are stored under `data/repos/`.
  - Vector indices and metadata are stored under `data/vectors/`.
  - Feedback is stored under `data/databases/`.

---

## Architecture

At a high level, RepoMind consists of:

- **FastAPI service** (`app_api.py`)
  - `POST /ingest` – clone + index a new GitHub repo, or load an existing FAISS index from disk.
  - `POST /chat` – run the query pipeline on the currently active repo.
  - `POST /feedback` – store explicit user feedback (question, answer, rating).
  - `GET /health` – basic health and cache status for monitoring.
  - Maintains a **process-wide cache**:
    - Single shared `Embedder`.
    - Per-repo `VectorStore` instances in memory (plus disk persistence).

- **Core pipelines** (`src/pipelines/`)
  - `ingest_pipeline.py` – orchestrates cloning, scanning, chunking, embedding, and saving FAISS indices.
  - `query_pipeline.py` – orchestrates retrieval, reranking, prompt building, and LLM answering.

- **Services** (`src/services/`)
  - `repository_service` – cloning and repo metadata.
  - `processing_service` – code cleaning and chunking.
  - `embedding_service` – Sentence-Transformers wrapper.
  - `vector_service` – FAISS index + metadata persistence.
  - `llm_service` – prompt construction and LLM calls (Groq/OpenAI-compatible).
  - `learning_service` – feedback storage (`FeedbackCollector`) and ranking optimization (`RankingOptimizer`).

- **UI layers**
  - Web frontend: `frontend/index.html` (static SPA calling the FastAPI backend).
  - CLI: `src/ui/cli_chat.py` and `main.py`.

---

## Project Structure

```text
REPO Analyzer/
├── app_api.py                 # FastAPI application (backend API)
├── main.py                    # CLI entry point (terminal chat)
├── config/
│   └── settings.py            # Central configuration & .env loading
├── frontend/
│   └── index.html             # Web UI (Tailwind, marked, Prism)
├── src/
│   ├── pipelines/
│   │   ├── ingest_pipeline.py # Ingestion/indexing pipeline
│   │   └── query_pipeline.py  # Query + ranking + LLM pipeline
│   ├── services/
│   │   ├── repository_service/
│   │   │   ├── clone_repo.py
│   │   │   └── repo_metadata.py
│   │   ├── processing_service/
│   │   │   ├── code_cleaner.py
│   │   │   └── code_chunker.py
│   │   ├── embedding_service/
│   │   │   └── embedder.py
│   │   ├── vector_service/
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   ├── llm_service/
│   │   │   ├── prompt_builder.py
│   │   │   └── answer_generator.py
│   │   └── learning_service/
│   │       ├── feedback_collector.py
│   │       └── optimizer.py
│   └── ui/
│       └── cli_chat.py        # Rich-based CLI chat UI
├── data/
│   ├── repos/                 # Cloned repositories
│   ├── vectors/               # Saved FAISS indices & metadata
│   └── databases/             # SQLite feedback database
├── requirements.txt
├── .env                       # Environment configuration (not committed)
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python** 3.12+
- **Git** installed and on your PATH
- A **Groq API key** (for LLM calls)
- Linux, macOS, or WSL recommended

### Clone & Create Environment

```bash
git clone https://github.com/your-username/repomind.git
cd "REPO Analyzer"

python3 -m venv codebase
source codebase/bin/activate        # Windows: .\codebase\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

`config/settings.py` will load this file automatically and expose these values to the rest of the app.

---

## Running the Project

### Start the FastAPI Backend

From the project root (with the virtualenv activated):

```bash
python3 app_api.py
```

This starts the API at `http://0.0.0.0:8000` with the following key endpoints:

- `POST /ingest`
- `POST /chat`
- `POST /feedback`
- `GET /health`

You can quickly verify the server with:

```bash
curl http://localhost:8000/health
```

### Open the Web UI

1. Open `frontend/index.html` directly in your browser (or serve it via a simple static file server).
2. Paste a GitHub repository URL into the input and click **Analyze**.
3. Wait for the progress bar to complete and the status to show **“Successfully connected … Ready to chat!”**.
4. Ask questions in the chat input at the bottom.
5. For each AI answer, use the **👍 / 👎** buttons to provide feedback (this will improve future results).

> You can add a screenshot of this flow here:
>
> ```md
> ![Web UI – Full Flow](docs/images/web-flow.png)
> ```

### Using the CLI

The CLI uses the same pipelines and configuration but runs in the terminal:

```bash
python3 main.py
```

You will be prompted for:

- A GitHub repository URL.
- Whether to reuse an existing index (if found).

Then you can type natural-language questions about the codebase and optionally rate answers (depending on your CLI flow).

> Add a CLI screenshot here:
>
> ```md
> ![CLI – RepoMind Session](docs/images/cli-session.png)
> ```

---

## How It Works

### Ingestion Pipeline

1. **Clone repository** – `RepoCloner` clones the target GitHub repo into `data/repos/<repo_name>`.
2. **Scan files** – Walks the repo tree, skipping `IGNORE_DIRS` and selecting only `SUPPORTED_EXTENSIONS`.
3. **Chunk code** – `CodeChunker` uses language-aware splitting (via LangChain text splitters) to build semantically meaningful chunks and attaches metadata such as relative `file_path`.
4. **Embed chunks** – `Embedder` encodes each chunk’s text using a Sentence-Transformers model on CPU.
5. **Build vector index** – `VectorStore` stores embeddings in FAISS and saves metadata + a `structure.json` file listing all observed file paths.
6. **Persist & cache** – The index is written to `data/vectors/<repo_name>` and also cached in memory when requested via FastAPI.

### Query Pipeline

1. **Retrieve** – `Retriever` encodes the user query and searches in FAISS for top-k similar chunks.
2. **Rerank with feedback** – `RankingOptimizer` consults `feedback.db` and boosts chunks that historically led to helpful answers.
3. **Build prompt** – `PromptBuilder` assembles:
   - A “physical file system” view from `VectorStore.get_verified_structure()`.
   - The top ranked code chunks with clear source file markers.
   - Instructions tailored for code understanding and architecture explanations.
4. **Generate answer** – `AnswerGenerator` calls the Groq-hosted LLM (OpenAI-compatible API) and streams the answer back to the caller.

### Feedback & Learning Loop

1. The frontend asks, **“Was this helpful?”** after each AI answer.
2. On a 👍 or 👎 click, it sends `POST /feedback` with:
   - `question` – the user’s original prompt.
   - `answer` – the full AI response.
   - `rating` – 1 for helpful, 0 for not helpful.
3. `FeedbackCollector` writes this into a SQLite DB under `data/databases/feedback.db`.
4. For future queries, `RankingOptimizer` reads this DB and slightly increases the score of chunks that have received positive feedback, biasing retrieval toward code that users found useful.

Over time, this makes RepoMind **more accurate and tailored** to your way of asking questions.

---

## Configuration

All core configuration lives in `config/settings.py`:

- **Paths**
  - `BASE_DIR`, `REPO_STORAGE`, `VECTOR_DB_PATH`
- **Chunking**
  - `CHUNK_SIZE`, `CHUNK_OVERLAP`
  - `SUPPORTED_EXTENSIONS`
  - `IGNORE_DIRS`
- **Models & LLM**
  - `EMBEDDING_MODEL` (from `EMBEDDING_MODEL` env var, default `all-MiniLM-L6-v2`)
  - `GROQ_API_KEY`, `GROQ_BASE_URL`
  - `LLM_MODEL`

Adjust these values (or the `.env` file) to customize behavior for your environment.

---

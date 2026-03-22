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

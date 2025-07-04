# 🧠 GPT Terminal Assistant

A terminal-based AI assistant powered by OpenAI's GPT models. It supports context-aware conversations using a vector database (ChromaDB), token limiting with `tiktoken`, evaluation logging, and modular design for future expansion.

---

## 🚀 Features

- Chat with GPT-3.5/4 using terminal
- Context-aware replies using vector database
- Token limit enforcement for model safety
- Modular, testable architecture (`ChatEngine`, `VectorStore`)
- CLI-first, with hooks for GUI or API expansion
- Evaluation logs and debug tools
- GitHub Actions CI setup with `uv` package manager

---

## 🛠️ Tech Stack

| Component        | Tool/Library          |
|------------------|-----------------------|
| LLM API          | OpenAI GPT            |
| Vector DB        | ChromaDB              |
| Embedding        | OpenAI Embeddings     |
| Tokenization     | `tiktoken`            |
| Packaging/Env    | `uv`, `pyproject.toml`|
| Testing          | `pytest`              |
| CI/CD            | GitHub Actions        |
| CLI Dev          | Python (>=3.12)       |

---

## 📦 Installation

1. **Clone the repo**
```bash
git clone https://github.com/vrp-314/gpt-terminal-assistant.git
cd gpt-terminal-assistant
---
##
2. **Install dependencies with uv**
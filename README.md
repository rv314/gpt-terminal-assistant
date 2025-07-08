# GPT Terminal Assistant

A terminal-based AI assistant powered by modular LLM, embedding & vector store backends using registry patterns and configuration. Current stack:

- **LLM**: OpenAI GPT‑3.5‑turbo / GPT‑4 (configurable via `config.json`)
- **Embeddings**: OpenAI (via registry)
- **Vector DB**: ChromaDB (persisted, also pluggable via registry)
- **Prompting**: YAML-based prompt templates (RAG-style context injection)
- **Logging**: JSONL eval logs + debug logging (configurable directory)
- **CLI**: terminal interface with interactive model selection
- **Tests & CI**: `pytest`, GitHub Actions + `uv` (PEP 582), coverage masks for missing OpenAI key

---
## 📥 Installation

Please refer to **[INSTALLATION.md](./INSTALLATION.md)** for full setup, including environment variable config and dependencies.

---

## 📌 Highlights and Features

### 🧠 Context-Aware LLM Assistant (RAG-Enabled)

This assistant implements a **Retrieval-Augmented Generation (RAG)** pipeline using a local vector database (ChromaDB):

- 🔍 **Embeddings & Semantic Search**: Each message is embedded using `OpenAIEmbeddings`, enabling retrieval of semantically similar past messages.
- 💬 **Context Injection**: Retrieved context is injected into the system prompt, allowing the assistant to remember and reference past interactions.
- 🧾 **Eval-Ready Logging**: Context, distances, and scores are logged to evaluate RAG effectiveness.

> ✅ Vector store is modular — easily swap to **Pinecone**, **Qdrant**, or **Weaviate** for production-scale setups.

---

## ⚙️ Configuration-driven architecture

Located at `config.json`, controlling:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "available_models": ["gpt-3.5-turbo", "gpt-4"]
  },
  "embedding": {
    "provider": "openai"
  },
  "vector_store": {
    "provider": "chroma",
    "persist_directory": "vectors/chroma"
  },
  "logging": {
    "debug": true,
    "log_dir": "logs"
  },
  "max_tokens": 3000
}
```
---

#### Seamlessly Add/change providers like qdrant, sentence_transformer, or new LLM backends centrally. No code changes needed.

## 💡 Features

- Registry Pattern: Plug-and-play support for embeddings, vector stores, and LLMs.
- Prompt Decoupling: Templates in `src/llm/prompt.yaml` using `{{context}}` placeholder.
- Context-aware RAG Prompting
- Logging: Eval logs stored in `logs/eval_log.jsonl`; debug logs in `logs/debug.log`.
- Token Limits
- Automated Tests & CI

---

## 🧰 Tools & Tech Stack

| Category        | Tools / Libraries                               |
|-----------------|-------------------------------------------------|
| Language        | Python 3.12                                     |
| Package Manager | [uv](https://github.com/astral-sh/uv) (PEP 582) |
| Embeddings      | OpenAI / SentenceTransformers (optional)        |
| Vector DB       | ChromaDB (swap-ready for Qdrant or Pinecone)    |
| Prompting       | OpenAI Chat API + RAG                           |
| CLI             | Terminal-based interface (`input()`)            |
| CI/CD           | GitHub Actions + `uv` + `pytest`                |

---

## 🛣️ Roadmap

#### Completed
- [x] Registry support for VectorStore and Embeddings
- [x] Modular LLM registry with OpenAI backend
- [x] YAML-based prompt templates
- [x] Context retrieval + prompt injection
- [x] Logging & debug via config
- [x] CLI model selection
- [x] Test coverage and CI pipeline

#### Planned
- [ ] Add support for additional vector stores (e.g., FAISS, Qdrant)
- [ ] Add additional embedding models (e.g., SentenceTransformer, Instructor)
- [ ] Add more LLM backends (e.g., LLaMA, HuggingFace)
- [ ] Multi-prompt profiles (e.g., dev-assistant.yaml, science-assistant.yaml)
- [ ] Refactor CLI using argparse or similar

---

## 🧠 Developer Notes
- Registry folders:
  - `src/registries/embedding_registry.py`
  - `src/registries/vector_registry.py`
  - `src/registries/llm_registry.py`

- Backends:
  - `src/vector_backends/chroma_store.py`
  - `src/embeddings/openai_embedder.py`
  - `src/llm/openai_llm.py`

- Prompt files:
  - `src/llm/prompt.yaml`

- Utilities for token management and debug functionality all respect `config.json`

---

## 🤝 Contributing
Feel free to fork or create issues! This project is a stepping stone toward building your own agentic apps and LLM tools.

---

## 📜 License
MIT

---

## 🙋‍♂️ Maintainer
This project is currently maintained by the following individuals:

*   **RP** - GitHub: [@rv314](https://github.com/rv314)
# 🧠 GPT Terminal Assistant

A terminal-based AI assistant powered by OpenAI's GPT models. It supports context-aware conversations using a vector database (ChromaDB), token limiting with `tiktoken`, evaluation logging, and modular design for future expansion.

---

## 🛠️ Installation

➡️ For full setup and advanced usage, see the [📄 Full Installation Guide.]()

## 📌 Features

### 🧠 Context-Aware LLM Assistant (RAG-Enabled)

This assistant implements a **Retrieval-Augmented Generation (RAG)** pipeline using a local vector database (ChromaDB):

- 🔍 **Embeddings & Semantic Search**: Each message is embedded using `OpenAIEmbeddings`, enabling retrieval of semantically similar past messages.
- 💬 **Context Injection**: Retrieved context is injected into the system prompt, allowing the assistant to remember and reference past interactions.
- 🧾 **Eval-Ready Logging**: Context, distances, and scores are logged to evaluate RAG effectiveness.

> ✅ Vector store is modular — easily swap to **Pinecone**, **Qdrant**, or **Weaviate** for production-scale setups.

---

### 🧪 Test-Driven & CI-Ready

- ✅ Coverage for critical components using **`pytest`**
- 🔁 Automated testing via **GitHub Actions**
- 🔒 Uses **GitHub Secrets** or local skipping for `OPENAI_API_KEY`

---

### 🧰 Modular, Extensible Codebase

- 🧱 Organized by purpose: `chat_client.py`, `vector_store.py`, `token_utils.py`, `evaluation_logger.py`, etc.
- 🧪 Optional debug logger and evaluation scoring logic for observability
- 🧠 Smart token-aware message trimming with `tiktoken`

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

## 🧠 Vector Store

Messages are stored and retrieved using ChromaDB. Retrieval is based on semantic similarity using OpenAI embeddings.

You can view logs and evals inside:
```bash
logs/eval_log.jsonl
```
---

## 🧰 Developer Notes

- Code is modular and testable.
- Debug logs can be toggled via `debug_log()` in `utils/debug.py` (Work in progress).
- Token limit enforced using `trim_messages()` in `utils/token_utils.py`.

---

## 🧭 Roadmap

- [x] Terminal-based assistant with memory
- [x] Modular ChatEngine class
- [x] Token limiter + debug tools
- [x] CI/CD pipeline with uv
- [ ] Add journaling / reminder commands
- [ ] GUI layer using Streamlit/Gradio
- [ ] Plug into agent framework (e.g., LangGraph)

---

## 🤝 Contributing
Feel free to fork or create issues! This project is a stepping stone toward building your own agentic apps and LLM tools.

---

## 📄 License
MIT

---

## 🙋‍♂️ Maintainer
This project is currently maintained by the following individuals:

*   **RP** - GitHub: [@rv314](https://github.com/rv314)
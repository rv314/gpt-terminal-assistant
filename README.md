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
```

2. **Install dependencies with uv**
```bash
uv sync
```

3. **Create `.env` file**

```env
# .env
OPENAI_API_KEY=your-openai-key
```

## 🧪 Run Tests
```bash
uv run pytest
```
✅ Includes vector DB and token limiter tests.

## 💬 Usage
### 🖥️ Start the assistant
```bash
uv run python assistant/cli.py
```
#### OR
```bash
python -m assistant.cli
```

- Type your queries in terminal.
- Type exit to quit.

## 🧠 Vector Store

Messages are stored and retrieved using ChromaDB. Retrieval is based on semantic similarity using OpenAI embeddings.

You can view logs and evals inside:
```bash
logs/eval_log.jsonl
```

## 🧰 Developer Notes

- Code is modular and testable.
- Debug logs can be toggled via `debug_log()` in `utils/debug.py` (Work in progress).
- Token limit enforced using `trim_messages()` in `utils/token_utils.py`.

## 🧭 Roadmap

- [x] Terminal-based assistant with memory
- [x] Modular ChatEngine class
- [x] Token limiter + debug tools
- [x] CI/CD pipeline with uv
- [ ] Add journaling / reminder commands
- [ ] GUI layer using Streamlit/Gradio
- [ ] Plug into agent framework (e.g., LangGraph)

## 🤝 Contributing
Feel free to fork or create issues! This project is a stepping stone toward building your own agentic apps and LLM tools.

## 📄 License
MIT

## 🙋‍♂️ Maintainer
This project is currently maintained by the following individuals:

*   **RP** - GitHub: [@rv314](https://github.com/rv314)
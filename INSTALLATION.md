## 📦 Installation

1. **Clone the repo**
```bash
git clone https://github.com/rv314/gpt-terminal-assistant.git
cd gpt-terminal-assistant
```

2. **Create a virtual environment (uv-based)**
```bash
uv venv .venv
```

3. **Activate virtual environment**
```bash
# Linux/Mac
source .venv/bin/activate

# Windows (Powershell)
.venv\Scripts\Activate.ps1
```

4. **Install dependencies with uv from pyproject.toml**
```bash
uv sync
```

5. **Create `.env` file**

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
uv run gpt-assistant
```
#### OR
```bash
python -m assistant.cli
```

Then follow the interactive CLI:

- Select model (if multiple configured)
- Enter your prompt
- Context-aware response generated, token-limited, logged
- Cycle continues until you type exit
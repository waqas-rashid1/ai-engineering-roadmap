# RAG Assistant — Step 0 Complete

Talk-to-documents RAG app. **Step 0** sets up the environment and verifies the Claude API connection.

## Project structure (Step 0)

```
rag-assistant/
├── docs/
│   └── sample.txt      # placeholder document for later steps
├── test_key.py         # API smoke test — run this to pass Step 0 checkpoint
├── requirements.txt    # pinned dependencies (generated from pip freeze)
├── .env.example        # template for secrets (committed)
├── .env                # your API key (local only, gitignored)
├── venv/               # local Python environment (not committed)
└── README.md           # you are here
```

## File guide

| File | Purpose |
|------|---------|
| **`test_key.py`** | Sends one message to Claude and prints the reply. Proves your API key, venv, and SDK work. |
| **`docs/sample.txt`** | Sample text file. Used in Step 1 when we load documents into the pipeline. |
| **`requirements.txt`** | Exact package versions so anyone can `pip install -r requirements.txt` and get the same stack. |
| **`.env.example`** | Template — copy to `.env` and paste your Anthropic API key. |
| **`.env`** | Real secrets file on your machine only; never pushed to GitHub. |
| **`.gitignore`** | Excludes `venv/`, `chroma_db/`, `.env`, and Python caches from git. |
| **`venv/`** | Isolated Python 3.11 environment — packages installed here don't affect system Python. |

## Setup

```bash
cd rag-assistant

# Create & activate virtual environment (Python 3.11 recommended)
python3.11 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Secrets — copy the template and add your key (file is gitignored)
cp .env.example .env
# edit .env → ANTHROPIC_API_KEY=sk-ant-...

# Run the Step 0 checkpoint
python test_key.py
```

**✅ Checkpoint:** `test_key.py` prints a short friendly sentence from Claude.

## What Step 0 teaches (Phase 1 foundations)

- **Virtual environments** — isolate project dependencies
- **Environment variables** — store API keys outside source code
- **HTTP APIs via SDK** — `client.messages.create()` wraps a REST call to Anthropic
- **Message format** — conversations are lists of `{"role", "content"}` turns

## Next step

**Step 1 — Load documents into text** (`ingest.py`): extract text from PDFs and `.txt` files with source tracking for citations.

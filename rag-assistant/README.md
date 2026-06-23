# RAG Assistant

Talk-to-documents RAG app — upload files, ask questions, get cited answers.

| Step | Status | What it does |
|------|--------|--------------|
| 0 | Done | Project setup + Claude API smoke test |
| 1 | Done | Load PDFs/text into structured records |
| 2–9 | Pending | Chunk → embed → retrieve → answer → UI → eval |

## Project structure

```
rag-assistant/
├── docs/
│   └── sample.txt      # test document
├── ingest.py           # Step 1 — load files → {text, source, page}
├── test_key.py         # Step 0 — verify Anthropic API key
├── requirements.txt
├── .env.example
└── README.md
```

## File guide

| File | Purpose |
|------|---------|
| **`ingest.py`** | Reads PDF or text files. Returns a list of records with `text`, `source`, and `page` for citations. |
| **`test_key.py`** | Sends one message to Claude — proves API key + SDK work. |
| **`docs/sample.txt`** | Sample document used by the Step 1 checkpoint. |
| **`.env`** | Your Anthropic API key (local only, gitignored). |

## Setup

The virtual environment lives at **`~/.venvs/rag-assistant`** (not inside the project folder — this drive is too slow for venv’s thousands of small files).

```bash
cd rag-assistant

# One-time: create venv (already done if you ran this with the agent)
python3.11 -m venv ~/.venvs/rag-assistant

# Every session: activate
source activate.sh
# or: source ~/.venvs/rag-assistant/bin/activate

pip install -r requirements.txt

# Secrets — copy the template if you haven't yet
cp .env.example .env   # add ANTHROPIC_API_KEY=...
```

## Checkpoints

```bash
# Step 0 — API works
python test_key.py

# Step 1 — documents load with source metadata
python ingest.py
```

**Step 1 ✅:** prints record count, source name, and first 300 characters of text.

## Next step

**Step 2 — Chunk the text:** split records into overlapping pieces for retrieval (`chunk_text`, `build_chunks` in `ingest.py`).

# RAG Assistant

Talk-to-documents RAG app — upload files, ask questions, get cited answers.

| Step | Status | What it does |
|------|--------|--------------|
| 0 | Done | Project setup + Claude API smoke test |
| 1 | Done | Load PDFs/text into structured records |
| 2 | Done | Split text into overlapping chunks for retrieval |
| 3 | Done | Embed chunks and store in Chroma vector DB |
| 4–9 | Pending | Retrieve → answer → UI → eval |

## Project structure

```
rag-assistant/
├── docs/
│   └── sample.txt      # test document
├── ingest.py           # Steps 1–3 — load, chunk, embed, store
├── embeddings_demo.py  # Step 3 — see how semantic similarity works
├── chroma_db/          # auto-created vector store (gitignored)
├── test_key.py         # Step 0 — verify Anthropic API key
├── requirements.txt
├── .env.example
└── README.md
```

## File guide

| File | Purpose |
|------|---------|
| **`ingest.py`** | Loads PDF/text (Step 1), splits into overlapping chunks (Step 2). Each chunk has `text`, `source`, `page`, `chunk_id`. |
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

# Step 1–3 — load, chunk, index into Chroma
python ingest.py

# Optional — embedding intuition demo
python embeddings_demo.py
```

**Step 3 ✅:** prints indexed chunk count and creates `chroma_db/`.

## Next step

**Step 4 — Retrieve relevant chunks:** query the vector DB and get top-k similar passages (`rag.py`).

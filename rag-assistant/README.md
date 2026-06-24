# RAG Assistant

Talk-to-documents RAG app — upload files, ask questions, get cited answers.

| Step | Status | What it does |
|------|--------|--------------|
| 0 | Done | Project setup + Claude API smoke test |
| 1 | Done | Load PDFs/text into structured records |
| 2 | Done | Split text into overlapping chunks for retrieval |
| 3 | Done | Embed chunks and store in Chroma vector DB |
| 4 | Done | Retrieve top-k relevant chunks from Chroma |
| 5 | Done | Claude generates grounded answers with [n] citations |
| 6–9 | Pending | Memory → UI → eval |

## Project structure

```
rag-assistant/
├── docs/
│   └── sample.txt      # test document
├── ingest.py           # Steps 1–3 — load, chunk, embed, store
├── rag.py              # Steps 4–5 — retrieve chunks, generate cited answers
├── chroma_db/          # auto-created vector store (gitignored)
├── test_key.py         # Step 0 — verify Anthropic API key
├── requirements.txt
├── .env.example
└── README.md
```

## File guide

| File | Purpose |
|------|---------|
| **`rag.py`** | `retrieve()` finds similar chunks (Step 4). `ask()` retrieves + calls Claude with citations (Step 5). |
| **`ingest.py`** | Steps 1–3 — load, chunk, embed, store in Chroma. |
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

# Step 4–5 — retrieval + cited answer (run ingest.py first)
python rag.py
```

**Step 5 ✅:** grounded answer with `[1]` citations; off-topic questions get "don't have enough information."

## Next step

**Step 6 — Conversation memory:** multi-turn follow-ups via `ask(query, history=...)`.

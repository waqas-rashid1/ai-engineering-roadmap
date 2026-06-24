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
| 6 | Done | Multi-turn chat via `history` in `ask()` |
| 7–9 | Pending | UI → eval → README |

## Project structure

```
rag-assistant/
├── docs/
│   └── sample.txt      # test document
├── ingest.py           # Steps 1–3 — load, chunk, embed, store
├── demo_memory.py      # Step 6 — multi-turn conversation demo
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
| **`demo_memory.py`** | Step 6 — shows follow-up questions using `ask(..., history=...)`. |
| **`rag.py`** | `retrieve()` + `ask()` — supports optional `history` for multi-turn chat. |
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

# Step 6 — multi-turn memory (follow-ups like "what does the third one do?")
python demo_memory.py
```

**Step 6 ✅:** turn 2 answers correctly even though it never names "embed" — history carries context.

## Next step

**Step 7 — Streamlit UI:** file upload + chat interface (`app.py`).

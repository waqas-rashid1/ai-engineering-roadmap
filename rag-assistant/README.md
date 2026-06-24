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
| 7 | Done | Streamlit UI — upload, chat, sources, memory |
| 8 | Done | Evaluate retrieval + answer quality (`evaluate.py`) |
| 9 | Pending | Final README + architecture diagram |

## Project structure

```
rag-assistant/
├── evaluate.py         # Step 8 — retrieval + answer metrics
├── app.py              # Step 7 — Streamlit UI (main app)
├── ingest.py           # Steps 1–3 — load, chunk, embed, store
├── rag.py              # Steps 4–5 — retrieve + generate
├── demo_memory.py      # Step 6 — CLI memory demo
├── embeddings_demo.py  # Step 3 — embedding intuition
├── test_key.py         # Step 0 — API smoke test
├── docs/sample.txt
├── chroma_db/          # vector store (gitignored)
└── README.md
```

## File guide

| File | Purpose |
|------|---------|
| **`app.py`** | Full UI: upload/index docs, chat, expandable sources, session memory. |
| **`rag.py`** | `retrieve()` + `ask()` — RAG core used by the UI. |
| **`ingest.py`** | Load, chunk, embed, store in Chroma. |
| **`evaluate.py`** | Step 8 — golden tests: retrieval hit rate, keyword match, optional LLM judge. |

## Setup

Virtual env: **`~/.venvs/rag-assistant`** (see `activate.sh`).

```bash
cd rag-assistant
source activate.sh
pip install torch --index-url https://download.pytorch.org/whl/cpu  # first time only
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
```

## Run the app (Step 7)

```bash
source activate.sh
streamlit run app.py
```

1. Upload a PDF or `.txt` in the sidebar → **Index documents**
2. Ask a question in the chat box
3. Expand **Sources** to see retrieved chunks
4. Ask a follow-up — memory carries prior turns

## CLI checkpoints

```bash
python test_key.py       # Step 0
python ingest.py         # Steps 1–3
python rag.py            # Steps 4–5
python demo_memory.py    # Step 6
python evaluate.py       # Step 8 — metrics (run ingest.py first)
python evaluate.py --judge   # Step 8 + LLM-as-judge
```

## Next step

**Step 9 — Final README:** architecture diagram, setup docs, demo GIF.

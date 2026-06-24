# AI Engineering Roadmap

A **learn-by-building** journey from writing code to shipping real AI products — at least one guided project per week.

This repository is the home for the full roadmap, weekly project code, build guides, and progress updates. It is **not** a single-project repo; new projects are added here as the path continues.

---

## What this repo is

| Piece | Purpose |
|-------|---------|
| **[AI-Engineering-Roadmap.md](./AI-Engineering-Roadmap.md)** | Master curriculum — phases, concepts, skills, capstone |
| **`/projects` folders** | One folder per weekly build (code + README + evals) |
| **Build guides** | Step-by-step instructions with checkpoints |
| **Git history** | Each step / project pushed as it is completed |

**Cadence:** at least **one guided project per week**, each tied to a section of the roadmap. You read the concept → build the smallest real thing → measure it → push it.

---

## Philosophy

- **AI Engineering ≠ ML Engineering** — build on top of foundation models; don't train from scratch.
- **Evaluation is the golden thread** — measure retrieval, answers, cost, and quality from project one.
- **Simplest tool first** — `prompt → RAG → agents → fine-tuning` (only add complexity when metrics say you need it).
- **Learn by shipping** — three small projects beat fifty hours of passive video.

---

## Roadmap at a glance

```
Phase 1  Foundations     Python · SQL · APIs · Git
    ↓
Phase 2  AI / LLM        Prompts · Embeddings · RAG · Eval
    ↓
Phase 3  Production       Agents · Fine-tuning · Inference · Safety
    ↓
Phase 4  Capstone         End-to-end systems with monitoring
```

Full detail → **[AI-Engineering-Roadmap.md](./AI-Engineering-Roadmap.md)**

---

## Weekly projects

| Week | Project | Roadmap focus | Status | Folder |
|------|---------|---------------|--------|--------|
| 1 | **Talk to Documents (RAG Assistant)** | Phase 2 — RAG, embeddings, eval, Streamlit | Complete | [`rag-assistant/`](./rag-assistant/) |
| 2 | *TBD — Tool-using agent* | Phase 2/3 — function calling, agent loop | Planned | — |
| 3 | *TBD* | Phase 3 — production systems | Planned | — |
| 4+ | *TBD* | Capstone-scale builds | Planned | — |

Each project includes:

- Step-by-step build (0 → ship)
- Commented code explaining *why*, not just *what*
- Evaluation script or metrics
- Its own `README.md` with architecture diagram

---

## Project 1 — RAG Assistant (complete)

Upload PDFs or text, ask questions, get **cited answers**.

**Stack:** Claude · Chroma · sentence-transformers · Streamlit

```bash
cd rag-assistant
source activate.sh
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
streamlit run app.py
```

→ **[rag-assistant/README.md](./rag-assistant/README.md)** for full docs, architecture, and evaluation.

Build guide (local): `Project-1-RAG-Assistant-Build-Guide.md`

---

## How to follow along

1. Read the relevant **phase** in [AI-Engineering-Roadmap.md](./AI-Engineering-Roadmap.md)
2. Clone this repo and open the **current week's project** folder
3. Follow the build guide step by step — run each checkpoint before moving on
4. Watch commits land each step (same pattern every project)

```bash
git clone git@github.com:waqas-rashid1/ai-engineering-roadmap.git
cd ai-engineering-roadmap
```

---

## Repo structure

```
ai-engineering-roadmap/
├── README.md                    ← you are here (repo hub)
├── AI-Engineering-Roadmap.md    ← full curriculum
├── Project-1-RAG-Assistant-Build-Guide.md
├── rag-assistant/               ← Week 1 project
│   ├── app.py
│   ├── ingest.py
│   ├── rag.py
│   ├── evaluate.py
│   └── README.md
└── (future weekly projects…)
```

---

## Resources

- [AI Engineering — Chip Huyen](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — closest book match to this roadmap
- [Anthropic docs](https://docs.anthropic.com) · [OpenAI docs](https://platform.openai.com/docs) — APIs change fast; check often

---

## Author

**[waqas-rashid1](https://github.com/waqas-rashid1)** — documenting the path to AI Engineering in public, at least one project per week.

---

*Last updated: June 2026 · Week 1 complete*

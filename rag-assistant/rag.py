"""
rag.py — Steps 4–5: retrieve relevant chunks and generate cited answers.

Run (index first if chroma_db is empty):
    source activate.sh
    python ingest.py
    python rag.py

Step 4: retrieve()  — the "R" in RAG (Retrieval)
Step 5: ask()       — the "G" in RAG (Generation via Claude)
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

from ingest import get_collection

load_dotenv(Path(__file__).resolve().parent / ".env")

# ---------------------------------------------------------------------------
# Step 5 — Generation (Claude)
# ---------------------------------------------------------------------------

client = anthropic.Anthropic()

# System prompt = rules the model must follow for every answer.
# Kept separate from the user message (data + question).
SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the provided context passages.

Rules:
- Use only the information in the numbered context passages below.
- Cite the passages you rely on by their number in square brackets, e.g. [1] or [2].
- If the answer is not contained in the context, say you don't have enough information. Never invent facts.
- Be clear and concise."""


def build_context(chunks):
    """
    Format retrieved chunks as numbered passages for citations.

    Example output:
        [1] (from sample.txt)
        RAG lets a language model answer questions using your documents...

        [2] (from report.pdf, p.3)
        Chunk text here...
    """
    blocks = []
    for i, c in enumerate(chunks, start=1):
        loc = c["source"]
        if c["page"]:
            loc += f", p.{c['page']}"
        blocks.append(f"[{i}] (from {loc})\n{c['text']}")
    return "\n\n".join(blocks)


def answer(query, chunks, history=None):
    """
    Send retrieved chunks + question to Claude; return the reply text.

    Args:
        query:   User question
        chunks:  Output of retrieve()
        history: Optional prior turns for multi-turn chat (Step 6)
    """
    history = history or []
    context = build_context(chunks)

    # User message = data (context) + task (question)
    user_message = f"Context passages:\n\n{context}\n\nQuestion: {query}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        temperature=0,  # deterministic, factual — raise for creative tasks
        system=SYSTEM_PROMPT,
        messages=history + [{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def ask(query, history=None, k=4):
    """
    Full RAG pipeline: retrieve → generate.

    Returns:
        (answer_text, source_chunks) — answer for the user, chunks for UI/citations
    """
    chunks = retrieve(query, k=k)
    text = answer(query, chunks, history=history)
    return text, chunks


# ---------------------------------------------------------------------------
# Step 4 — Retrieval (Chroma)
# ---------------------------------------------------------------------------

def retrieve(query, k=4):
    """
    Find the k chunks whose embeddings are closest to the query.

    Chroma embeds the question with the same model used at index time,
    then returns nearest neighbors (lower distance = more similar).
    """
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": meta["source"],
            "page": meta["page"],
            "distance": dist,
        })
    return chunks


def _format_source(i, c):
    loc = c["source"]
    if c["page"]:
        loc += f" p.{c['page']}"
    return f"[{i}] {loc} (distance {c['distance']:.3f})"


if __name__ == "__main__":
    tests = [
        ("What are the four stages of the RAG pipeline?", True),
        ("How do quarterly revenue numbers look?", False),  # not in sample.txt
    ]

    for question, expect_answer in tests:
        print("=" * 60)
        print(f"Q: {question}\n")
        text, sources = ask(question, k=3)
        print(f"A: {text}\n")
        print("Sources:")
        for i, c in enumerate(sources, 1):
            print(f"  {_format_source(i, c)}")
        print()

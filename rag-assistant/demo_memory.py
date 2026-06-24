"""
demo_memory.py — Step 6: multi-turn conversation with history.

Run:
    source activate.sh
    python ingest.py      # if chroma_db is empty
    python demo_memory.py

Key idea: Claude is stateless — it forgets everything after each call unless
you pass prior turns in `messages`. We store plain Q/A pairs (not bulky context)
and pass them to ask(..., history=history) on each new question.

Retrieval still runs fresh for EVERY question (context matches current query).
History only helps Claude resolve pronouns like "the third stage" or "that".
"""

from rag import ask


def run_conversation(questions):
    """
    Simulate a chat: each question sees all prior plain Q/A turns.

    After each answer we append ONLY the short question and answer to history —
    not the retrieved chunks (those would bloat tokens and duplicate retrieval).
    """
    history = []

    for i, question in enumerate(questions, start=1):
        print("=" * 60)
        print(f"Turn {i}")
        print(f"Q: {question}\n")

        # ask() retrieves for THIS question, but Claude also sees `history`
        text, sources = ask(question, history=history, k=3)

        print(f"A: {text}\n")
        print("Retrieved from:", ", ".join(s["source"] for s in sources))

        # Save lean turns for the next call
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": text})

    print("=" * 60)
    print(f"History length: {len(history)} messages ({len(history) // 2} turns)")


if __name__ == "__main__":
    # Turn 2 never says "embed" or "stage 3" — it relies on Turn 1 + history
    run_conversation([
        "What are the four stages of the RAG pipeline?",
        "What does the third one do?",  # "the third one" = Embed (from prior answer)
        "Why do chunk size and overlap matter?",  # also in sample.txt
    ])

"""
evaluate.py — Step 8: measure RAG quality with numbers, not vibes.

Run (index sample.txt first if chroma_db is empty):
    source activate.sh
    python ingest.py
    python evaluate.py
    python evaluate.py --judge   # also run LLM-as-judge (uses API credits)

Two metrics (measure separately — core AI engineering skill):
  1. Retrieval hit rate  — did the right source appear in top-k?
  2. Answer keyword match — does the answer contain expected facts?

Optional: LLM-as-judge grades whether the answer is supported by context.
"""

import argparse
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from rag import ask, build_context, retrieve

load_dotenv(Path(__file__).resolve().parent / ".env")

# Golden test set — questions you know the answer to for docs/sample.txt
# Add more cases when you index your own PDFs.
TESTS = [
    {
        "question": "What are the four stages of the RAG pipeline?",
        "expected_source": "sample.txt",
        "expected_keyword": "embed",
    },
    {
        "question": "What does the embed stage do?",
        "expected_source": "sample.txt",
        "expected_keyword": "vector",
    },
    {
        "question": "Why do chunk size and overlap matter?",
        "expected_source": "sample.txt",
        "expected_keyword": "retrieval",
    },
    {
        "question": "What are the quarterly revenue numbers?",
        "expected_source": "sample.txt",
        "expected_keyword": "not contain",  # should refuse — no revenue in doc
    },
]


def retrieval_hit(question, expected_source, k=4):
    """True if expected_source appears in top-k retrieved chunks."""
    sources = {c["source"] for c in retrieve(question, k=k)}
    return expected_source in sources


def answer_keyword_hit(question, keyword, k=4):
    """True if expected keyword/phrase appears in the generated answer."""
    text, _ = ask(question, k=k)
    return keyword.lower() in text.lower()


def judge(question, answer_text, context_text):
    """
    LLM-as-judge: Claude grades if the answer is grounded in the context.

    Returns Claude's reply (starts with GOOD or BAD).
    """
    client = anthropic.Anthropic()
    prompt = (
        f"Question: {question}\n\n"
        f"Answer given: {answer_text}\n\n"
        f"Source context:\n{context_text}\n\n"
        "Is the answer fully supported by the context and does it correctly "
        "answer the question? Reply GOOD or BAD, then one sentence of reasoning."
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def evaluate(run_judge=False, k=4):
    retrieval_hits = 0
    answer_hits = 0
    judge_hits = 0

    print(f"Running {len(TESTS)} test(s)  (k={k})\n")

    for i, test in enumerate(TESTS, start=1):
        q = test["question"]
        print(f"--- Test {i}: {q}")

        ret_ok = retrieval_hit(q, test["expected_source"], k=k)
        retrieval_hits += int(ret_ok)
        print(f"  Retrieval: {'PASS' if ret_ok else 'FAIL'}  (expected source: {test['expected_source']})")

        text, chunks = ask(q, k=k)
        ans_ok = test["expected_keyword"].lower() in text.lower()
        answer_hits += int(ans_ok)
        print(f"  Answer:    {'PASS' if ans_ok else 'FAIL'}  (keyword: {test['expected_keyword']!r})")
        print(f"  Preview:   {text[:120].replace(chr(10), ' ')}...")

        if run_judge:
            context = build_context(chunks)
            verdict = judge(q, text, context)
            good = verdict.strip().upper().startswith("GOOD")
            judge_hits += int(good)
            print(f"  Judge:     {'PASS' if good else 'FAIL'}  ({verdict[:80]}...)")

        print()

    n = len(TESTS)
    print("=" * 50)
    print(f"Retrieval hit rate:   {retrieval_hits}/{n}  ({100 * retrieval_hits / n:.0f}%)")
    print(f"Answer keyword match: {answer_hits}/{n}  ({100 * answer_hits / n:.0f}%)")
    if run_judge:
        print(f"LLM-as-judge pass:    {judge_hits}/{n}  ({100 * judge_hits / n:.0f}%)")
    print("=" * 50)
    print("\nTip: change chunk_size in ingest.py or k here, re-run ingest + evaluate, compare numbers.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval and answer quality.")
    parser.add_argument(
        "--judge",
        action="store_true",
        help="Also run LLM-as-judge (extra API calls)",
    )
    parser.add_argument("--k", type=int, default=4, help="Top-k chunks to retrieve")
    args = parser.parse_args()
    evaluate(run_judge=args.judge, k=args.k)

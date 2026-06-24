"""
rag.py — Step 4: retrieve the most relevant chunks for a question.

Run (index first if chroma_db is empty):
    source activate.sh
    python ingest.py          # ensure sample.txt is indexed
    python rag.py             # retrieval checkpoint

This is the "R" in RAG — Retrieval.
Generation (Claude answering) comes in Step 5.
"""

from ingest import get_collection


def retrieve(query, k=4):
    """
    Find the k chunks whose embeddings are closest to the query.

    How it works:
      1. Chroma embeds your question with the same model used at index time
      2. Compares that vector to every stored chunk vector
      3. Returns the k nearest matches (text + metadata + distance)

    Args:
        query: Natural-language question, e.g. "What is RAG?"
        k:     How many chunks to return. Higher k = more context, more noise.

    Returns:
        List of dicts: text, source, page, distance (lower = more similar).
    """
    collection = get_collection()

    # query_texts: list of questions (we send one).
    # n_results: top-k nearest neighbors by vector distance.
    results = collection.query(query_texts=[query], n_results=k)

    chunks = []
    # results["documents"][0] — matches for the first (only) query
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


if __name__ == "__main__":
    # Questions we know sample.txt can answer — good retrieval should hit them
    test_queries = [
        "What are the four stages of the RAG pipeline?",
        "What is chunk size and overlap?",
        "How do quarterly revenue numbers look?",  # not in doc — may still return something
    ]

    for query in test_queries:
        print("=" * 60)
        print(f"Query: {query}\n")
        hits = retrieve(query, k=3)

        if not hits:
            print("No results — run `python ingest.py` first to index documents.\n")
            continue

        for i, h in enumerate(hits, 1):
            # page 0 means plain text file (no PDF pages)
            loc = h["source"]
            if h["page"]:
                loc += f" p.{h['page']}"
            print(f"--- Result {i}  (distance {h['distance']:.3f}, {loc}) ---")
            print(h["text"][:250].strip())
            if len(h["text"]) > 250:
                print("...")
            print()

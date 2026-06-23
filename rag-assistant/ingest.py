"""
ingest.py — Steps 1–2: load documents and split them into chunks.

Run:
    source activate.sh
    python ingest.py

Pipeline so far:
    load_file()   → [{text, source, page}, ...]     (Step 1)
    build_chunks() → [{text, source, page, chunk_id}, ...]  (Step 2)
"""

from pathlib import Path

from pypdf import PdfReader


# ---------------------------------------------------------------------------
# Step 1 — Load documents
# ---------------------------------------------------------------------------

def load_file(path, display_name=None):
    """
    Read a PDF or text file into a list of {text, source, page} records.

    PDFs → one record per page (non-blank).
    Text files → one record for the whole file (page is None).
    """
    path = Path(path)
    name = display_name or path.name
    records = []

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                records.append({
                    "text": text,
                    "source": name,
                    "page": page_num,
                })
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")
        records.append({
            "text": text,
            "source": name,
            "page": None,
        })

    return records


# ---------------------------------------------------------------------------
# Step 2 — Chunk the text
# ---------------------------------------------------------------------------

def chunk_text(text, chunk_size=800, overlap=150):
    """
    Split a long string into overlapping chunks of ~chunk_size characters.

    Why not feed the whole document to the model?
      - Context window is limited (can't fit a 200-page PDF)
      - Embeddings work best on focused passages, not entire books
      - Retrieval returns only the relevant pieces → precise, citable answers

    Two knobs:
      chunk_size — how big each piece is (default 800 chars ≈ ~200 tokens)
      overlap    — shared text between neighbors so ideas split at a boundary
                   aren't lost (default 150 chars)

    Tokenization note: models count tokens, not characters. Rough rule for
    English: 4 characters ≈ 1 token. So 800 chars ≈ 200 tokens.
    """
    chunks = []
    start = 0
    while start < len(text):
        # Slice [start : start + chunk_size], strip whitespace at edges
        piece = text[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        # Advance by (chunk_size - overlap) so the next chunk reuses `overlap`
        # characters from the end of this one
        start += chunk_size - overlap
    return chunks


def build_chunks(records, chunk_size=800, overlap=150):
    """
    Turn loaded records into chunk records that remember their source.

    Each output dict:
      text     — the chunk content (what gets embedded and retrieved)
      source   — filename for citations
      page     — page number (None for plain text files)
      chunk_id — unique ID for storage in the vector DB later
    """
    all_chunks = []
    for rec in records:
        pieces = chunk_text(rec["text"], chunk_size, overlap)
        page_label = rec["page"] if rec["page"] is not None else 0
        for i, piece in enumerate(pieces):
            all_chunks.append({
                "text": piece,
                "source": rec["source"],
                "page": rec["page"],
                "chunk_id": f'{rec["source"]}-p{page_label}-{i}',
            })
    return all_chunks


if __name__ == "__main__":
    sample = Path(__file__).resolve().parent / "docs" / "sample.txt"

    # Step 1 — load
    records = load_file(sample)
    print(f"Step 1: loaded {len(records)} record(s) from {sample.name}\n")

    # Step 2 — chunk (default size)
    chunks = build_chunks(records)
    print(f"Step 2: created {len(chunks)} chunk(s)  (chunk_size=800, overlap=150)")
    print("First chunk:")
    print(chunks[0])
    print()

    # Context engineering experiment — smaller chunks = more pieces
    small = build_chunks(records, chunk_size=400, overlap=80)
    large = build_chunks(records, chunk_size=1200, overlap=150)
    print("Chunk count vs size (same document):")
    print(f"  chunk_size=400  → {len(small)} chunks")
    print(f"  chunk_size=800  → {len(chunks)} chunks")
    print(f"  chunk_size=1200 → {len(large)} chunks")

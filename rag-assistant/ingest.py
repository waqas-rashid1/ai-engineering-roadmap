"""
ingest.py — Steps 1–3: load, chunk, embed, and store in Chroma.

Run:
    source activate.sh
    python ingest.py              # full pipeline checkpoint
    python embeddings_demo.py     # optional: see how embeddings work

Pipeline:
    load_file()    → records
    build_chunks() → chunks with chunk_id
    index_chunks() → vectors stored in ./chroma_db
    ingest_file()  → load → chunk → index (one call)
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

# Project root — chroma_db lives next to this file
_ROOT = Path(__file__).resolve().parent
_CHROMA_PATH = _ROOT / "chroma_db"

# Persistent vector DB on disk (survives restarts)
_client = chromadb.PersistentClient(path=str(_CHROMA_PATH))

# Same model as embeddings_demo.py — Chroma calls it on upsert and query
_embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_collection():
    """Single place that defines our collection + embedding model."""
    return _client.get_or_create_collection(
        name="documents",
        embedding_function=_embed_fn,
    )


# ---------------------------------------------------------------------------
# Step 1 — Load documents
# ---------------------------------------------------------------------------

def load_file(path, display_name=None):
    """Read PDF or text into [{text, source, page}, ...]."""
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
    """Split text into overlapping chunks (~800 chars ≈ 200 tokens each)."""
    chunks = []
    start = 0
    while start < len(text):
        piece = text[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        start += chunk_size - overlap
    return chunks


def build_chunks(records, chunk_size=800, overlap=150):
    """Records → chunks with text, source, page, chunk_id."""
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


# ---------------------------------------------------------------------------
# Step 3 — Embed and store in Chroma
# ---------------------------------------------------------------------------

def index_chunks(chunks):
    """
    Embed each chunk and store in Chroma.

    Chroma + embedding_function handles vectors for you:
      - on upsert: text → embedding → stored
      - on query (Step 4): question → embedding → nearest neighbors

    upsert (not add) updates existing chunk_ids without duplicate errors.
    """
    collection = get_collection()
    collection.upsert(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "source": c["source"],
                # Chroma metadata must be str/int/float/bool — not None
                "page": c["page"] if c["page"] is not None else 0,
            }
            for c in chunks
        ],
    )
    return collection.count()


def ingest_file(path, display_name=None, chunk_size=800, overlap=150):
    """Full pipeline: load → chunk → embed → store."""
    records = load_file(path, display_name=display_name)
    chunks = build_chunks(records, chunk_size, overlap)
    total = index_chunks(chunks)
    return len(chunks), total


if __name__ == "__main__":
    sample = _ROOT / "docs" / "sample.txt"

    print("Step 3: ingest → embed → store in Chroma\n")
    added, total = ingest_file(sample)

    print(f"Indexed {added} chunk(s) from {sample.name}")
    print(f"Collection now holds {total} chunk(s) total")
    print(f"Vector DB folder: {_CHROMA_PATH}")
    print(f"chroma_db exists: {_CHROMA_PATH.is_dir()}")

    # Quick sanity check — collection is readable
    col = get_collection()
    peek = col.get(limit=1, include=["documents", "metadatas"])
    if peek["ids"]:
        print(f"\nStored example id: {peek['ids'][0]}")
        print(f"Metadata: {peek['metadatas'][0]}")
        print(f"Text preview: {peek['documents'][0][:120]}...")

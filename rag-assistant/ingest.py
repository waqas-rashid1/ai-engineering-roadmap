"""
ingest.py — Step 1: load documents into plain text with source tracking.

Run:
    source venv/bin/activate
    pip install pypdf
    python ingest.py

What this file does:
    Reads PDF or text files and returns a list of records.
    Each record has: text, source (filename), page (number or None).
    That metadata is what lets the app cite "sample.txt, page 2" later.
"""

from pathlib import Path

# pypdf extracts text from PDF files page by page.
# Models can't read binary PDFs — we turn them into strings first.
from pypdf import PdfReader


def load_file(path, display_name=None):
    """
    Read a PDF or text file into a list of {text, source, page} records.

    Args:
        path: Path to a .pdf, .txt, .md, etc.
        display_name: Optional friendly name (e.g. original upload filename
                      when the file is stored under a temp path in the UI).

    Returns:
        List of dicts, one per page (PDF) or one per file (plain text).
    """
    path = Path(path)
    # Use display_name when the UI saves uploads with random temp names
    # but we still want citations to show the user's filename.
    name = display_name or path.name
    records = []

    if path.suffix.lower() == ".pdf":
        # --- PDF path ---
        # PdfReader opens the file; .pages is every page object.
        reader = PdfReader(str(path))
        for page_num, page in enumerate(reader.pages, start=1):
            # extract_text() pulls selectable text from the page.
            # Scanned PDFs (images only) often return "" — OCR is out of scope.
            text = page.extract_text() or ""
            if text.strip():  # skip blank / image-only pages
                records.append({
                    "text": text,
                    "source": name,
                    "page": page_num,
                })
    else:
        # --- Plain text path (.txt, .md, ...) ---
        # read_text loads the whole file as one string.
        # errors="ignore" skips bytes that aren't valid UTF-8 instead of crashing.
        text = path.read_text(encoding="utf-8", errors="ignore")
        records.append({
            "text": text,
            "source": name,
            "page": None,  # no pages in a .txt file
        })

    return records


if __name__ == "__main__":
    # Step 1 checkpoint — load sample.txt and print a preview
    sample = Path(__file__).resolve().parent / "docs" / "sample.txt"
    records = load_file(sample)

    print(f"Loaded {len(records)} record(s) from {sample.name}")
    print("-" * 50)
    print("First record keys:", list(records[0].keys()))
    print("Source:", records[0]["source"])
    print("Page:", records[0]["page"])
    print("-" * 50)
    print("Text preview (first 300 chars):")
    print(records[0]["text"][:300])

"""
embeddings_demo.py — Step 3 intuition: what embeddings are and why they work.

Run once:
    source activate.sh
    python embeddings_demo.py

First run downloads the embedding model (~80 MB) — cached after that.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2: small, fast, free, runs locally.
# Turns any sentence into a vector of 384 numbers that capture meaning.
model = SentenceTransformer("all-MiniLM-L6-v2")

a = model.encode("The cat sat on the mat.")
b = model.encode("A kitten rested on the rug.")
c = model.encode("Quarterly revenue grew 12%.")

# Cosine similarity: 1.0 = identical direction, 0 = unrelated
cos = lambda x, y: float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))

print("vector length:", len(a), "numbers per sentence")
print("cat vs kitten:", round(cos(a, b), 3), "  ← HIGH (similar meaning, different words)")
print("cat vs revenue:", round(cos(a, c), 3), " ← LOW  (unrelated topics)")

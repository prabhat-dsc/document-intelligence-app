"""
Simple retrieval evaluation scaffold.

Populate golden_dataset.json with verified questions/pages before
using this as a real quality gate.
"""
import json
from pathlib import Path

def recall_at_k(expected_pages, retrieved_docs, k=5):
    retrieved_pages = {
        d.metadata.get("page")
        for d in retrieved_docs[:k]
    }
    return int(bool(set(expected_pages) & retrieved_pages))

if __name__ == "__main__":
    path = Path(__file__).parent / "golden_dataset.json"
    dataset = json.loads(path.read_text())
    print(f"Loaded {len(dataset)} evaluation cases.")
    print("Add your retrieval loop here after indexing the evaluation documents.")

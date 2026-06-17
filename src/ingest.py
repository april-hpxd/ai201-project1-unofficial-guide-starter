"""
ingest.py
Reads all .txt files from the data/ directory and returns a list of dicts:
  [{"source": "filename.txt", "text": "full content"}, ...]
"""

import os


def load_documents(data_dir: str = "data") -> list[dict]:
    documents = []
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if text:
                documents.append({"source": filename, "text": text})
                print(f"  Loaded: {filename} ({len(text)} chars)")
    return documents
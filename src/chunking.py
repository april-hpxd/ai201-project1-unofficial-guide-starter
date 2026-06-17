"""
chunking.py
Splits document text into overlapping character-window chunks.

Chunk size: 800 characters
Overlap:    150 characters

Why these numbers for this corpus:
- Documents are medium-length guides (4,000–7,000 chars each)
- Key facts (prices, rules, tips) tend to sit in 2–4 sentence bursts
- 800 chars (~120–140 words) captures a full idea without pulling in noise
- 150-char overlap ensures a fact at a boundary appears in both neighbors
"""


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Takes output of ingest.load_documents() and returns a flat list of chunk dicts:
      [{"source": "filename.txt", "text": "chunk text", "chunk_id": "filename_0"}, ...]
    """
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": f"{doc['source'].replace('.txt', '')}_{i}",
                "text": chunk,
            })
    return all_chunks
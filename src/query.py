"""
query.py
Orchestrates the full RAG query pipeline:
  question → retrieve top-k chunks → generate grounded answer
"""

from src.retrieve import retrieve
from src.generate import generate_answer


def ask(question: str, top_k: int = 5) -> dict:
    """
    Returns a dict with:
      - answer: str
      - sources: list of source filenames used
      - chunks: the raw retrieved chunks (for debugging/evaluation)
    """
    chunks = retrieve(question, top_k=top_k)
    answer = generate_answer(question, chunks)
    sources = sorted(set(c["source"] for c in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }
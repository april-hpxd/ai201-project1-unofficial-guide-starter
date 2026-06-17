"""
retrieve.py
Embeds a query and retrieves the top-k most semantically similar chunks
from ChromaDB using cosine similarity.
"""

from sentence_transformers import SentenceTransformer
from src.embed import get_collection, MODEL_NAME

_model = None  # lazy singleton so we don't reload the model on every query


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Returns a list of top_k dicts:
      [{"text": "...", "source": "...", "distance": float}, ...]
    Sorted by relevance (lowest cosine distance = most relevant).
    """
    model = _get_model()
    query_embedding = model.encode(query, convert_to_list=True)

    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": metadata.get("source", "unknown"),
            "distance": round(distance, 4),
        })
    return chunks
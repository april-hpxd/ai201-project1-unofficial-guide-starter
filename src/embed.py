"""
embed.py
Embeds text chunks using sentence-transformers and stores them in a
persistent local ChromaDB collection.

Model: all-MiniLM-L6-v2
- 384-dimensional embeddings
- Fast, lightweight, strong semantic similarity on English text
- Well-suited for short-to-medium passages like student tips and guides
"""

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "nyc_student_guide"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def embed_and_store(chunks: list[dict]):
    print(f"  Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    collection = get_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    print(f"  Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_list=True)

    # Upsert in batches of 500 to stay safe on memory
    batch_size = 500
    for i in range(0, len(texts), batch_size):
        collection.upsert(
            ids=ids[i:i+batch_size],
            documents=texts[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
        )
    print(f"  Stored {len(texts)} chunks in ChromaDB collection '{COLLECTION_NAME}'")
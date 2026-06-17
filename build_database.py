"""
build_database.py
Run this ONCE to ingest documents, chunk them, embed them, and load
everything into the local ChromaDB vector store.

Re-run it whenever you add new documents or change chunking settings.
(It upserts, so re-running is safe — it won't duplicate entries.)
"""

from dotenv import load_dotenv
load_dotenv()

from src.ingest import load_documents
from src.chunking import chunk_documents
from src.embed import embed_and_store


def main():
    print("\n=== Step 1: Loading documents ===")
    documents = load_documents("data")
    print(f"  Total documents loaded: {len(documents)}")

    print("\n=== Step 2: Chunking ===")
    chunks = chunk_documents(documents)
    print(f"  Total chunks created: {len(chunks)}")

    print("\n=== Step 3: Embedding + storing in ChromaDB ===")
    embed_and_store(chunks)

    print("\n✅ Database build complete.")
    print(f"   {len(documents)} documents → {len(chunks)} chunks stored in chroma_db/")


if __name__ == "__main__":
    main()
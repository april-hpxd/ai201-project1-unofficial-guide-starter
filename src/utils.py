"""
utils.py
Shared utility helpers for the pipeline.
"""

import os


def check_env():
    """Raises a clear error if GROQ_API_KEY is missing."""
    key = os.environ.get("GROQ_API_KEY")
    if not key or key.startswith("your_") or len(key) < 10:
        raise EnvironmentError(
            "GROQ_API_KEY is not set or looks like a placeholder.\n"
            "Copy .env.example to .env and add your real Groq API key.\n"
            "Get a free key at: https://console.groq.com"
        )


def print_chunks(chunks: list[dict]):
    """Pretty-prints retrieved chunks for debugging."""
    for i, c in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} | source: {c['source']} | distance: {c['distance']} ---")
        print(c["text"][:300] + ("..." if len(c["text"]) > 300 else ""))
"""
generate.py
Sends the retrieved context chunks + user question to Groq and returns
a grounded answer. The system prompt strictly limits the model to the
provided documents — it cannot draw on general training knowledge.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a helpful assistant for The Unofficial NYC Student Guide.
Answer ONLY using the information in the CONTEXT sections provided below.
Do NOT use any outside knowledge, even if you know the answer.
If the answer is not contained in the context, respond with EXACTLY:
  "I don't have enough information in the documents to answer that."
Always cite the source filenames at the end of your answer using this format:
  Sources: [filename1.txt, filename2.txt]"""


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "I don't have enough information in the documents to answer that."

    # Build context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Context {i} — Source: {chunk['source']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)

    user_message = f"""CONTEXT:

{context}

---

Question: {question}

Answer based only on the CONTEXT above."""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()
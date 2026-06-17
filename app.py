"""
app.py
Streamlit chat interface for the NYC Student Unofficial Guide RAG system.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv
from src.utils import check_env
from src.query import ask

load_dotenv()
check_env()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NYC Student Unofficial Guide",
    page_icon="🗽",
    layout="centered",
)

st.title("🗽 NYC Student Unofficial Guide")
st.caption(
    "Ask anything about student life in NYC — food, transit, housing, budgeting, "
    "safety, campus hacks, and more. Answers come only from curated student-sourced documents."
)

# ── Example questions ─────────────────────────────────────────────────────────
with st.expander("💡 Example questions to try"):
    st.markdown("""
- What's the cheapest way to eat in NYC as a student?
- How does the OMNY weekly bonus cap work?
- What neighborhoods are affordable for students with roommates?
- As an F-1 student, can I work off campus?
- What should I watch out for safety-wise in the subway late at night?
- How much should I budget per month living off campus in NYC?
- What free things are there to do in NYC as a student?
""")

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"📄 Sources: {', '.join(msg['sources'])}")

# ── Input ─────────────────────────────────────────────────────────────────────
if question := st.chat_input("Ask a question about student life in NYC..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            result = ask(question, top_k=5)

        st.markdown(result["answer"])

        if result["sources"]:
            st.caption(f"📄 Sources: {', '.join(result['sources'])}")

        # Optional: show retrieved chunks in an expander for transparency
        with st.expander("🔍 View retrieved chunks"):
            for i, chunk in enumerate(result["chunks"], 1):
                st.markdown(f"**Chunk {i}** — `{chunk['source']}` (distance: {chunk['distance']})")
                st.text(chunk["text"][:400] + ("..." if len(chunk["text"]) > 400 else ""))

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
    })
"""
app.py — Step 7: Streamlit chat UI (upload + ask + citations + memory).

Run:
    source activate.sh
    streamlit run app.py

Streamlit reruns this entire script on every click/keypress.
Anything that must persist (chat messages) lives in st.session_state.
"""

import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from ingest import get_collection, ingest_file
from rag import ask

load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(page_title="Talk to Documents", page_icon="📄")
st.title("Talk to Documents")
st.caption("Upload documents, ask questions, get cited answers.")

# ---------------------------------------------------------------------------
# Session state — survives Streamlit reruns (our "memory" for the UI session)
# Each message: {role: "user"|"assistant", content: str, sources?: list}
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


def format_location(source_chunk):
    """Citation line: filename and optional page."""
    loc = source_chunk["source"]
    if source_chunk.get("page"):
        loc += f", p.{source_chunk['page']}"
    return loc


# --- Sidebar: upload and index ---
with st.sidebar:
    st.header("Your documents")
    uploaded = st.file_uploader(
        "Upload PDFs or text files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )

    if st.button("Index documents", type="primary") and uploaded:
        with st.spinner("Reading, chunking, and embedding..."):
            total_chunks = 0
            for f in uploaded:
                # Streamlit gives bytes in memory; ingest_file expects a file path
                suffix = os.path.splitext(f.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(f.getvalue())
                    tmp_path = tmp.name
                try:
                    # display_name keeps the real filename in citations
                    added, _ = ingest_file(tmp_path, display_name=f.name)
                    total_chunks += added
                finally:
                    os.unlink(tmp_path)
        st.success(f"Indexed {total_chunks} chunk(s) from {len(uploaded)} file(s).")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    try:
        count = get_collection().count()
        st.caption(f"{count} chunk(s) in the vector database.")
    except Exception:
        st.caption("No documents indexed yet.")


# --- Render conversation history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for i, chunk in enumerate(message["sources"], 1):
                    st.markdown(f"**[{i}]** {format_location(chunk)}")


# --- New user message ---
if prompt := st.chat_input("Ask a question about your documents"):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build lean history: prior turns only (plain Q/A, no sources blob)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and thinking..."):
            try:
                text, sources = ask(prompt, history=history, k=4)
            except Exception as e:
                text = f"Error: {e}"
                sources = []

        st.markdown(text)
        if sources:
            with st.expander("Sources"):
                for i, chunk in enumerate(sources, 1):
                    st.markdown(f"**[{i}]** {format_location(chunk)}")
                    st.caption(chunk["text"][:200] + ("..." if len(chunk["text"]) > 200 else ""))

    st.session_state.messages.append(
        {"role": "assistant", "content": text, "sources": sources}
    )

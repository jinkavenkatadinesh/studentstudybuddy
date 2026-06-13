"""Ask Your Documents — Chat page with RAG."""

import streamlit as st
from models.schemas import ChatMessage
from components.chat import render_chat_history, render_sources


def render_chat():
    """Render the document Q&A chat page."""
    st.markdown("### 💬 Ask Your Documents")
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1rem;">Chat with your study materials using AI. Ask questions and get answers with source citations.</div>',
        unsafe_allow_html=True,
    )

    rag = st.session_state.get("rag_pipeline")
    vector_store = st.session_state.get("vector_store")

    # Check if there are documents
    if not vector_store or vector_store.total_vectors == 0:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">💬</div>'
            '<div class="empty-state-text">Upload documents first to start chatting with them!</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("📤 Upload Documents", type="primary"):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    # Chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Clear chat button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear", key="clear_chat", help="Clear chat history"):
            st.session_state.chat_messages = []
            st.rerun()

    # Display chat history
    render_chat_history(st.session_state.chat_messages)

    # Chat input
    question = st.chat_input("Ask a question about your documents...", key="chat_input")

    if question and rag:
        # Add user message
        user_msg = ChatMessage(role="user", content=question)
        st.session_state.chat_messages.append(user_msg)

        # Generate response
        model = st.session_state.get("selected_model", "qwen3:8b")
        temp = st.session_state.get("temperature", 0.7)

        with st.spinner("Thinking..."):
            try:
                answer, sources = rag.ask(question, model=model, temperature=temp)
                assistant_msg = ChatMessage(role="assistant", content=answer, sources=sources)
                st.session_state.chat_messages.append(assistant_msg)
            except Exception as e:
                error_msg = ChatMessage(role="assistant", content=f"⚠️ Error: {e}")
                st.session_state.chat_messages.append(error_msg)

        st.rerun()

    # Document context indicator
    if vector_store:
        doc_count = len(vector_store.document_ids)
        vec_count = vector_store.total_vectors
        st.caption(f"📚 Searching across {doc_count} document(s) ({vec_count} chunks)")

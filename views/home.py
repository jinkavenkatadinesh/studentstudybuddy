"""Home Dashboard page."""

import streamlit as st

from components.metrics import render_metric_card
from utils.helpers import format_file_size, format_timestamp


def render_home():
    """Render the home dashboard page."""
    # Welcome section
    st.markdown(
        """
    <div style="text-align:center;margin:0.5rem 0 2rem;">
        <div style="font-size:1.4rem;font-weight:700;color:#E2E8F0;">Welcome to Your Study Dashboard</div>
        <div style="font-size:1rem;color:#94A3B8;margin-top:0.3rem;">
            Upload materials, generate quizzes, create flashcards, and learn smarter with AI
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Stats row
    stats = st.session_state.get("analytics_stats", None)
    cols = st.columns(4)
    metrics = [
        ("📄", "Documents", stats.documents_uploaded if stats else 0),
        ("🧪", "Quizzes Taken", stats.quizzes_completed if stats else 0),
        ("📊", "Avg Score", f"{stats.avg_score:.0f}%" if stats else "0%"),
        ("🃏", "Flashcards", stats.flashcards_generated if stats else 0),
    ]
    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            render_metric_card(icon, label, value)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI Model Status
    ollama_ok = st.session_state.get("ollama_available", False)
    model = st.session_state.get("selected_model", "")
    if ollama_ok:
        st.markdown(
            f'<div class="glass-card" style="display:flex;align-items:center;gap:1rem;">'
            f'<div class="status-online"><span class="status-dot online"></span> AI Online</div>'
            f'<span style="color:#94A3B8;">Model: <strong style="color:#C4B5FD;">{model}</strong></span>'
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="glass-card" style="display:flex;align-items:center;gap:1rem;">'
            '<div class="status-offline"><span class="status-dot offline"></span> AI Offline</div>'
            '<span style="color:#94A3B8;">Start Ollama to enable AI features</span>'
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    actions = [
        (c1, "📤", "Upload", "upload", "Upload study materials"),
        (c2, "🧪", "Quiz", "quiz", "Test your knowledge"),
        (c3, "💬", "Chat", "chat", "Ask your documents"),
        (c4, "🃏", "Flashcards", "flashcards", "Create study cards"),
    ]
    for col, icon, title, page, desc in actions:
        with col:
            st.markdown(
                f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            if st.button(f"Go to {title}", key=f"qa_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent Documents
    file_mgr = st.session_state.get("file_manager")
    if file_mgr:
        docs = file_mgr.list_documents()[:5]
        if docs:
            st.markdown("### 📄 Recent Documents")
            for doc in docs:
                type_icons = {"pdf": "📕", "docx": "📘", "txt": "📄"}
                icon = type_icons.get(doc.file_type, "📄")
                st.markdown(
                    f"""
                <div class="doc-card">
                    <div class="doc-name">{icon} {doc.filename}</div>
                    <div class="doc-meta">
                        {format_file_size(doc.file_size)} · {doc.num_chunks} chunks · {format_timestamp(doc.upload_time)}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

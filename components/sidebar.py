"""Sidebar component — navigation, model config, and status."""

import streamlit as st
from config import PAGES, AVAILABLE_MODELS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, MIN_TEMPERATURE, MAX_TEMPERATURE


def render_sidebar():
    """Render the sidebar with navigation and AI configuration."""
    with st.sidebar:
        # ── Navigation ────────────────────────────────────
        st.markdown('<div class="sidebar-section">📌 Navigation</div>', unsafe_allow_html=True)

        current_page = st.session_state.get("current_page", "home")
        for page_key, page_info in PAGES.items():
            label = f"{page_info['icon']} {page_info['label']}"
            is_active = current_page == page_key
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── AI Model Config ───────────────────────────────
        st.markdown('<div class="sidebar-section">🤖 AI Model</div>', unsafe_allow_html=True)

        # Ollama status
        ollama_ok = st.session_state.get("ollama_available", False)
        if ollama_ok:
            st.markdown(
                '<div class="status-online"><span class="status-dot online"></span> Ollama Connected</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-offline"><span class="status-dot offline"></span> Ollama Offline</div>',
                unsafe_allow_html=True,
            )

        # Model selector — combine available + default models
        available = st.session_state.get("ollama_models", [])
        all_models = list(dict.fromkeys(available + AVAILABLE_MODELS))
        current_model = st.session_state.get("selected_model", DEFAULT_MODEL)
        if current_model not in all_models:
            all_models.insert(0, current_model)
        idx = all_models.index(current_model) if current_model in all_models else 0

        selected = st.selectbox(
            "Model",
            all_models,
            index=idx,
            key="model_selector",
            label_visibility="collapsed",
        )
        st.session_state.selected_model = selected

        # Temperature
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=MIN_TEMPERATURE,
            max_value=MAX_TEMPERATURE,
            value=st.session_state.get("temperature", DEFAULT_TEMPERATURE),
            step=0.1,
            key="temp_slider",
            help="Lower = more focused, Higher = more creative",
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── Stats summary ─────────────────────────────────
        st.markdown('<div class="sidebar-section">📊 Quick Stats</div>', unsafe_allow_html=True)

        stats = st.session_state.get("analytics_stats", None)
        if stats:
            st.caption(f"📄 {stats.documents_uploaded} documents")
            st.caption(f"🧪 {stats.quizzes_completed} quizzes")
            st.caption(f"🃏 {stats.flashcards_generated} flashcards")
            st.caption(f"📝 {stats.summaries_generated} summaries")
        else:
            st.caption("No stats yet — start learning!")

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # Footer
        st.markdown(
            '<div style="text-align:center;color:#64748B;font-size:0.75rem;padding-top:0.5rem;">'
            'Student Study Buddy v1.0<br>Powered by Ollama & LangChain'
            '</div>',
            unsafe_allow_html=True,
        )

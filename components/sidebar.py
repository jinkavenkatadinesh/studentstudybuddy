"""Sidebar component — navigation, model config, and status."""

import streamlit as st

from config import AVAILABLE_MODELS, DEFAULT_TEMPERATURE, MAX_TEMPERATURE, MIN_TEMPERATURE, PAGES


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

        # Provider Selector
        provider_map = {"Local (Ollama)": "ollama", "OpenAI": "openai", "Google Gemini": "gemini"}
        current_provider = st.session_state.get("ai_provider", "ollama")
        provider_list = list(provider_map.keys())
        default_provider_idx = list(provider_map.values()).index(current_provider)

        selected_provider_label = st.selectbox(
            "AI Provider", provider_list, index=default_provider_idx, key="provider_select"
        )
        selected_provider = provider_map[selected_provider_label]

        if selected_provider != current_provider:
            st.session_state.ai_provider = selected_provider
            # Reset active model based on the new provider
            if selected_provider == "ollama":
                available = st.session_state.get("ollama_models", [])
                from config import DEFAULT_MODEL

                if available and DEFAULT_MODEL not in available:
                    st.session_state.selected_model = available[0]
                else:
                    st.session_state.selected_model = DEFAULT_MODEL
            elif selected_provider == "openai":
                from config import OPENAI_MODELS

                st.session_state.selected_model = OPENAI_MODELS[0]
            elif selected_provider == "gemini":
                from config import GEMINI_MODELS

                st.session_state.selected_model = GEMINI_MODELS[0]
            st.rerun()

        # Conditional API Key Inputs & Provider Status
        if selected_provider == "ollama":
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
        elif selected_provider == "openai":
            openai_key = st.text_input(
                "OpenAI API Key",
                value=st.session_state.get("openai_api_key", ""),
                type="password",
                placeholder="sk-...",
                help="Your OpenAI API Key will not be stored permanently.",
            )
            st.session_state.openai_api_key = openai_key
            if openai_key:
                st.markdown(
                    '<div class="status-online"><span class="status-dot online"></span> Key Configured</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="status-offline"><span class="status-dot offline"></span> Key Missing</div>',
                    unsafe_allow_html=True,
                )
        elif selected_provider == "gemini":
            gemini_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.get("gemini_api_key", ""),
                type="password",
                placeholder="AIzaSy...",
                help="Your Gemini API Key will not be stored permanently.",
            )
            st.session_state.gemini_api_key = gemini_key
            if gemini_key:
                st.markdown(
                    '<div class="status-online"><span class="status-dot online"></span> Key Configured</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="status-offline"><span class="status-dot offline"></span> Key Missing</div>',
                    unsafe_allow_html=True,
                )

        # Dynamic Model List based on selected provider
        all_models = []
        if selected_provider == "ollama":
            available = st.session_state.get("ollama_models", [])
            all_models = list(dict.fromkeys(available + AVAILABLE_MODELS))
        elif selected_provider == "openai":
            from config import OPENAI_MODELS

            all_models = OPENAI_MODELS
        elif selected_provider == "gemini":
            from config import GEMINI_MODELS

            all_models = GEMINI_MODELS

        current_model = st.session_state.get("selected_model")
        if not current_model or current_model not in all_models:
            current_model = all_models[0] if all_models else ""
            st.session_state.selected_model = current_model

        idx = all_models.index(current_model) if (current_model in all_models) else 0

        selected = st.selectbox(
            "Model",
            all_models,
            index=idx,
            key="model_selector",
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
            "Student Study Buddy v1.0<br>Powered by Ollama & LangChain"
            "</div>",
            unsafe_allow_html=True,
        )

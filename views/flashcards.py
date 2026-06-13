"""Flashcards Generator page."""

import streamlit as st

from components.flashcard import render_flashcard_set
from config import DEFAULT_NUM_FLASHCARDS, DIFFICULTY_LEVELS, MAX_NUM_FLASHCARDS, MIN_NUM_FLASHCARDS


def render_flashcards():
    """Render the flashcards generator page."""
    st.markdown("### 🃏 Flashcard Generator")
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1.5rem;">Create AI-powered study flashcards from your documents.</div>',
        unsafe_allow_html=True,
    )

    file_mgr = st.session_state.get("file_manager")
    flashcard_gen = st.session_state.get("flashcard_generator")
    analytics = st.session_state.get("analytics_tracker")

    if not file_mgr:
        st.error("System not ready.")
        return

    docs = file_mgr.list_documents()
    if not docs:
        st.info("📤 Upload documents first to generate flashcards.")
        return

    # Configuration
    doc_options = {f"{d.filename} ({d.file_type.upper()})": d.id for d in docs}
    selected_label = st.selectbox("Select Document", list(doc_options.keys()), key="fc_doc")
    doc_id = doc_options[selected_label]

    col1, col2 = st.columns(2)
    with col1:
        num_cards = st.slider(
            "Number of Cards", MIN_NUM_FLASHCARDS, MAX_NUM_FLASHCARDS, DEFAULT_NUM_FLASHCARDS, key="fc_num"
        )
    with col2:
        difficulty = st.select_slider("Difficulty", DIFFICULTY_LEVELS, value="medium", key="fc_diff")

    # Generate
    if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
        if not flashcard_gen:
            st.error("AI service not available. Is Ollama running?")
            return

        with st.spinner(f"Generating {num_cards} flashcards..."):
            try:
                model = st.session_state.get("selected_model", "qwen3:8b")
                temp = st.session_state.get("temperature", 0.7)
                fc_set = flashcard_gen.generate(doc_id, num_cards, difficulty, model=model, temperature=temp)
                st.session_state.current_flashcards = fc_set
                st.session_state.fc_current = 0
                st.session_state.fc_flipped = False
                if analytics:
                    analytics.track_flashcards(len(fc_set.cards))
                st.rerun()
            except Exception as e:
                st.error(f"Failed to generate flashcards: {e}")
                return

    # Display flashcards
    fc_set = st.session_state.get("current_flashcards")
    if fc_set:
        st.markdown("---")
        render_flashcard_set(fc_set)

        # Export
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📥 Export Flashcards")
        col1, col2 = st.columns(2)
        with col1:
            json_data = flashcard_gen.export_json(fc_set) if flashcard_gen else "[]"
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name="flashcards.json",
                mime="application/json",
                use_container_width=True,
            )
        with col2:
            csv_data = flashcard_gen.export_csv(fc_set) if flashcard_gen else ""
            st.download_button(
                "Download CSV", data=csv_data, file_name="flashcards.csv", mime="text/csv", use_container_width=True
            )

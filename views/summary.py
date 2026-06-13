"""AI Summary page."""

import streamlit as st
from config import SUMMARY_TYPES


def render_summary():
    """Render the AI summary page."""
    st.markdown("### 📝 AI Summary Generator")
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1.5rem;">Generate AI-powered summaries of your study materials.</div>',
        unsafe_allow_html=True,
    )

    file_mgr = st.session_state.get("file_manager")
    summary_gen = st.session_state.get("summary_generator")
    analytics = st.session_state.get("analytics_tracker")

    if not file_mgr:
        st.error("System not ready.")
        return

    docs = file_mgr.list_documents()
    if not docs:
        st.info("📤 Upload documents first to generate summaries.")
        return

    # Document selector
    doc_options = {f"{d.filename} ({d.file_type.upper()})": d.id for d in docs}
    selected_label = st.selectbox("Select Document", list(doc_options.keys()), key="summary_doc")
    doc_id = doc_options[selected_label]

    # Summary type
    col1, col2 = st.columns(2)
    with col1:
        type_labels = {"short": "📋 Short Summary", "detailed": "📖 Detailed Summary", "bullet": "📌 Bullet Points", "chapter": "📑 Chapter-wise"}
        summary_type = st.selectbox("Summary Type", SUMMARY_TYPES, format_func=lambda x: type_labels.get(x, x), key="summary_type")
    with col2:
        model = st.session_state.get("selected_model", "qwen3:8b")
        temp = st.session_state.get("temperature", 0.7)

    # Generate button
    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        if not summary_gen:
            st.error("AI service not available. Is Ollama running?")
            return

        with st.spinner(f"Generating {summary_type} summary..."):
            try:
                summary = summary_gen.generate(doc_id, summary_type, model=model, temperature=temp)
                st.session_state.last_summary = summary
                if analytics:
                    analytics.track_summary()
            except Exception as e:
                st.error(f"Failed to generate summary: {e}")
                return

    # Display summary
    summary = st.session_state.get("last_summary")
    if summary:
        st.markdown("---")
        st.markdown("#### Generated Summary")
        st.markdown(summary.content)

        # Download
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download as TXT",
                data=summary.content,
                file_name=f"summary_{summary.summary_type}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col2:
            if st.button("📋 Copy to Clipboard", key="copy_summary", use_container_width=True):
                st.code(summary.content, language=None)
                st.success("Summary displayed above — copy from there!")

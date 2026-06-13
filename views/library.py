"""Document Library page."""

import streamlit as st
from utils.helpers import format_file_size, format_timestamp


def render_library():
    """Render the document library page."""
    st.markdown("### 📚 Document Library")

    file_mgr = st.session_state.get("file_manager")
    vector_store = st.session_state.get("vector_store")
    if not file_mgr:
        st.error("System not ready.")
        return

    docs = file_mgr.list_documents()
    if not docs:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">📚</div>'
            '<div class="empty-state-text">No documents yet. Upload study materials to get started!</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("📤 Upload Documents", type="primary"):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search documents", key="lib_search", placeholder="Search by filename...", label_visibility="collapsed")
    with col2:
        filter_type = st.selectbox("Filter", ["All", "PDF", "DOCX", "TXT"], key="lib_filter", label_visibility="collapsed")

    # Filter documents
    filtered = docs
    if search:
        filtered = [d for d in filtered if search.lower() in d.filename.lower()]
    if filter_type != "All":
        filtered = [d for d in filtered if d.file_type == filter_type.lower()]

    st.caption(f"Showing {len(filtered)} of {len(docs)} documents")

    # Document list
    type_icons = {"pdf": "📕", "docx": "📘", "txt": "📄"}
    for doc in filtered:
        icon = type_icons.get(doc.file_type, "📄")
        with st.container():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="doc-card">
                    <div class="doc-name">{icon} {doc.filename}</div>
                    <div class="doc-meta">
                        {doc.file_type.upper()} · {format_file_size(doc.file_size)} · {doc.num_chunks} chunks · {format_timestamp(doc.upload_time)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"del_{doc.id}", help="Delete this document"):
                    if vector_store:
                        vector_store.delete_document(doc.id)
                    file_mgr.delete_file(doc.id)
                    st.success(f"Deleted {doc.filename}")
                    st.rerun()

            # Metadata expander
            with st.expander("View Metadata", expanded=False):
                meta = doc.metadata or {}
                if meta:
                    for k, v in meta.items():
                        if v:
                            st.text(f"{k}: {v}")
                else:
                    st.caption("No additional metadata available.")

"""Upload Materials page."""

import streamlit as st

from config import ALLOWED_EXTENSIONS
from utils.helpers import format_file_size, get_file_extension, truncate_text


def render_upload():
    """Render the upload materials page."""
    st.markdown("### 📤 Upload Study Materials")
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1.5rem;">'
        "Upload your study documents (PDF, DOCX, TXT) to enable AI-powered learning features."
        "</div>",
        unsafe_allow_html=True,
    )

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="file_uploader",
        help=f"Supported: {', '.join(ALLOWED_EXTENSIONS)}. Max 50MB per file.",
    )

    if uploaded_files:
        file_mgr = st.session_state.get("file_manager")
        vector_store = st.session_state.get("vector_store")
        analytics = st.session_state.get("analytics_tracker")

        if not file_mgr or not vector_store:
            st.error("System not ready. Please refresh the page.")
            return

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            filename = uploaded_file.name

            # Validate
            valid, error_msg = file_mgr.validate_file(filename, len(file_bytes))
            if not valid:
                st.error(f"❌ {filename}: {error_msg}")
                continue

            # Check duplicate
            dup_id = file_mgr.check_duplicate(file_bytes)
            if dup_id:
                st.warning(f"⚠️ {filename} has already been uploaded.")
                continue

            # Process
            with st.status(f"Processing {filename}...", expanded=True) as status:
                # Save file
                st.write("💾 Saving file...")
                doc = file_mgr.save_file(filename, file_bytes)

                # Parse text
                st.write("📖 Extracting text...")
                try:
                    ext = get_file_extension(filename)
                    if ext == ".pdf":
                        from parsers.pdf_parser import PDFParser

                        parser = PDFParser()
                        text = parser.parse(doc.filepath)
                        meta = parser.extract_metadata(doc.filepath)
                        doc.num_pages = meta.get("page_count", 0)
                        doc.metadata = meta
                    elif ext == ".docx":
                        from parsers.docx_parser import DocxParser

                        parser = DocxParser()
                        text = parser.parse(doc.filepath)
                        meta = parser.extract_metadata(doc.filepath)
                        doc.metadata = meta
                    else:
                        from parsers.txt_parser import TxtParser

                        parser = TxtParser()
                        text = parser.parse(doc.filepath)
                        meta = parser.extract_metadata(doc.filepath)
                        doc.metadata = meta
                except Exception as e:
                    st.error(f"Failed to extract text: {e}")
                    file_mgr.delete_file(doc.id)
                    continue

                # Chunk text
                st.write("✂️ Chunking text...")
                from parsers.processor import TextProcessor

                processor = TextProcessor()
                chunks = processor.get_full_text_chunks(text, doc.id)
                doc.num_chunks = len(chunks)
                file_mgr.update_document(doc.id, num_chunks=len(chunks), num_pages=doc.num_pages, metadata=doc.metadata)

                # Embed and index
                st.write(f"🧠 Embedding {len(chunks)} chunks...")
                vector_store.add_documents(doc.id, chunks, source=filename)

                # Track analytics
                if analytics:
                    analytics.track_upload()

                status.update(label=f"✅ {filename} processed!", state="complete")

            # Preview
            with st.expander(f"📄 Preview: {filename}"):
                st.text(truncate_text(text, 1000))
                st.caption(f"{len(chunks)} chunks · {format_file_size(len(file_bytes))}")

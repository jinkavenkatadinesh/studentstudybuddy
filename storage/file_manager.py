"""File manager — handles file storage, validation, and duplicate detection."""

from __future__ import annotations
import json
import shutil
from pathlib import Path

from config import UPLOAD_DIR, DOCUMENTS_META_FILE, MAX_FILE_SIZE_BYTES, ALLOWED_EXTENSIONS
from models.schemas import Document
from utils.helpers import generate_id, compute_hash, get_file_extension, sanitize_filename
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FileManager:
    """Manages uploaded file storage, validation, and metadata."""

    def __init__(self):
        self.upload_dir = Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self._documents: dict[str, Document] = {}
        self._load_metadata()

    def _load_metadata(self):
        if DOCUMENTS_META_FILE.exists():
            try:
                with open(DOCUMENTS_META_FILE, "r") as f:
                    data = json.load(f)
                for d in data:
                    doc = Document.from_dict(d)
                    self._documents[doc.id] = doc
                logger.info("Loaded %d document records", len(self._documents))
            except Exception as e:
                logger.error("Failed to load document metadata: %s", e)

    def _save_metadata(self):
        try:
            data = [doc.to_dict() for doc in self._documents.values()]
            with open(DOCUMENTS_META_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error("Failed to save document metadata: %s", e)

    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """Validate file type and size."""
        ext = get_file_extension(filename)
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        if file_size > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb:.0f} MB"
        if file_size == 0:
            return False, "File is empty"
        return True, ""

    def check_duplicate(self, file_bytes: bytes) -> str | None:
        """Check if file content already exists. Returns doc_id if duplicate."""
        file_hash = compute_hash(file_bytes)
        for doc in self._documents.values():
            if doc.content_hash == file_hash:
                return doc.id
        return None

    def save_file(self, filename: str, file_bytes: bytes) -> Document:
        """Save an uploaded file and create a Document record."""
        doc_id = generate_id()
        safe_name = sanitize_filename(filename)
        ext = get_file_extension(filename)
        save_name = f"{doc_id}_{safe_name}"
        save_path = self.upload_dir / save_name

        save_path.write_bytes(file_bytes)

        doc = Document(
            id=doc_id,
            filename=filename,
            filepath=str(save_path),
            file_type=ext.lstrip("."),
            file_size=len(file_bytes),
            content_hash=compute_hash(file_bytes),
        )
        self._documents[doc_id] = doc
        self._save_metadata()
        logger.info("Saved file: %s (id=%s)", filename, doc_id)
        return doc

    def delete_file(self, doc_id: str) -> bool:
        if doc_id not in self._documents:
            return False
        doc = self._documents[doc_id]
        try:
            path = Path(doc.filepath)
            if path.exists():
                path.unlink()
        except Exception as e:
            logger.error("Failed to delete file: %s", e)
        del self._documents[doc_id]
        self._save_metadata()
        logger.info("Deleted document: %s", doc_id)
        return True

    def get_document(self, doc_id: str) -> Document | None:
        return self._documents.get(doc_id)

    def list_documents(self) -> list[Document]:
        return sorted(self._documents.values(), key=lambda d: d.upload_time, reverse=True)

    def update_document(self, doc_id: str, **kwargs):
        if doc_id in self._documents:
            doc = self._documents[doc_id]
            for key, value in kwargs.items():
                if hasattr(doc, key):
                    setattr(doc, key, value)
            self._save_metadata()

    @property
    def document_count(self) -> int:
        return len(self._documents)

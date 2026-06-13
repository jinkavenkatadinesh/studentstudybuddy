"""PDF parser — extracts text and metadata from PDF files.

Uses PyPDF2 as primary extractor with pdfplumber as fallback
for complex layouts or scanned-like PDFs.
"""

from pathlib import Path

from PyPDF2 import PdfReader
import pdfplumber

from utils.logger import setup_logger

logger = setup_logger(__name__)


class PDFParser:
    """Handles PDF document parsing and metadata extraction."""

    def parse(self, file_path: str) -> str:
        """Extract text from a PDF file.

        Tries PyPDF2 first. If the extracted text is too short (possibly
        a scanned or complex layout PDF), falls back to pdfplumber.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If no text could be extracted.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        logger.info("Parsing PDF: %s", path.name)

        # Try PyPDF2 first
        text = self._parse_pypdf2(file_path)

        # Fallback to pdfplumber if PyPDF2 extracted very little
        if len(text.strip()) < 50:
            logger.info("PyPDF2 extracted minimal text, falling back to pdfplumber")
            text_plumber = self._parse_pdfplumber(file_path)
            if len(text_plumber.strip()) > len(text.strip()):
                text = text_plumber

        if not text.strip():
            raise ValueError(f"Could not extract text from PDF: {path.name}")

        logger.info("Extracted %d characters from %s", len(text), path.name)
        return text

    def _parse_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2."""
        try:
            reader = PdfReader(file_path)
            pages_text = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    pages_text.append(page_text)
            return "\n\n".join(pages_text)
        except Exception as e:
            logger.warning("PyPDF2 extraction failed: %s", e)
            return ""

    def _parse_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber (handles complex layouts)."""
        try:
            pages_text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        pages_text.append(page_text)
            return "\n\n".join(pages_text)
        except Exception as e:
            logger.warning("pdfplumber extraction failed: %s", e)
            return ""

    def extract_metadata(self, file_path: str) -> dict:
        """Extract metadata from a PDF file.

        Returns:
            Dict with keys: page_count, author, title, creator, creation_date.
        """
        metadata = {
            "page_count": 0,
            "author": "",
            "title": "",
            "creator": "",
            "creation_date": "",
        }
        try:
            reader = PdfReader(file_path)
            metadata["page_count"] = len(reader.pages)
            if reader.metadata:
                metadata["author"] = reader.metadata.get("/Author", "") or ""
                metadata["title"] = reader.metadata.get("/Title", "") or ""
                metadata["creator"] = reader.metadata.get("/Creator", "") or ""
                raw_date = reader.metadata.get("/CreationDate", "")
                metadata["creation_date"] = str(raw_date) if raw_date else ""
        except Exception as e:
            logger.warning("Could not extract PDF metadata: %s", e)
        return metadata

    def get_page_count(self, file_path: str) -> int:
        """Get the number of pages in a PDF."""
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception:
            return 0

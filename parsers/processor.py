"""Text processor — cleaning, chunking, and preprocessing pipeline."""

import re
import unicodedata

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE
from models.schemas import TextChunk
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TextProcessor:
    """Handles text cleaning, chunking, and preprocessing."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def clean_text(self, text: str) -> str:
        """Clean and normalize raw text.

        - Normalize Unicode characters
        - Remove control characters (keep newlines and tabs)
        - Collapse excessive whitespace
        - Strip leading/trailing whitespace per line
        """
        # Normalize unicode
        text = unicodedata.normalize("NFKC", text)

        # Remove control characters except newline and tab
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        # Replace tabs with spaces
        text = text.replace("\t", "    ")

        # Collapse multiple spaces to single space (per line)
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            line = re.sub(r" {2,}", " ", line).strip()
            cleaned_lines.append(line)

        # Collapse 3+ consecutive blank lines to 2
        text = "\n".join(cleaned_lines)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def chunk_text(self, text: str, doc_id: str) -> list[TextChunk]:
        """Split text into overlapping chunks for embedding.

        Uses LangChain's RecursiveCharacterTextSplitter for intelligent splitting
        at paragraph, sentence, and word boundaries.

        Args:
            text: Cleaned text to chunk.
            doc_id: Document ID for chunk metadata.

        Returns:
            List of TextChunk objects.
        """
        if not text.strip():
            return []

        raw_chunks = self._splitter.split_text(text)
        chunks = []
        for i, chunk_text in enumerate(raw_chunks):
            chunks.append(
                TextChunk(
                    content=chunk_text,
                    doc_id=doc_id,
                    chunk_index=i,
                    metadata={"chunk_size": len(chunk_text)},
                )
            )

        logger.info("Split document %s into %d chunks", doc_id, len(chunks))
        return chunks

    def detect_language(self, text: str) -> str:
        """Detect the primary language of the text.

        Returns:
            ISO 639-1 language code (e.g., 'en', 'hi', 'ta').
        """
        try:
            from langdetect import detect

            sample = text[:2000]  # Use first 2000 chars for speed
            return detect(sample)
        except Exception:
            return "en"

    def preprocess(self, text: str) -> str:
        """Full preprocessing pipeline: clean → normalize."""
        return self.clean_text(text)

    def get_full_text_chunks(self, text: str, doc_id: str) -> list[TextChunk]:
        """Clean text and split into chunks — full pipeline."""
        cleaned = self.preprocess(text)
        return self.chunk_text(cleaned, doc_id)

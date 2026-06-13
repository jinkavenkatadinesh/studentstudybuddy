"""TXT parser — reads plain text files with encoding detection."""

from pathlib import Path

from utils.logger import setup_logger

logger = setup_logger(__name__)

# Encodings to try in order of likelihood
_ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "ascii"]


class TxtParser:
    """Handles plain text file parsing."""

    def parse(self, file_path: str) -> str:
        """Read text from a TXT file with encoding detection.

        Tries multiple encodings until one succeeds.

        Args:
            file_path: Path to the text file.

        Returns:
            File text content.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file can't be decoded.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {file_path}")

        logger.info("Parsing TXT: %s", path.name)

        for encoding in _ENCODINGS:
            try:
                text = path.read_text(encoding=encoding)
                if text.strip():
                    logger.info(
                        "Read %d characters from %s (encoding: %s)",
                        len(text),
                        path.name,
                        encoding,
                    )
                    return text
            except (UnicodeDecodeError, UnicodeError):
                continue

        raise ValueError(f"Could not decode text file: {path.name}")

    def extract_metadata(self, file_path: str) -> dict:
        """Extract basic metadata from a text file."""
        metadata = {"word_count": 0, "line_count": 0, "encoding": ""}
        try:
            for encoding in _ENCODINGS:
                try:
                    text = Path(file_path).read_text(encoding=encoding)
                    metadata["word_count"] = len(text.split())
                    metadata["line_count"] = text.count("\n") + 1
                    metadata["encoding"] = encoding
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
        except Exception as e:
            logger.warning("Could not extract TXT metadata: %s", e)
        return metadata

"""General utility functions."""

import hashlib
import re
import uuid
from datetime import datetime


def generate_id() -> str:
    """Generate a unique document/entity ID."""
    return uuid.uuid4().hex[:12]


def compute_hash(data: bytes) -> str:
    """Compute SHA-256 hash of binary data for duplicate detection."""
    return hashlib.sha256(data).hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format byte count to human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def format_timestamp(ts: float | None = None) -> str:
    """Format a UNIX timestamp to readable string. Defaults to now."""
    dt = datetime.fromtimestamp(ts) if ts else datetime.now()
    return dt.strftime("%b %d, %Y %I:%M %p")


def truncate_text(text: str, max_len: int = 200) -> str:
    """Truncate text to max_len, adding ellipsis if needed."""
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "…"


def sanitize_filename(name: str) -> str:
    """Remove unsafe characters from a filename."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip("_")[:200]


def get_file_extension(filename: str) -> str:
    """Get lowercase file extension including the dot."""
    idx = filename.rfind(".")
    if idx == -1:
        return ""
    return filename[idx:].lower()

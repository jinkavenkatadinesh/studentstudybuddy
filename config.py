"""Centralized configuration for Student Study Buddy."""

import os
from pathlib import Path

# ── App Metadata ──────────────────────────────────────────────────────────────
APP_NAME = "Student Study Buddy"
APP_VERSION = "1.0.0"
APP_ICON = "📚"
APP_DESCRIPTION = "AI-powered learning assistant that processes your study materials."

# ── Directory Paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_DIR = DATA_DIR / "vectors"
LOG_DIR = BASE_DIR / "logs"
ANALYTICS_FILE = DATA_DIR / "analytics.json"
DOCUMENTS_META_FILE = DATA_DIR / "documents.json"

# Auto-create directories
for _dir in [DATA_DIR, UPLOAD_DIR, VECTOR_DIR, LOG_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── Ollama Configuration ─────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "qwen3:8b"
AVAILABLE_MODELS = [
    "qwen3:8b",
    "qwen2.5-coder",
    "mistral",
    "llama3",
]
DEFAULT_TEMPERATURE = 0.7
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 1.5

# ── Embedding Configuration ──────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2

# ── Text Processing ──────────────────────────────────────────────────────────
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CONTEXT_CHUNKS = 5

# ── File Upload ───────────────────────────────────────────────────────────────
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]
ALLOWED_MIME_TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}

# ── Quiz Configuration ───────────────────────────────────────────────────────
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DEFAULT_DIFFICULTY = "medium"
DEFAULT_NUM_QUESTIONS = 5
MIN_NUM_QUESTIONS = 3
MAX_NUM_QUESTIONS = 20
QUIZ_TIME_PER_QUESTION = 30  # seconds

# ── Flashcard Configuration ──────────────────────────────────────────────────
DEFAULT_NUM_FLASHCARDS = 10
MIN_NUM_FLASHCARDS = 5
MAX_NUM_FLASHCARDS = 30

# ── Summary Configuration ────────────────────────────────────────────────────
SUMMARY_TYPES = ["short", "detailed", "bullet", "chapter"]

# ── Retrieval Configuration ──────────────────────────────────────────────────
DEFAULT_RETRIEVAL_K = 5
MAX_RETRIEVAL_K = 10

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ── Navigation Pages ─────────────────────────────────────────────────────────
PAGES = {
    "home": {"label": "Home Dashboard", "icon": "🏠"},
    "upload": {"label": "Upload Materials", "icon": "📤"},
    "library": {"label": "Document Library", "icon": "📚"},
    "summary": {"label": "AI Summary", "icon": "📝"},
    "flashcards": {"label": "Flashcards", "icon": "🃏"},
    "quiz": {"label": "Quiz Generator", "icon": "🧪"},
    "chat": {"label": "Ask Documents", "icon": "💬"},
    "analytics": {"label": "Study Analytics", "icon": "📊"},
}

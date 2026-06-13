"""Student Study Buddy — AI-Powered Learning Assistant.

Main Streamlit application entry point.
Initializes all services and manages page routing.
"""

import os

import streamlit as st

from config import APP_ICON, APP_NAME

# ── Page Config (must be first Streamlit command) ─────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} — AI Learning Assistant",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Service Initialization ───────────────────────────────────────────────────


@st.cache_resource(show_spinner="Loading embedding model...")
def _init_embedding_manager():
    """Initialize the embedding manager (cached across reruns)."""
    from embeddings.manager import get_embedding_manager

    return get_embedding_manager()


@st.cache_resource(show_spinner="Loading vector store...")
def _init_vector_store(_embedding_manager):
    """Initialize the FAISS vector store (cached across reruns)."""
    from vectorstore.faiss_store import FAISSVectorStore

    return FAISSVectorStore(_embedding_manager)


@st.cache_resource
def _init_file_manager():
    """Initialize the file manager (cached across reruns)."""
    from storage.file_manager import FileManager

    return FileManager()


@st.cache_resource
def _init_analytics_tracker():
    """Initialize the analytics tracker (cached across reruns)."""
    from analytics.tracker import AnalyticsTracker

    return AnalyticsTracker()


def _init_ollama_manager():
    """Initialize the Ollama manager (not cached — needs to check availability)."""
    from config import OLLAMA_BASE_URL
    from services.ollama_manager import OllamaManager

    return OllamaManager(OLLAMA_BASE_URL)


def _init_services():
    """Initialize all services and store them in session state."""
    # Only initialize once per session
    if st.session_state.get("_services_initialized"):
        return

    # Embedding Manager
    embedding_mgr = _init_embedding_manager()
    st.session_state.embedding_manager = embedding_mgr

    # Vector Store
    vector_store = _init_vector_store(embedding_mgr)
    st.session_state.vector_store = vector_store

    # File Manager
    file_mgr = _init_file_manager()
    st.session_state.file_manager = file_mgr

    # Analytics Tracker
    analytics = _init_analytics_tracker()
    st.session_state.analytics_tracker = analytics
    st.session_state.analytics_stats = analytics.get_stats()

    # Ollama Manager
    ollama_mgr = _init_ollama_manager()
    st.session_state.ollama_manager = ollama_mgr
    st.session_state.ollama_available = ollama_mgr.is_available()

    if st.session_state.ollama_available:
        st.session_state.ollama_models = ollama_mgr.list_models()
        # Auto-pull default model if missing
        from config import DEFAULT_MODEL

        model_exists = any(DEFAULT_MODEL in m for m in st.session_state.ollama_models)
        if not model_exists:
            with st.spinner(f"📥 Downloading local model '{DEFAULT_MODEL}' (~1.6GB)... This may take a few minutes."):
                try:
                    ollama_mgr.pull_model(DEFAULT_MODEL)
                    st.session_state.ollama_models = ollama_mgr.list_models()
                except Exception as e:
                    st.error(f"Failed to auto-download '{DEFAULT_MODEL}': {e}")
    else:
        st.session_state.ollama_models = []

    # Unified AI Manager
    from services.ai_manager import AIManager

    ai_mgr = AIManager(ollama_mgr)
    st.session_state.ai_manager = ai_mgr

    # RAG Pipeline
    from rag.pipeline import RAGPipeline

    rag = RAGPipeline(vector_store, ai_mgr)
    st.session_state.rag_pipeline = rag

    # Generators
    from services.flashcard_generator import FlashcardGenerator
    from services.quiz_generator import QuizGenerator
    from services.summary_generator import SummaryGenerator

    st.session_state.quiz_generator = QuizGenerator(rag, ai_mgr)
    st.session_state.flashcard_generator = FlashcardGenerator(rag, ai_mgr)
    st.session_state.summary_generator = SummaryGenerator(rag, ai_mgr)

    st.session_state._services_initialized = True


# Initialize all services
_init_services()

# ── Initialize Session State ─────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "ai_provider" not in st.session_state:
    st.session_state.ai_provider = "ollama"

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

if "selected_model" not in st.session_state:
    from config import DEFAULT_MODEL

    available = st.session_state.get("ollama_models", [])
    if available and DEFAULT_MODEL not in available:
        st.session_state.selected_model = available[0]
    else:
        st.session_state.selected_model = DEFAULT_MODEL


if "temperature" not in st.session_state:
    from config import DEFAULT_TEMPERATURE

    st.session_state.temperature = DEFAULT_TEMPERATURE


# ── Render Components ─────────────────────────────────────────────────────────
from components.header import render_header
from components.sidebar import render_sidebar

render_header()
render_sidebar()


# ── Page Router ───────────────────────────────────────────────────────────────
page = st.session_state.get("current_page", "home")

try:
    if page == "home":
        from views.home import render_home

        render_home()
    elif page == "upload":
        from views.upload import render_upload

        render_upload()
    elif page == "library":
        from views.library import render_library

        render_library()
    elif page == "summary":
        from views.summary import render_summary

        render_summary()
    elif page == "flashcards":
        from views.flashcards import render_flashcards

        render_flashcards()
    elif page == "quiz":
        from views.quiz import render_quiz

        render_quiz()
    elif page == "chat":
        from views.chat import render_chat

        render_chat()
    elif page == "analytics":
        from views.analytics_page import render_analytics

        render_analytics()
    else:
        st.session_state.current_page = "home"
        st.rerun()

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.caption("Try refreshing the page or checking if Ollama is running.")

    import traceback

    with st.expander("Error Details"):
        st.code(traceback.format_exc())

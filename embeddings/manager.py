"""Embedding manager — Sentence Transformer embeddings with caching.

Provides a singleton-style manager for generating text embeddings
using a local Sentence Transformer model.
"""

from __future__ import annotations

import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL
from utils.logger import setup_logger

logger = setup_logger(__name__)

_instance: EmbeddingManager | None = None


class EmbeddingManager:
    """Manages text embedding generation with Sentence Transformers.

    Uses a singleton pattern to share a single model instance across
    the application, avoiding redundant model loading.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self._model: SentenceTransformer | None = None
        self._langchain_embeddings: HuggingFaceEmbeddings | None = None
        logger.info("EmbeddingManager initialized with model: %s", model_name)

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-load the Sentence Transformer model."""
        if self._model is None:
            logger.info("Loading Sentence Transformer model: %s", self.model_name)
            self._model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
        return self._model

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text.

        Args:
            text: Text to embed.

        Returns:
            Numpy array of shape (embedding_dim,).
        """
        return self.model.encode(text, show_progress_bar=False)

    def embed_batch(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed.
            batch_size: Number of texts per batch.

        Returns:
            Numpy array of shape (num_texts, embedding_dim).
        """
        if not texts:
            return np.array([])

        logger.info("Embedding batch of %d texts", len(texts))
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embeddings

    def get_langchain_embeddings(self) -> HuggingFaceEmbeddings:
        """Get a LangChain-compatible embedding wrapper.

        Returns:
            HuggingFaceEmbeddings instance using the same model.
        """
        if self._langchain_embeddings is None:
            self._langchain_embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self._langchain_embeddings

    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self.model.get_sentence_embedding_dimension()


def get_embedding_manager(model_name: str = EMBEDDING_MODEL) -> EmbeddingManager:
    """Get or create the singleton EmbeddingManager instance."""
    global _instance
    if _instance is None or _instance.model_name != model_name:
        _instance = EmbeddingManager(model_name)
    return _instance

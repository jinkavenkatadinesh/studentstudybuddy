"""FAISS vector store — manages document embeddings with CRUD operations."""

from __future__ import annotations

import pickle
from pathlib import Path

import faiss
import numpy as np
from langchain_community.vectorstores import FAISS as LangchainFAISS

from config import MAX_CONTEXT_CHUNKS, VECTOR_DIR
from embeddings.manager import EmbeddingManager
from models.schemas import TextChunk
from utils.logger import setup_logger

logger = setup_logger(__name__)

FAISS_INDEX_FILE = Path(VECTOR_DIR) / "index.faiss"
METADATA_FILE = Path(VECTOR_DIR) / "metadata.pkl"


class FAISSVectorStore:
    """FAISS-backed vector store with document-level CRUD."""

    def __init__(self, embedding_manager: EmbeddingManager):
        self.embedding_manager = embedding_manager
        self._index: faiss.IndexFlatIP | None = None
        self._metadata: list[dict] = []
        self._langchain_store: LangchainFAISS | None = None
        self._load()

    def _load(self):
        if FAISS_INDEX_FILE.exists() and METADATA_FILE.exists():
            try:
                self._index = faiss.read_index(str(FAISS_INDEX_FILE))
                with open(METADATA_FILE, "rb") as f:
                    self._metadata = pickle.load(f)  # nosec B301 # nosem
                logger.info("Loaded FAISS index with %d vectors", self._index.ntotal)
                self._rebuild_langchain_store()
            except Exception as e:
                logger.error("Failed to load FAISS index: %s", e)
                self._init_empty()
        else:
            self._init_empty()

    def _init_empty(self):
        dim = self.embedding_manager.dimension
        self._index = faiss.IndexFlatIP(dim)
        self._metadata = []
        self._langchain_store = None

    def _rebuild_langchain_store(self):
        if not self._metadata:
            self._langchain_store = None
            return
        try:
            embeddings = self.embedding_manager.get_langchain_embeddings()
            texts = [m["content"] for m in self._metadata]
            metadatas = [
                {"doc_id": m["doc_id"], "chunk_index": m["chunk_index"], "source": m.get("source", "")}
                for m in self._metadata
            ]
            self._langchain_store = LangchainFAISS.from_texts(texts, embeddings, metadatas=metadatas)
        except Exception as e:
            logger.error("Failed to rebuild LangChain store: %s", e)
            self._langchain_store = None

    def add_documents(self, doc_id: str, chunks: list[TextChunk], source: str = "") -> int:
        if not chunks:
            return 0
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_manager.embed_batch(texts)
        assert self._index is not None
        self._index.add(np.array(embeddings, dtype=np.float32))
        for chunk in chunks:
            self._metadata.append(
                {"doc_id": doc_id, "chunk_index": chunk.chunk_index, "content": chunk.content, "source": source}
            )
        self._rebuild_langchain_store()
        self.save()
        logger.info("Added %d chunks for document %s", len(chunks), doc_id)
        return len(chunks)

    def delete_document(self, doc_id: str) -> bool:
        keep = [i for i, m in enumerate(self._metadata) if m["doc_id"] != doc_id]
        if len(keep) == len(self._metadata):
            return False
        if not keep:
            self._init_empty()
        else:
            assert self._index is not None
            vecs = faiss.rev_swig_ptr(self._index.get_xb(), self._index.ntotal * self._index.d)
            vecs = vecs.reshape(self._index.ntotal, self._index.d).copy()
            keep_vecs = vecs[keep]
            self._metadata = [self._metadata[i] for i in keep]
            dim = self._index.d
            self._index = faiss.IndexFlatIP(dim)
            self._index.add(np.array(keep_vecs, dtype=np.float32))
            self._rebuild_langchain_store()
        self.save()
        return True

    def update_document(self, doc_id: str, chunks: list[TextChunk], source: str = "") -> int:
        self.delete_document(doc_id)
        return self.add_documents(doc_id, chunks, source)

    def similarity_search(self, query: str, k: int = MAX_CONTEXT_CHUNKS) -> list[tuple[str, float, dict]]:
        if self._index is None or self._index.ntotal == 0:
            return []
        k = min(k, self._index.ntotal)
        qe = self.embedding_manager.embed_text(query)
        scores, indices = self._index.search(np.array([qe], dtype=np.float32), k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self._metadata):
                meta = self._metadata[idx]
                results.append((meta["content"], float(score), meta))
        return results

    def get_retriever(self, k: int = MAX_CONTEXT_CHUNKS):
        if self._langchain_store is None:
            return None
        return self._langchain_store.as_retriever(search_type="similarity", search_kwargs={"k": k})

    def get_document_chunks(self, doc_id: str) -> list[str]:
        chunks = [(m["chunk_index"], m["content"]) for m in self._metadata if m["doc_id"] == doc_id]
        chunks.sort(key=lambda x: x[0])
        return [c for _, c in chunks]

    def save(self):
        try:
            if self._index is not None:
                faiss.write_index(self._index, str(FAISS_INDEX_FILE))
            with open(METADATA_FILE, "wb") as f:
                pickle.dump(self._metadata, f)  # nosem
        except Exception as e:
            logger.error("Failed to save FAISS index: %s", e)

    @property
    def total_vectors(self) -> int:
        return self._index.ntotal if self._index else 0

    @property
    def document_ids(self) -> list[str]:
        return list({m["doc_id"] for m in self._metadata})

    def has_document(self, doc_id: str) -> bool:
        return any(m["doc_id"] == doc_id for m in self._metadata)

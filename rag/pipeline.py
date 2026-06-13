"""RAG pipeline — retrieval-augmented generation for document Q&A."""

from __future__ import annotations

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_CONTEXT_CHUNKS
from rag.prompts import CHAT_SYSTEM_PROMPT, QA_PROMPT, QA_SYSTEM_PROMPT
from services.ai_manager import AIManager
from utils.logger import setup_logger
from vectorstore.faiss_store import FAISSVectorStore

logger = setup_logger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline.

    Combines FAISS similarity search with LLM generation
    to answer questions grounded in uploaded documents.
    """

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        ai_manager: AIManager,
    ):
        self.vector_store = vector_store
        self.ai_manager = ai_manager

    def ask(
        self,
        question: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        k: int = MAX_CONTEXT_CHUNKS,
    ) -> tuple[str, list[dict]]:
        """Ask a question using RAG (retrieve → generate)."""
        results = self.vector_store.similarity_search(question, k=k)

        if not results:
            return "I don't have any documents to search. Please upload study materials first.", []

        context_parts = []
        sources = []
        for i, (content, score, meta) in enumerate(results):
            context_parts.append(f"[Source {i + 1}] {content}")
            sources.append(
                {
                    "content": content[:200] + "..." if len(content) > 200 else content,
                    "source": meta.get("source", "Unknown"),
                    "doc_id": meta.get("doc_id", ""),
                    "score": round(score, 3),
                }
            )

        context = "\n\n".join(context_parts)
        prompt = QA_PROMPT.format(context=context, question=question)

        # Generate answer
        answer = self.ai_manager.generate(
            prompt=prompt,
            model=model,
            temperature=temperature,
            system=QA_SYSTEM_PROMPT,
        )

        logger.info("RAG answered question with %d sources", len(sources))
        return answer, sources

    def stream_ask(
        self,
        question: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        k: int = MAX_CONTEXT_CHUNKS,
    ):
        """Stream an answer using RAG. Yields text chunks, then sources at the end."""
        results = self.vector_store.similarity_search(question, k=k)

        if not results:
            yield "I don't have any documents to search. Please upload study materials first."
            return

        context_parts = []
        sources = []
        for i, (content, score, meta) in enumerate(results):
            context_parts.append(f"[Source {i + 1}] {content}")
            sources.append(
                {
                    "content": content[:200] + "..." if len(content) > 200 else content,
                    "source": meta.get("source", "Unknown"),
                    "doc_id": meta.get("doc_id", ""),
                    "score": round(score, 3),
                }
            )

        context = "\n\n".join(context_parts)
        prompt = QA_PROMPT.format(context=context, question=question)

        for chunk in self.ai_manager.stream_generate(
            prompt=prompt,
            model=model,
            temperature=temperature,
            system=CHAT_SYSTEM_PROMPT,
        ):
            yield chunk

        # Yield sources as the final item
        yield sources

    def generate_with_context(
        self,
        prompt: str,
        context: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = "",
    ) -> str:
        """Generate using a custom prompt with provided context."""
        full_prompt = prompt.format(context=context) if "{context}" in prompt else prompt
        return self.ai_manager.generate(
            prompt=full_prompt,
            model=model,
            temperature=temperature,
            system=system,
        )

    def get_document_context(self, doc_id: str, max_chars: int = 8000) -> str:
        """Get the full text content of a document from the vector store."""
        chunks = self.vector_store.get_document_chunks(doc_id)
        if not chunks:
            return ""
        full_text = "\n\n".join(chunks)
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "\n\n[Content truncated...]"
        return full_text

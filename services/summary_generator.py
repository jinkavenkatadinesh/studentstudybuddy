"""Summary generator — creates AI summaries of documents."""

from __future__ import annotations

from models.schemas import Summary
from rag.pipeline import RAGPipeline
from rag.prompts import (
    SUMMARY_SHORT_PROMPT, SUMMARY_DETAILED_PROMPT,
    SUMMARY_BULLET_PROMPT, SUMMARY_CHAPTER_PROMPT,
)
from services.ollama_manager import OllamaManager
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from utils.logger import setup_logger

logger = setup_logger(__name__)

_PROMPT_MAP = {
    "short": SUMMARY_SHORT_PROMPT,
    "detailed": SUMMARY_DETAILED_PROMPT,
    "bullet": SUMMARY_BULLET_PROMPT,
    "chapter": SUMMARY_CHAPTER_PROMPT,
}


class SummaryGenerator:
    """Generates various types of summaries from document content."""

    def __init__(self, rag_pipeline: RAGPipeline, ollama_manager: OllamaManager):
        self.rag = rag_pipeline
        self.ollama = ollama_manager

    def generate(
        self,
        doc_id: str,
        summary_type: str = "short",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Summary:
        """Generate a summary of the specified type."""
        context = self.rag.get_document_context(doc_id, max_chars=10000)
        if not context:
            raise ValueError("No content found for this document.")

        prompt_template = _PROMPT_MAP.get(summary_type, SUMMARY_SHORT_PROMPT)
        prompt = prompt_template.format(text=context)

        content = self.ollama.generate(
            prompt=prompt, model=model, temperature=temperature,
            system="You are an expert academic summarizer. Create clear, well-organized summaries.",
        )

        logger.info("Generated %s summary for document %s", summary_type, doc_id)
        return Summary(content=content, summary_type=summary_type, doc_id=doc_id)

    def generate_short(self, doc_id: str, **kwargs) -> Summary:
        return self.generate(doc_id, "short", **kwargs)

    def generate_detailed(self, doc_id: str, **kwargs) -> Summary:
        return self.generate(doc_id, "detailed", **kwargs)

    def generate_bullet(self, doc_id: str, **kwargs) -> Summary:
        return self.generate(doc_id, "bullet", **kwargs)

    def generate_chapter_wise(self, doc_id: str, **kwargs) -> Summary:
        return self.generate(doc_id, "chapter", **kwargs)

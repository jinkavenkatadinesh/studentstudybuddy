"""Unit tests for SummaryGenerator."""

from unittest.mock import MagicMock

import pytest

from services.summary_generator import SummaryGenerator


def test_summary_generator_success():
    """Test successful summary generation."""
    rag_mock = MagicMock()
    rag_mock.get_document_context.return_value = "This is a document about machine learning."

    ai_mock = MagicMock()
    ai_mock.generate.return_value = "Summary: Machine learning."

    generator = SummaryGenerator(rag_mock, ai_mock)
    summary = generator.generate("doc123", summary_type="short")

    assert summary.content == "Summary: Machine learning."
    assert summary.doc_id == "doc123"
    assert summary.summary_type == "short"

    rag_mock.get_document_context.assert_called_once_with("doc123", max_chars=10000)
    ai_mock.generate.assert_called_once()


def test_summary_generator_no_context():
    """Test generator raises ValueError if document context is empty."""
    rag_mock = MagicMock()
    rag_mock.get_document_context.return_value = ""

    ai_mock = MagicMock()

    generator = SummaryGenerator(rag_mock, ai_mock)
    with pytest.raises(ValueError, match="No content found for this document"):
        generator.generate("doc123")

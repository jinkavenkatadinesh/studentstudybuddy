"""Unit tests for the Unified AI Manager."""

from unittest.mock import MagicMock

import pytest

from services.ai_manager import AIManager


def test_ai_manager_provider_detection(mock_session_state):
    """Test AIManager reads the correct provider from session state."""
    mock_session_state["ai_provider"] = "openai"

    ollama_mock = MagicMock()
    manager = AIManager(ollama_mock)

    assert manager._get_provider() == "openai"


def test_ai_manager_api_key_retrieval(mock_session_state):
    """Test AIManager retrieves the API key correctly."""
    mock_session_state["openai_api_key"] = "test-openai-key"
    mock_session_state["gemini_api_key"] = "test-gemini-key"

    ollama_mock = MagicMock()
    manager = AIManager(ollama_mock)

    assert manager._get_api_key("openai") == "test-openai-key"
    assert manager._get_api_key("gemini") == "test-gemini-key"


def test_ai_manager_ollama_routing(mock_session_state):
    """Test routing to Ollama manager."""
    mock_session_state["ai_provider"] = "ollama"

    ollama_mock = MagicMock()
    ollama_mock.generate.return_value = "Ollama response"

    manager = AIManager(ollama_mock)
    response = manager.generate("Hello", "qwen2.5-coder")

    ollama_mock.generate.assert_called_once_with("Hello", "qwen2.5-coder", 0.7, "")
    assert response == "Ollama response"


def test_ai_manager_missing_keys(mock_session_state):
    """Test validation errors for missing API keys."""
    mock_session_state["ai_provider"] = "openai"
    mock_session_state["openai_api_key"] = ""

    ollama_mock = MagicMock()
    manager = AIManager(ollama_mock)

    with pytest.raises(ValueError, match="OpenAI API Key is required"):
        manager.generate("Hello", "gpt-4o-mini")

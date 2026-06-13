"""Unit tests for the OllamaManager."""

from unittest.mock import MagicMock, patch

from services.ollama_manager import OllamaManager


@patch("services.ollama_manager.ollama.Client")
def test_ollama_is_available(mock_client_cls):
    """Test availability check returns True when listing models succeeds."""
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.list.return_value = {"models": []}

    manager = OllamaManager()
    assert manager.is_available() is True
    mock_client.list.assert_called_once()


@patch("services.ollama_manager.ollama.Client")
def test_ollama_is_available_failure(mock_client_cls):
    """Test availability check returns False when listing models throws exception."""
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.list.side_effect = Exception("Connection refused")

    manager = OllamaManager()
    assert manager.is_available() is False


@patch("services.ollama_manager.ollama.Client")
def test_ollama_list_models(mock_client_cls):
    """Test list_models returns a sorted list of model names."""
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.list.return_value = {"models": [{"name": "llama3:latest"}, {"model": "qwen2.5-coder:1.5b"}]}

    manager = OllamaManager()
    models = manager.list_models()
    assert models == ["llama3:latest", "qwen2.5-coder:1.5b"]


@patch("services.ollama_manager.ollama.Client")
def test_ollama_generate(mock_client_cls):
    """Test chat generation response."""
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.chat.return_value = {"message": {"content": "Test response content"}}

    manager = OllamaManager()
    response = manager.generate("Hello", model="llama3")
    assert response == "Test response content"
    mock_client.chat.assert_called_once()

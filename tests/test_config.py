"""Unit tests for configuration settings."""

import config


def test_app_metadata():
    """Verify application metadata values."""
    assert config.APP_NAME == "Student Study Buddy"
    assert config.APP_VERSION == "1.0.0"
    assert config.APP_ICON == "📚"


def test_directory_configuration():
    """Verify that configuration directories are properly set up and exist."""
    assert config.DATA_DIR.exists()
    assert config.UPLOAD_DIR.exists()
    assert config.VECTOR_DIR.exists()
    assert config.LOG_DIR.exists()


def test_model_configurations():
    """Verify default models are present."""
    assert "gpt-4o-mini" in config.OPENAI_MODELS
    assert "gemini-2.0-flash" in config.GEMINI_MODELS
    assert config.DEFAULT_MODEL in config.AVAILABLE_MODELS

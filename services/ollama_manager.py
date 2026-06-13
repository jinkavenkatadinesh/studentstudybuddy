"""Ollama manager — handles connection, model listing, and text generation."""

from __future__ import annotations

import ollama
from langchain_ollama import ChatOllama

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, OLLAMA_BASE_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)


class OllamaManager:
    """Manages Ollama API interactions for LLM generation."""

    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url
        self._client = ollama.Client(host=base_url)

    def is_available(self) -> bool:
        """Check if Ollama server is reachable."""
        try:
            self._client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """Get list of available model names."""
        try:
            response = self._client.list()
            models = []
            for m in response.get("models", []):
                name = m.get("name", "") or m.get("model", "")
                if name:
                    models.append(name)
            return sorted(models)
        except Exception as e:
            logger.error("Failed to list models: %s", e)
            return []

    def pull_model(self, model: str) -> None:
        """Pull a model from Ollama."""
        try:
            logger.info("Starting pull for model: %s", model)
            self._client.pull(model)
            logger.info("Successfully pulled model: %s", model)
        except Exception as e:
            logger.error("Failed to pull model %s: %s", model, e)
            raise RuntimeError(f"Failed to pull model {model}: {e}")

    def generate(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = "",
    ) -> str:
        """Generate a response from Ollama.

        Args:
            prompt: User prompt.
            model: Model name.
            temperature: Sampling temperature.
            system: Optional system prompt.

        Returns:
            Generated text response.
        """
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self._client.chat(
                model=model,
                messages=messages,
                options={"temperature": temperature},
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error("Ollama generation failed: %s", e)
            raise ConnectionError(f"Failed to generate with Ollama: {e}")

    def stream_generate(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = "",
    ):
        """Stream a response from Ollama, yielding text chunks.

        Yields:
            Text chunks as they are generated.
        """
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            stream = self._client.chat(
                model=model,
                messages=messages,
                options={"temperature": temperature},
                stream=True,
            )
            for chunk in stream:
                text = chunk.get("message", {}).get("content", "")
                if text:
                    yield text
        except Exception as e:
            logger.error("Ollama streaming failed: %s", e)
            yield f"\n\n⚠️ Error: {e}"

    def get_langchain_llm(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> ChatOllama:
        """Get a LangChain-compatible ChatOllama instance."""
        return ChatOllama(
            model=model,
            base_url=self.base_url,
            temperature=temperature,
        )

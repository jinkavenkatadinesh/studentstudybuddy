"""Unified AI Manager — supports Ollama, OpenAI, and Google Gemini."""

from __future__ import annotations

import os
from typing import Generator

import streamlit as st
from google import genai
from google.genai import types
from openai import OpenAI

from config import DEFAULT_TEMPERATURE
from services.ollama_manager import OllamaManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AIManager:
    """Unified AI generation interface for local and cloud LLMs."""

    def __init__(self, ollama_manager: OllamaManager):
        self.ollama = ollama_manager

    def _get_provider(self) -> str:
        """Get the active AI provider from session state."""
        return st.session_state.get("ai_provider", "ollama")

    def _get_api_key(self, provider: str) -> str:
        """Get the API key for the provider from session state or environment."""
        if provider == "openai":
            key = st.session_state.get("openai_api_key", "").strip()
            if not key:
                key = os.getenv("OPENAI_API_KEY", "").strip()
            return key
        elif provider == "gemini":
            key = st.session_state.get("gemini_api_key", "").strip()
            if not key:
                key = os.getenv("GEMINI_API_KEY", "").strip()
            return key
        return ""

    def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = "",
    ) -> str:
        """Generate response text from the active provider."""
        provider = self._get_provider()
        api_key = self._get_api_key(provider)

        if provider == "ollama":
            return self.ollama.generate(prompt, model, temperature, system)

        elif provider == "openai":
            if not api_key:
                raise ValueError("OpenAI API Key is required. Please set it in the sidebar.")
            try:
                openai_client = OpenAI(api_key=api_key)
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                response = openai_client.chat.completions.create(
                    model=model,
                    messages=messages,  # type: ignore
                    temperature=temperature,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                logger.error("OpenAI generation failed: %s", e)
                raise RuntimeError(f"OpenAI generation failed: {e}")

        elif provider == "gemini":
            if not api_key:
                raise ValueError("Gemini API Key is required. Please set it in the sidebar.")
            try:
                gemini_client = genai.Client(api_key=api_key)
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system if system else None,
                )
                response = gemini_client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                return response.text or ""
            except Exception as e:
                logger.error("Gemini generation failed: %s", e)
                raise RuntimeError(f"Gemini generation failed: {e}")

        else:
            raise ValueError(f"Unknown AI Provider: {provider}")

    def stream_generate(
        self,
        prompt: str,
        model: str,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = "",
    ) -> Generator[str, None, None]:
        """Stream response chunks from the active provider."""
        provider = self._get_provider()
        api_key = self._get_api_key(provider)

        if provider == "ollama":
            yield from self.ollama.stream_generate(prompt, model, temperature, system)

        elif provider == "openai":
            if not api_key:
                yield "⚠️ OpenAI API Key is required. Please set it in the sidebar."
                return
            try:
                openai_client = OpenAI(api_key=api_key)
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                stream = openai_client.chat.completions.create(
                    model=model,
                    messages=messages,  # type: ignore
                    temperature=temperature,
                    stream=True,
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            except Exception as e:
                logger.error("OpenAI streaming failed: %s", e)
                yield f"\n\n⚠️ Error: {e}"

        elif provider == "gemini":
            if not api_key:
                yield "⚠️ Gemini API Key is required. Please set it in the sidebar."
                return
            try:
                gemini_client = genai.Client(api_key=api_key)
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system if system else None,
                )
                response_stream = gemini_client.models.generate_content_stream(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                logger.error("Gemini streaming failed: %s", e)
                yield f"\n\n⚠️ Error: {e}"
        else:
            yield f"⚠️ Unknown provider: {provider}"

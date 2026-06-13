# Feature Specification: Unified AI Manager & BYOK Cloud Support 📐

This specification outlines the unified AI interface supporting local inference (Ollama) and cloud APIs (OpenAI, Google Gemini) via a Bring Your Own Key (BYOK) model.

---

## 📋 Context & Requirements

### Background
To support various deployment modes (local-first off-grid, cost-effective API integration, or high-capacity reasoning), the system needs a unified, pluggable facade for interacting with multiple Large Language Models (LLMs).

### Functional Requirements
- **Unified Interface**: Provide single class `AIManager` that exposes a consistent public API for standard and streaming generations.
- **BYOK Config**: Allow users to input OpenAI/Gemini API keys via the Streamlit UI. Keys should only exist in memory/session state.
- **Model Resolution**: Autodetect active provider and support dynamic model listing/filtering.

---

## 🏗️ Architecture & Design

### Interfaces & Data Flow
```
[Streamlit View] -> [Generators / RAG Pipeline] -> [AIManager] -> [Ollama / OpenAI / Gemini SDKs]
```

#### Key Methods in AIManager:
- `generate(prompt: str, model: str, temperature: float, system: str) -> str`
- `stream_generate(prompt: str, model: str, temperature: float, system: str) -> Generator[str, None, None]`

### Session State Configuration
- `st.session_state.ai_provider`: Active provider (`ollama`, `openai`, `gemini`).
- `st.session_state.openai_api_key`: Active OpenAI key.
- `st.session_state.gemini_api_key`: Active Gemini key.

---

## 🧪 Testing & Verification

### Unit Tests
- `tests/test_ai_manager.py`: Mocks API responses for OpenAI and Gemini clients.
- Verify that correct exceptions are raised when required keys are missing.

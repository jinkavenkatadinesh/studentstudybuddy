# Implementation Plan: Unified AI Manager & BYOK Cloud Support 🛠️

Detailed step-by-step breakdown of how the specification is implemented.

---

## 📅 Milestones & Phases

### Phase 1: Foundation & Requirements
- [x] Create Unified AI Manager class skeleton in `services/ai_manager.py`.
- [x] Configure default model constants in `config.py`.

### Phase 2: Core Implementation
- [x] Integrate Ollama local generation via `services/ollama_manager.py`.
- [x] Integrate OpenAI Chat Completion client.
- [x] Integrate Google GenAI SDK client for Gemini.
- [x] Implement streaming generation support for all three backends.

### Phase 3: Integration & Testing
- [x] Connect Streamlit sidebar components to read/write session state API keys.
- [x] Write unit tests mocking OpenAI and Gemini clients in `tests/test_ai_manager.py`.

---

## 🛠️ Proposed File Changes
List of files modified or created:
- `[NEW]` `services/ai_manager.py`
- `[NEW]` `tests/test_ai_manager.py`
- `[MODIFY]` `app.py`
- `[MODIFY]` `config.py`

---

## ⚠️ Risks & Considerations
- Security risk of exposing API keys (addressed by keeping keys only in Streamlit session state memory and out of code/logs).
- Potential model naming/formatting differences between providers.

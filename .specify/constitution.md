# Student Study Buddy Constitution 📜

This constitution establishes the non-negotiable architectural and software development principles for Student Study Buddy.

---

## 🏛️ Core Principles

### 1. Robust AI Interactivity & Abstraction
- All LLM features must route through the unified `AIManager` facade. No direct LLM API calls are permitted from user interface views.
- Implement both standard and streaming responses to ensure responsive and premium user experiences.

### 2. High-Fidelity Retrieval (RAG)
- RAG operations must use semantic chunking with overlapping contexts to preserve content flow.
- All documents must track and display detailed citation metadata (source file, match score, chunk index) for transparent grounding.

### 3. Local-First & Privacy Compliance
- The system must prioritize local models (Ollama) by default.
- Cloud providers (OpenAI, Gemini) should operate on a "Bring Your Own Key" (BYOK) model. Under no circumstances should API keys be hardcoded or written to persistent files/logs.

---

## 🛠️ Code Quality & Conventions

- **Formatting & Style**: All Python code must strictly pass `ruff` check and format validations.
- **Type Safety**: Type hints should be used for public functions and interface boundaries, verified via `mypy`.
- **Imports**: Organize imports cleanly, grouped by standard library, third-party libraries, and local project modules.

---

## 🧪 Testing Guidelines

- **Unit Testing**: All services, managers, and embedding processing tools must have companion unit tests.
- **Coverage**: Maintain a code coverage rate of at least 20% across all core backend services.
- **Deterministic Runs**: Tests should be isolated from external servers. Cloud LLM calls in tests should be mocked, or test suites should run using local mock classes where necessary.

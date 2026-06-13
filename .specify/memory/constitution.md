# Developer Constitution — Student Study Buddy 📜

This constitution defines the development principles, quality standards, and compliance rules for the **Student Study Buddy** project.

---

## 🏛️ Guiding Principles

1. **User Experience First**: The application must be visually stunning, responsive, and easy to use. Default styling should feel premium and avoid standard browser defaults.
2. **Local & Cloud Harmony**: Maintain seamless compatibility between local execution (Ollama) and cloud providers (OpenAI/Gemini). Never assume one is available over the other.
3. **Clean & Grounded Responses**: AI generations (quizzes, summaries, flashcards) must be strictly grounded in user-provided documents when using RAG.
4. **No Code Left Behind**: Keep components focused, reusable, and document files up to date.

---

## ⚙️ Coding Standards

- **Language**: Python 3.10+
- **Framework**: Streamlit for dashboard frontend & services routing.
- **Type Hinting**: Proactively use type annotations for function signatures.
- **Error Handling**: Use explicit try-except blocks with logger reporting; never silence exceptions silently.
- **Secrets Management**: Absolutely no credentials or API keys committed to repository branches.

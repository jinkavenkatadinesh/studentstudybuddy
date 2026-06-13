# AI Architecture & Agents Specification 🤖

This document outlines the AI and Large Language Model (LLM) architecture within **Student Study Buddy**.

---

## 🏗️ Core AI Components

### 1. Unified AI Manager (`AIManager`)
The `AIManager` acts as a facade pattern over different LLM runtimes. It dynamically handles text generation and token streaming for three providers:
- **Local (Ollama)**: Connects to a locally running Ollama instance via the `ollama` library.
- **OpenAI**: Connects to OpenAI's GPT API.
- **Google Gemini**: Uses the official `google-genai` SDK for Gemini models.

### 2. Retrieval-Augmented Generation (RAG) Pipeline
The `RAGPipeline` class combines vector retrieval and generative AI:
1. Queries the local **FAISS Vector Store** to retrieve the top `k` most relevant chunks for a question.
2. Builds a structured context from source passages.
3. Formulates a grounded query using the `QA_PROMPT` and queries the active LLM.
4. Returns the response along with citation metadata (source file, match score, document ID).

---

## ⚡ Task Generators (Specialized Prompts)

- **Summary Generator**: Adapts prompts based on summary types (`short`, `detailed`, `bullet`, `chapter`) to condense academic text.
- **Quiz Generator**: Formulates prompts requiring valid JSON structures for multiple-choice and true/false questions, including incorrect options and detailed explanations.
- **Flashcard Generator**: Extracts core concepts and defines front/back pairs in JSON formats ready for studying.

# User Manual & Deployment Guide 📚

Welcome to **Student Study Buddy**! This manual details how to navigate the application and deploy it to cloud hosting environments.

---

## 🖥️ Dashboard Navigation

### 1. Home Dashboard
Provides a quick overview of your uploaded documents, study metrics, and shortcuts to start quizzes, flashcards, or chats.

### 2. Upload Materials
Upload PDF, DOCX, or plain TXT files. The app automatically extracts text, splits it into semantic chunks with context overlap, embeds them using `all-MiniLM-L6-v2`, and registers them in the FAISS index.

### 3. Document Library
View all uploaded documents, metadata details (file size, chunks, upload date), and delete materials you no longer need.

### 4. AI Summary
Select a document and generate summaries. You can configure:
- **Summary Type**: Concise Short, Detailed, Bulleted, or Chapter-wise.
- **Download**: Export summaries as plain text (`.txt`).
- **Copy**: Copy content directly to the clipboard.

### 5. Flashcards
Select a document to create interactive study flashcards. Click on any card to flip it and review the answer. Flashcard sets are exportable to CSV and JSON formats.

### 6. Quiz Generator
Test your knowledge with custom quizzes:
- Generate from an **uploaded document** or a **general topic**.
- Configure difficulty (Easy, Medium, Hard).
- Pick question types (Multiple Choice or True/False).
- View instant grading and detailed explanations for every option.

### 7. Ask Documents
A ChatGPT-style interface allowing you to chat directly with your document collection. Each answer includes clickable source citations from your files.

---

## ⚙️ Configuration & API Keys

Select your **AI Provider** in the sidebar:
- **Local (Ollama)**: Requires Ollama running on `http://localhost:11434`. Pull models beforehand (e.g. `ollama pull qwen2.5-coder:1.5b`).
- **OpenAI**: Requires an OpenAI API Key.
- **Google Gemini**: Requires a Gemini API Key.

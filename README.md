# Student Study Buddy 📚

**Student Study Buddy** is a premium, AI-powered learning assistant built with Streamlit. It parses your study materials (PDF, DOCX, TXT) and generates personalized summaries, interactive quizzes, study flashcards, and provides an interactive document Q&A chatbot with citation tracking.

---

## 🌟 Key Features

1. **Document Ingestion**: Seamless PDF, DOCX, and TXT parsing, with text cleaning and overlap-preserving chunking.
2. **FAISS Vector Storage**: Custom vector database implementation supporting incremental indexing, updating, and document deletion.
3. **Bring Your Own Key (BYOK) Cloud LLMs**: Out-of-the-box support for both local models (**Ollama**) and cloud providers (**OpenAI** & **Google Gemini**).
4. **AI Summary Generator**: Short, detailed, bulleted, or chapter-wise summaries of your learning materials.
5. **Flashcard Generator**: Instant flashcards generated from document context, exportable to CSV/JSON.
6. **Quiz Generator**: Generates MCQ and True/False questions dynamically from documents or general topics.
7. **Interactive RAG Chat**: Interactive chatbot with citation sources directly linking back to uploaded materials.
8. **Study Analytics**: A tracking dashboard for documents uploaded, quizzes taken, and performance metrics.

---

## 🛠️ Technology Stack

- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Vector Database**: [FAISS](https://github.com/facebookresearch/faiss)
- **Parsers**: PyPDF2, pdfplumber, python-docx
- **LLM Integrations**: Ollama, OpenAI, Google GenAI SDK

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com/) (Optional, for local inference)

### 2. Clone the Repository
```bash
git clone https://github.com/jinkavenkatadinesh/studentstudybuddy.git
cd studentstudybuddy
```

### 3. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The application will be accessible at `http://localhost:8501` (or the configured port).

---

## ☁️ Deployment

For detailed deployment instructions to **Streamlit Community Cloud** or **Hugging Face Spaces**, refer to the [USER_MANUAL.md](USER_MANUAL.md).

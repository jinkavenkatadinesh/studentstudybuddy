"""Prompt templates for all AI generation tasks."""

# ── Document Q&A ──────────────────────────────────────────────────────────────

QA_SYSTEM_PROMPT = """You are a helpful study assistant. Answer questions based on the provided context from the student's study materials. Be accurate, clear, and educational.

If the context doesn't contain enough information to answer the question, say so honestly. Always cite which parts of the context you used."""

QA_PROMPT = """Use the following context from the student's documents to answer the question.

Context:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the provided context
- Be clear and educational
- If the answer isn't in the context, say "I couldn't find this in your documents"
- Reference the source material when possible

Answer:"""

# ── Chat System ───────────────────────────────────────────────────────────────

CHAT_SYSTEM_PROMPT = """You are Student Study Buddy, an AI learning assistant. You help students understand their study materials by answering questions, explaining concepts, and providing insights based on their uploaded documents.

Be friendly, educational, and thorough. When answering from documents, cite your sources."""

# ── Summary Prompts ───────────────────────────────────────────────────────────

SUMMARY_SHORT_PROMPT = """Provide a concise summary (3-5 sentences) of the following study material:

{text}

Summary:"""

SUMMARY_DETAILED_PROMPT = """Provide a comprehensive and detailed summary of the following study material. Cover all major topics, key concepts, and important details:

{text}

Detailed Summary:"""

SUMMARY_BULLET_PROMPT = """Summarize the following study material as a well-organized bullet-point list. Group related points under topic headers:

{text}

Bullet Summary:"""

SUMMARY_CHAPTER_PROMPT = """Analyze the following study material and create a chapter-wise or section-wise summary. Identify logical sections and summarize each one:

{text}

Chapter-wise Summary:"""

# ── Quiz Prompts ──────────────────────────────────────────────────────────────

QUIZ_MCQ_PROMPT = """Generate exactly {num_questions} multiple-choice questions from the following study material.
Difficulty level: {difficulty}

Study Material:
{context}

Rules:
- Each question must have exactly 4 options
- Only one option should be correct
- Include a brief explanation for the correct answer
- Difficulty guide: easy=recall, medium=understanding, hard=analysis

Return ONLY a valid JSON array. Each object must have:
- "question": the question text
- "options": array of exactly 4 options
- "correct_answer": exact text of correct option (must match one option)
- "explanation": brief explanation why this is correct

Return ONLY the JSON array, no other text."""

QUIZ_TRUE_FALSE_PROMPT = """Generate exactly {num_questions} True/False questions from the following study material.
Difficulty level: {difficulty}

Study Material:
{context}

Rules:
- Each statement should be clearly true or false based on the material
- Include explanations for each answer
- Mix true and false answers roughly equally

Return ONLY a valid JSON array. Each object must have:
- "question": a statement
- "options": ["True", "False"]
- "correct_answer": either "True" or "False"
- "explanation": why this is true or false

Return ONLY the JSON array, no other text."""

# ── Flashcard Prompts ─────────────────────────────────────────────────────────

FLASHCARD_PROMPT = """Generate exactly {num_cards} study flashcards from the following material.
Difficulty level: {difficulty}

Study Material:
{context}

Rules:
- Front: a clear question or concept prompt
- Back: a concise, accurate answer
- Cover key concepts, definitions, and important facts
- Vary question types (what, why, how, define, explain)

Return ONLY a valid JSON array. Each object must have:
- "front": question or concept (flashcard front)
- "back": answer or explanation (flashcard back)
- "difficulty": "{difficulty}"

Return ONLY the JSON array, no other text."""

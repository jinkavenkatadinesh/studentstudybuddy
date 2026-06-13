"""Data models for all entities in Student Study Buddy."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


# ── Document Models ───────────────────────────────────────────────────────────

@dataclass
class Document:
    """Represents an uploaded study document."""
    id: str
    filename: str
    filepath: str
    file_type: str  # pdf, docx, txt
    file_size: int  # bytes
    upload_time: float = field(default_factory=time.time)
    num_pages: int = 0
    num_chunks: int = 0
    content_hash: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "upload_time": self.upload_time,
            "num_pages": self.num_pages,
            "num_chunks": self.num_chunks,
            "content_hash": self.content_hash,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Document:
        return cls(**data)


@dataclass
class TextChunk:
    """A chunk of text from a parsed document."""
    content: str
    doc_id: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


# ── Quiz Models ───────────────────────────────────────────────────────────────

@dataclass
class Question:
    """A single quiz question (MCQ or True/False)."""
    question: str
    options: list[str]
    correct_answer: str
    explanation: str = ""
    difficulty: str = "medium"
    question_type: str = "mcq"  # "mcq" or "true_false"

    def is_correct(self, user_answer: str) -> bool:
        return user_answer.strip().lower() == self.correct_answer.strip().lower()


@dataclass
class Quiz:
    """A complete quiz with metadata and questions."""
    topic: str
    questions: list[Question]
    difficulty: str = "medium"
    doc_id: str = ""
    question_type: str = "mcq"
    created_at: float = field(default_factory=time.time)

    @property
    def num_questions(self) -> int:
        return len(self.questions)


@dataclass
class QuizResult:
    """Results from a completed quiz attempt."""
    quiz: Quiz
    user_answers: list[str]
    score: int = 0
    total: int = 0
    time_taken: float = 0.0
    per_question: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.total = len(self.quiz.questions)

    def calculate(self) -> QuizResult:
        """Calculate score and per-question breakdown."""
        self.score = 0
        self.per_question = []
        for i, question in enumerate(self.quiz.questions):
            user_ans = self.user_answers[i] if i < len(self.user_answers) else ""
            is_correct = question.is_correct(user_ans)
            if is_correct:
                self.score += 1
            self.per_question.append({
                "question": question.question,
                "options": question.options,
                "user_answer": user_ans,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation,
            })
        return self

    @property
    def percentage(self) -> float:
        return (self.score / self.total * 100) if self.total > 0 else 0

    @property
    def grade(self) -> str:
        pct = self.percentage
        if pct >= 80:
            return "excellent"
        elif pct >= 60:
            return "good"
        elif pct >= 40:
            return "average"
        return "poor"


# ── Flashcard Models ──────────────────────────────────────────────────────────

@dataclass
class Flashcard:
    """A single flashcard with front (question) and back (answer)."""
    front: str
    back: str
    difficulty: str = "medium"
    topic: str = ""


@dataclass
class FlashcardSet:
    """A set of flashcards generated from a document."""
    cards: list[Flashcard]
    topic: str = ""
    doc_id: str = ""
    created_at: float = field(default_factory=time.time)


# ── Summary Models ────────────────────────────────────────────────────────────

@dataclass
class Summary:
    """An AI-generated summary of a document."""
    content: str
    summary_type: str  # short, detailed, bullet, chapter
    doc_id: str = ""
    created_at: float = field(default_factory=time.time)


# ── Chat Models ───────────────────────────────────────────────────────────────

@dataclass
class ChatMessage:
    """A single message in a chat conversation."""
    role: str  # "user" or "assistant"
    content: str
    sources: list[dict] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


# ── Analytics Models ──────────────────────────────────────────────────────────

@dataclass
class AnalyticsData:
    """Aggregated analytics data."""
    documents_uploaded: int = 0
    quizzes_completed: int = 0
    avg_score: float = 0.0
    flashcards_generated: int = 0
    summaries_generated: int = 0
    quiz_history: list[dict] = field(default_factory=list)
    total_questions_answered: int = 0
    total_correct: int = 0

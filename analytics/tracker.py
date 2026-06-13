"""Analytics tracker — tracks usage statistics and learning metrics."""

from __future__ import annotations

import json
import time
from pathlib import Path

from config import ANALYTICS_FILE
from models.schemas import AnalyticsData, QuizResult
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AnalyticsTracker:
    """Tracks and persists user learning analytics."""

    def __init__(self):
        self._data: dict = {
            "documents_uploaded": 0,
            "quizzes_completed": 0,
            "flashcards_generated": 0,
            "summaries_generated": 0,
            "total_questions_answered": 0,
            "total_correct": 0,
            "quiz_history": [],
        }
        self._load()

    def _load(self):
        path = Path(ANALYTICS_FILE)
        if path.exists():
            try:
                with open(path, "r") as f:
                    self._data.update(json.load(f))
            except Exception as e:
                logger.error("Failed to load analytics: %s", e)

    def _save(self):
        try:
            with open(ANALYTICS_FILE, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            logger.error("Failed to save analytics: %s", e)

    def track_upload(self):
        self._data["documents_uploaded"] += 1
        self._save()

    def track_quiz(self, quiz_result: QuizResult):
        self._data["quizzes_completed"] += 1
        self._data["total_questions_answered"] += quiz_result.total
        self._data["total_correct"] += quiz_result.score
        self._data["quiz_history"].append(
            {
                "topic": quiz_result.quiz.topic,
                "score": quiz_result.score,
                "total": quiz_result.total,
                "percentage": round(quiz_result.percentage, 1),
                "difficulty": quiz_result.quiz.difficulty,
                "type": quiz_result.quiz.question_type,
                "timestamp": time.time(),
            }
        )
        # Keep last 100 entries
        self._data["quiz_history"] = self._data["quiz_history"][-100:]
        self._save()

    def track_flashcards(self, count: int):
        self._data["flashcards_generated"] += count
        self._save()

    def track_summary(self):
        self._data["summaries_generated"] += 1
        self._save()

    def get_stats(self) -> AnalyticsData:
        total_q = self._data["total_questions_answered"]
        total_c = self._data["total_correct"]
        avg = (total_c / total_q * 100) if total_q > 0 else 0

        return AnalyticsData(
            documents_uploaded=self._data["documents_uploaded"],
            quizzes_completed=self._data["quizzes_completed"],
            avg_score=round(avg, 1),
            flashcards_generated=self._data["flashcards_generated"],
            summaries_generated=self._data["summaries_generated"],
            quiz_history=self._data["quiz_history"],
            total_questions_answered=total_q,
            total_correct=total_c,
        )

    def get_quiz_history(self) -> list[dict]:
        return self._data.get("quiz_history", [])

"""Quiz generator — generates MCQ and True/False quizzes from documents."""

from __future__ import annotations

import json
import re

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from models.schemas import Question, Quiz, QuizResult
from rag.pipeline import RAGPipeline
from rag.prompts import QUIZ_MCQ_PROMPT, QUIZ_TRUE_FALSE_PROMPT
from services.ai_manager import AIManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class QuizGenerator:
    """Generates quizzes from document content using AI."""

    def __init__(self, rag_pipeline: RAGPipeline, ai_manager: AIManager):
        self.rag = rag_pipeline
        self.ai = ai_manager

    def generate_mcq(
        self,
        doc_id: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Quiz:
        """Generate MCQ quiz from a document."""
        context = self.rag.get_document_context(doc_id)
        if not context:
            raise ValueError("No content found for this document.")

        prompt = QUIZ_MCQ_PROMPT.format(num_questions=num_questions, difficulty=difficulty, context=context)
        raw = self.ai.generate(prompt, model=model, temperature=temperature)
        questions = self._parse_questions(raw, "mcq")

        return Quiz(
            topic="Quiz from document",
            questions=questions[:num_questions],
            difficulty=difficulty,
            doc_id=doc_id,
            question_type="mcq",
        )

    def generate_true_false(
        self,
        doc_id: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Quiz:
        """Generate True/False quiz from a document."""
        context = self.rag.get_document_context(doc_id)
        if not context:
            raise ValueError("No content found for this document.")

        prompt = QUIZ_TRUE_FALSE_PROMPT.format(num_questions=num_questions, difficulty=difficulty, context=context)
        raw = self.ai.generate(prompt, model=model, temperature=temperature)
        questions = self._parse_questions(raw, "true_false")

        return Quiz(
            topic="True/False Quiz",
            questions=questions[:num_questions],
            difficulty=difficulty,
            doc_id=doc_id,
            question_type="true_false",
        )

    def generate_from_topic(
        self,
        topic: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        question_type: str = "mcq",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Quiz:
        """Generate quiz from a topic (no document context)."""
        if question_type == "true_false":
            prompt_template = QUIZ_TRUE_FALSE_PROMPT
        else:
            prompt_template = QUIZ_MCQ_PROMPT

        prompt = prompt_template.format(
            num_questions=num_questions,
            difficulty=difficulty,
            context=f"Topic: {topic}\n\nGenerate questions about this topic using your knowledge.",
        )
        raw = self.ai.generate(prompt, model=model, temperature=temperature)
        questions = self._parse_questions(raw, question_type)

        return Quiz(
            topic=topic,
            questions=questions[:num_questions],
            difficulty=difficulty,
            question_type=question_type,
        )

    def evaluate_quiz(self, quiz: Quiz, user_answers: list[str]) -> QuizResult:
        """Evaluate a quiz attempt and calculate results."""
        result = QuizResult(quiz=quiz, user_answers=user_answers)
        result.calculate()
        return result

    def _parse_questions(self, raw_text: str, q_type: str) -> list[Question]:
        """Parse AI response into Question objects."""
        text = raw_text.strip()

        # Extract JSON from code fences
        code_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if code_match:
            text = code_match.group(1).strip()

        # Find JSON array
        if not text.startswith("["):
            arr_match = re.search(r"\[.*\]", text, re.DOTALL)
            if arr_match:
                text = arr_match.group(0)

        # Fix common JSON issues
        text = re.sub(r",\s*([}\]])", r"\1", text)

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.error("Failed to parse quiz JSON: %s", text[:500])
            raise ValueError("Could not parse AI response as valid quiz JSON.")

        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of questions.")

        questions = []
        for item in data:
            if not isinstance(item, dict):
                continue
            q_text = item.get("question", "")
            options = item.get("options", [])
            correct = item.get("correct_answer", "")
            explanation = item.get("explanation", "")

            if not q_text or not options or not correct:
                continue

            options = [str(o) for o in options]

            # Ensure correct answer matches an option
            if correct not in options:
                for opt in options:
                    if opt.strip().lower() == correct.strip().lower():
                        correct = opt
                        break
                else:
                    correct = options[0]

            questions.append(
                Question(
                    question=q_text,
                    options=options,
                    correct_answer=correct,
                    explanation=explanation,
                    difficulty=item.get("difficulty", "medium"),
                    question_type=q_type,
                )
            )

        if not questions:
            raise ValueError("No valid questions found in AI response.")
        return questions

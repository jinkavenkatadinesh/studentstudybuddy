"""Flashcard generator — creates study flashcards from documents."""

from __future__ import annotations

import csv
import io
import json
import re

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from models.schemas import Flashcard, FlashcardSet
from rag.pipeline import RAGPipeline
from rag.prompts import FLASHCARD_PROMPT
from services.ai_manager import AIManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FlashcardGenerator:
    """Generates study flashcards from document content."""

    def __init__(self, rag_pipeline: RAGPipeline, ai_manager: AIManager):
        self.rag = rag_pipeline
        self.ai = ai_manager

    def generate(
        self,
        doc_id: str,
        num_cards: int = 10,
        difficulty: str = "medium",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> FlashcardSet:
        """Generate flashcards from a document."""
        context = self.rag.get_document_context(doc_id)
        if not context:
            raise ValueError("No content found for this document.")

        prompt = FLASHCARD_PROMPT.format(num_cards=num_cards, difficulty=difficulty, context=context)
        raw = self.ai.generate(prompt, model=model, temperature=temperature)
        cards = self._parse_flashcards(raw, difficulty)

        return FlashcardSet(
            cards=cards[:num_cards],
            topic="Flashcards from document",
            doc_id=doc_id,
        )

    def generate_from_text(
        self,
        text: str,
        num_cards: int = 10,
        difficulty: str = "medium",
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> FlashcardSet:
        """Generate flashcards from raw text."""
        prompt = FLASHCARD_PROMPT.format(num_cards=num_cards, difficulty=difficulty, context=text[:5000])
        raw = self.ai.generate(prompt, model=model, temperature=temperature)
        cards = self._parse_flashcards(raw, difficulty)
        return FlashcardSet(cards=cards[:num_cards], topic="Custom flashcards")

    def export_json(self, flashcard_set: FlashcardSet) -> str:
        """Export flashcards as JSON string."""
        data = [{"front": c.front, "back": c.back, "difficulty": c.difficulty} for c in flashcard_set.cards]
        return json.dumps(data, indent=2)

    def export_csv(self, flashcard_set: FlashcardSet) -> str:
        """Export flashcards as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Front", "Back", "Difficulty"])
        for card in flashcard_set.cards:
            writer.writerow([card.front, card.back, card.difficulty])
        return output.getvalue()

    def _parse_flashcards(self, raw_text: str, default_difficulty: str = "medium") -> list[Flashcard]:
        """Parse AI response into Flashcard objects."""
        text = raw_text.strip()

        code_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if code_match:
            text = code_match.group(1).strip()

        if not text.startswith("["):
            arr_match = re.search(r"\[.*\]", text, re.DOTALL)
            if arr_match:
                text = arr_match.group(0)

        text = re.sub(r",\s*([}\]])", r"\1", text)

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.error("Failed to parse flashcard JSON")
            raise ValueError("Could not parse AI response as flashcards.")

        cards = []
        for item in data:
            if not isinstance(item, dict):
                continue
            front = item.get("front", "")
            back = item.get("back", "")
            if front and back:
                cards.append(
                    Flashcard(
                        front=front,
                        back=back,
                        difficulty=item.get("difficulty", default_difficulty),
                    )
                )
        if not cards:
            raise ValueError("No valid flashcards found in AI response.")
        return cards

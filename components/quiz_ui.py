"""Quiz UI component — question display and results."""

import streamlit as st

from models.schemas import Question, QuizResult


def render_question(question: Question, index: int, total: int):
    """Render a single quiz question with radio options."""
    st.markdown(
        f"""
    <div class="question-card">
        <div class="question-number">Question {index + 1} of {total}</div>
        <div class="question-text">{question.question}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    answer = st.radio(
        f"Select your answer for Q{index + 1}:",
        question.options,
        key=f"quiz_q_{index}",
        index=None,
        label_visibility="collapsed",
    )
    return answer


def render_quiz_progress(current: int, total: int):
    """Render quiz progress indicator."""
    progress = current / total if total > 0 else 0
    st.progress(progress)
    st.markdown(
        f'<div style="text-align:center;color:#94A3B8;font-size:0.85rem;">'
        f"Answered {current} of {total} questions</div>",
        unsafe_allow_html=True,
    )


def render_quiz_results(result: QuizResult):
    """Render the quiz results dashboard."""
    # Score card
    grade_colors = {"excellent": "#10B981", "good": "#3B82F6", "average": "#F59E0B", "poor": "#EF4444"}
    grade_emojis = {"excellent": "🌟", "good": "👍", "average": "📚", "poor": "💪"}
    color = grade_colors.get(result.grade, "#94A3B8")
    emoji = grade_emojis.get(result.grade, "📊")

    st.markdown(
        f"""
    <div class="score-card">
        <div style="font-size:3rem;margin-bottom:0.5rem;">{emoji}</div>
        <div class="score-number">{result.percentage:.0f}%</div>
        <div class="score-label">{result.score} / {result.total} correct</div>
        <div style="margin-top:0.5rem;color:{color};font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">
            {result.grade}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Per-question breakdown
    st.markdown("### 📋 Question Breakdown")
    for i, pq in enumerate(result.per_question):
        css_class = "result-correct" if pq["is_correct"] else "result-incorrect"
        icon = "✅" if pq["is_correct"] else "❌"
        st.markdown(
            f"""
        <div class="{css_class}">
            <strong>{icon} Q{i + 1}: {pq["question"]}</strong><br>
            <span style="color:#94A3B8;">Your answer:</span> {pq["user_answer"] or "(unanswered)"}<br>
            <span style="color:#94A3B8;">Correct answer:</span> <strong style="color:#10B981;">{pq["correct_answer"]}</strong>
            {"<br><span style='color:#94A3B8;font-size:0.85rem;'>" + pq["explanation"] + "</span>" if pq.get("explanation") else ""}
        </div>
        """,
            unsafe_allow_html=True,
        )

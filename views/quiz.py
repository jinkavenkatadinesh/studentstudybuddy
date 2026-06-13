"""Quiz Generator page."""

import time
import streamlit as st
from components.quiz_ui import render_question, render_quiz_progress, render_quiz_results
from config import DIFFICULTY_LEVELS, DEFAULT_NUM_QUESTIONS, MIN_NUM_QUESTIONS, MAX_NUM_QUESTIONS


def render_quiz():
    """Render the quiz generator page."""
    st.markdown("### 🧪 Quiz Generator")

    # If we have quiz results, show them
    if st.session_state.get("quiz_result"):
        _render_results()
        return

    # If we have an active quiz, show it
    if st.session_state.get("active_quiz"):
        _render_active_quiz()
        return

    # Otherwise show the generation form
    _render_quiz_form()


def _render_quiz_form():
    """Render the quiz configuration form."""
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1.5rem;">Generate quizzes from your documents or any topic.</div>',
        unsafe_allow_html=True,
    )

    file_mgr = st.session_state.get("file_manager")
    quiz_gen = st.session_state.get("quiz_generator")

    # Source selection
    source = st.radio("Quiz Source", ["From Document", "From Topic"], horizontal=True, key="quiz_source")

    doc_id = None
    topic = ""
    if source == "From Document":
        if not file_mgr or not file_mgr.list_documents():
            st.info("📤 Upload documents first to generate quizzes from them.")
            return
        docs = file_mgr.list_documents()
        doc_options = {f"{d.filename}": d.id for d in docs}
        selected = st.selectbox("Select Document", list(doc_options.keys()), key="quiz_doc")
        doc_id = doc_options[selected]
    else:
        topic = st.text_input("Enter Topic", placeholder="e.g., Python Data Structures", key="quiz_topic")

    # Quiz config
    col1, col2, col3 = st.columns(3)
    with col1:
        q_type = st.selectbox("Question Type", ["MCQ", "True/False"], key="quiz_type")
    with col2:
        num_q = st.slider("Questions", MIN_NUM_QUESTIONS, MAX_NUM_QUESTIONS, DEFAULT_NUM_QUESTIONS, key="quiz_num")
    with col3:
        difficulty = st.select_slider("Difficulty", DIFFICULTY_LEVELS, value="medium", key="quiz_diff")

    # Generate
    if st.button("✨ Generate Quiz", type="primary", use_container_width=True):
        if not quiz_gen:
            st.error("AI service not available. Is Ollama running?")
            return
        if source == "From Topic" and not topic:
            st.error("Please enter a topic.")
            return

        with st.spinner(f"Generating {num_q} {q_type} questions..."):
            try:
                model = st.session_state.get("selected_model", "qwen3:8b")
                temp = st.session_state.get("temperature", 0.7)
                qtype = "true_false" if q_type == "True/False" else "mcq"

                if source == "From Document":
                    if qtype == "true_false":
                        quiz = quiz_gen.generate_true_false(doc_id, num_q, difficulty, model=model, temperature=temp)
                    else:
                        quiz = quiz_gen.generate_mcq(doc_id, num_q, difficulty, model=model, temperature=temp)
                else:
                    quiz = quiz_gen.generate_from_topic(topic, num_q, difficulty, qtype, model=model, temperature=temp)

                st.session_state.active_quiz = quiz
                st.session_state.quiz_start_time = time.time()
                st.session_state.quiz_result = None
                st.rerun()
            except Exception as e:
                st.error(f"Failed to generate quiz: {e}")


def _render_active_quiz():
    """Render the active quiz with all questions."""
    quiz = st.session_state.active_quiz
    st.markdown(f"**Topic:** {quiz.topic} | **Difficulty:** {quiz.difficulty.upper()} | **Type:** {quiz.question_type.upper()}")

    answers = {}
    answered_count = 0

    for i, question in enumerate(quiz.questions):
        answer = render_question(question, i, len(quiz.questions))
        if answer:
            answers[i] = answer
            answered_count += 1

    render_quiz_progress(answered_count, len(quiz.questions))

    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 Submit Quiz", type="primary", use_container_width=True):
            quiz_gen = st.session_state.get("quiz_generator")
            analytics = st.session_state.get("analytics_tracker")

            user_answers = [answers.get(i, "") for i in range(len(quiz.questions))]
            result = quiz_gen.evaluate_quiz(quiz, user_answers)
            result.time_taken = round(time.time() - st.session_state.get("quiz_start_time", time.time()), 1)

            st.session_state.quiz_result = result
            if analytics:
                analytics.track_quiz(result)
            st.rerun()

    if st.button("← Cancel Quiz", key="cancel_quiz"):
        st.session_state.active_quiz = None
        st.rerun()


def _render_results():
    """Render quiz results."""
    result = st.session_state.quiz_result
    render_quiz_results(result)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.active_quiz = None
            st.session_state.quiz_result = None
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.active_quiz = None
            st.session_state.quiz_result = None
            st.session_state.current_page = "home"
            st.rerun()

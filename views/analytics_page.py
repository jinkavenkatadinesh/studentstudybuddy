"""Study Analytics page."""

import streamlit as st

from components.metrics import render_difficulty_chart, render_metric_card, render_quiz_history_chart


def render_analytics():
    """Render the study analytics page."""
    st.markdown("### 📊 Study Analytics")
    st.markdown(
        '<div style="color:#94A3B8;margin-bottom:1.5rem;">Track your learning progress and performance metrics.</div>',
        unsafe_allow_html=True,
    )

    analytics = st.session_state.get("analytics_tracker")
    if not analytics:
        st.error("Analytics not available.")
        return

    stats = analytics.get_stats()
    st.session_state.analytics_stats = stats

    # Top stats row
    cols = st.columns(5)
    metrics = [
        ("📄", "Documents", stats.documents_uploaded),
        ("🧪", "Quizzes", stats.quizzes_completed),
        ("📊", "Avg Score", f"{stats.avg_score:.0f}%"),
        ("🃏", "Flashcards", stats.flashcards_generated),
        ("📝", "Summaries", stats.summaries_generated),
    ]
    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            render_metric_card(icon, label, value)

    st.markdown("<br>", unsafe_allow_html=True)

    # Additional stats
    col1, col2 = st.columns(2)
    with col1:
        render_metric_card("❓", "Questions Answered", stats.total_questions_answered)
    with col2:
        render_metric_card("✅", "Correct Answers", stats.total_correct)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    history = stats.quiz_history

    if history:
        st.markdown("#### 📈 Quiz Score Progress")
        render_quiz_history_chart(history)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎯 Difficulty Distribution")
            render_difficulty_chart(history)
        with col2:
            st.markdown("#### 📋 Recent Quizzes")
            for h in reversed(history[-5:]):
                score_color = "#10B981" if h["percentage"] >= 60 else "#EF4444"
                st.markdown(
                    f"""
                <div class="doc-card">
                    <div class="doc-name">{h['topic']}</div>
                    <div class="doc-meta">
                        <span style="color:{score_color};font-weight:700;">{h['percentage']:.0f}%</span>
                        · {h['score']}/{h['total']} · {h['difficulty']} · {h.get('type', 'mcq').upper()}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">📊</div>'
            '<div class="empty-state-text">Take quizzes to see your analytics!</div>'
            "</div>",
            unsafe_allow_html=True,
        )

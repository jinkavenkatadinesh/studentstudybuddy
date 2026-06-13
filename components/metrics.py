"""Metrics and charts UI components."""

import streamlit as st
import plotly.graph_objects as go
from models.schemas import AnalyticsData


def render_metric_card(icon: str, label: str, value, color: str = "#7C3AED"):
    """Render a styled metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_row(stats: AnalyticsData):
    """Render a row of key metric cards."""
    cols = st.columns(4)
    metrics = [
        ("📄", "Documents", stats.documents_uploaded),
        ("🧪", "Quizzes", stats.quizzes_completed),
        ("📊", "Avg Score", f"{stats.avg_score:.0f}%"),
        ("🃏", "Flashcards", stats.flashcards_generated),
    ]
    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            render_metric_card(icon, label, value)


def render_quiz_history_chart(history: list[dict]):
    """Render a quiz score over time line chart."""
    if not history:
        st.info("No quiz history yet. Take a quiz to see your progress!")
        return

    scores = [h["percentage"] for h in history]
    labels = [f"Quiz {i+1}" for i in range(len(history))]
    difficulties = [h.get("difficulty", "medium") for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=scores,
        mode='lines+markers',
        line=dict(color='#7C3AED', width=3),
        marker=dict(size=10, color='#EC4899', line=dict(width=2, color='#7C3AED')),
        text=[f"{s:.0f}% ({d})" for s, d in zip(scores, difficulties)],
        hoverinfo='text+x',
        fill='tozeroy',
        fillcolor='rgba(124,58,237,0.1)',
    ))
    fig.update_layout(
        title=None,
        xaxis_title="", yaxis_title="Score %",
        yaxis=dict(range=[0, 105]),
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=40, r=20, t=20, b=40),
        font=dict(family="Inter", color="#94A3B8"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_difficulty_chart(history: list[dict]):
    """Render a difficulty distribution pie chart."""
    if not history:
        return

    diff_counts = {}
    for h in history:
        d = h.get("difficulty", "medium")
        diff_counts[d] = diff_counts.get(d, 0) + 1

    colors = {"easy": "#10B981", "medium": "#F59E0B", "hard": "#EF4444"}
    fig = go.Figure(data=[go.Pie(
        labels=list(diff_counts.keys()),
        values=list(diff_counts.values()),
        marker=dict(colors=[colors.get(d, "#7C3AED") for d in diff_counts.keys()]),
        hole=0.5,
        textinfo='label+percent',
        textfont=dict(size=13),
    )])
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Inter", color="#94A3B8"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

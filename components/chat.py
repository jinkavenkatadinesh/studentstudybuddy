"""Chat UI component — ChatGPT-style conversation interface."""

import streamlit as st

from models.schemas import ChatMessage


def render_chat_message(message: ChatMessage):
    """Render a single chat message bubble."""
    if message.role == "user":
        st.markdown(
            f'<div class="chat-user">{message.content}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-assistant">{message.content}</div>',
            unsafe_allow_html=True,
        )
        if message.sources:
            render_sources(message.sources)


def render_sources(sources: list[dict]):
    """Render source citations in an expander."""
    with st.expander(f"📎 {len(sources)} Source(s) Referenced", expanded=False):
        for i, src in enumerate(sources):
            source_name = src.get("source", "Unknown")
            content = src.get("content", "")
            score = src.get("score", 0)
            st.markdown(
                f'<div class="source-citation">'
                f"<strong>Source {i+1}</strong> — {source_name} "
                f'<span style="color:#7C3AED;">(relevance: {score:.2f})</span><br>'
                f'<span style="font-size:0.83rem;">{content}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )


def render_chat_history(messages: list[ChatMessage]):
    """Render the full chat history."""
    if not messages:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">💬</div>'
            '<div class="empty-state-text">Start a conversation with your documents!</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        return

    for msg in messages:
        render_chat_message(msg)

"""Flashcard UI component — flip-card display with navigation."""

import streamlit as st
from models.schemas import Flashcard, FlashcardSet


def render_flashcard(card: Flashcard, index: int, is_flipped: bool = False):
    """Render a single flashcard with flip animation."""
    flipped_class = "flipped" if is_flipped else ""
    st.markdown(f"""
    <div class="flashcard-container">
        <div class="flashcard {flipped_class}">
            <div class="flashcard-front">
                <div>
                    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);margin-bottom:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">
                        Question {index + 1}
                    </div>
                    {card.front}
                </div>
            </div>
            <div class="flashcard-back">
                <div>
                    <div style="font-size:0.75rem;color:#7C3AED;margin-bottom:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">
                        Answer
                    </div>
                    {card.back}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_flashcard_navigation(total: int, current: int):
    """Render Previous/Next buttons and progress."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Prev", key="fc_prev", disabled=current <= 0, use_container_width=True):
            st.session_state.fc_current = max(0, current - 1)
            st.session_state.fc_flipped = False
            st.rerun()
    with col2:
        st.markdown(f'<div style="text-align:center;color:#94A3B8;padding:0.5rem;font-weight:600;">Card {current + 1} of {total}</div>', unsafe_allow_html=True)
        st.progress((current + 1) / total if total > 0 else 0)
    with col3:
        if st.button("Next →", key="fc_next", disabled=current >= total - 1, use_container_width=True):
            st.session_state.fc_current = min(total - 1, current + 1)
            st.session_state.fc_flipped = False
            st.rerun()


def render_flashcard_set(flashcard_set: FlashcardSet):
    """Render full flashcard set with navigation."""
    if not flashcard_set.cards:
        st.info("No flashcards to display.")
        return
    if "fc_current" not in st.session_state:
        st.session_state.fc_current = 0
    if "fc_flipped" not in st.session_state:
        st.session_state.fc_flipped = False

    current = st.session_state.fc_current
    if current >= len(flashcard_set.cards):
        current = 0
        st.session_state.fc_current = 0
    card = flashcard_set.cards[current]

    render_flashcard(card, current, st.session_state.fc_flipped)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        flip_label = "🔄 Flip Card" if not st.session_state.fc_flipped else "🔄 Show Question"
        if st.button(flip_label, key="fc_flip", use_container_width=True, type="primary"):
            st.session_state.fc_flipped = not st.session_state.fc_flipped
            st.rerun()

    render_flashcard_navigation(len(flashcard_set.cards), current)

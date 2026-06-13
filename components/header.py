"""Header component — app branding, global CSS design system."""

import streamlit as st


def render_header():
    """Render the app header and inject the global CSS design system."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ── Base ──────────────────────────────────────── */
        .stApp { font-family: 'Inter', sans-serif; }

        /* ── Header ────────────────────────────────────── */
        .app-header {
            text-align: center;
            padding: 2rem 1rem 1.5rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(236,72,153,0.10) 50%, rgba(59,130,246,0.10));
            border-radius: 20px;
            border: 1px solid rgba(124,58,237,0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        .app-header::before {
            content: '';
            position: absolute; top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(124,58,237,0.08), transparent 50%);
            animation: pulse-glow 4s ease-in-out infinite;
        }
        @keyframes pulse-glow {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 1; }
        }
        .app-title {
            font-size: 2.5rem; font-weight: 800;
            background: linear-gradient(135deg, #7C3AED, #EC4899 50%, #3B82F6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative; z-index: 1; letter-spacing: -0.02em;
        }
        .app-subtitle {
            font-size: 1.1rem; color: #94A3B8; font-weight: 400;
            position: relative; z-index: 1;
        }

        /* ── Sidebar ───────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F0F1A, #1A1A2E);
            border-right: 1px solid rgba(124,58,237,0.15);
        }
        .sidebar-section {
            font-size: 0.78rem; font-weight: 700; color: #7C3AED;
            text-transform: uppercase; letter-spacing: 0.08em;
            margin-top: 1rem; margin-bottom: 0.5rem;
        }
        .sidebar-divider {
            border: none; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(124,58,237,0.3), transparent);
            margin: 1.2rem 0;
        }
        .nav-item {
            display: block; padding: 0.65rem 1rem;
            border-radius: 10px; margin: 0.15rem 0;
            color: #94A3B8; text-decoration: none;
            transition: all 0.25s ease; cursor: pointer;
            font-size: 0.92rem; font-weight: 500;
        }
        .nav-item:hover { background: rgba(124,58,237,0.12); color: #E2E8F0; }
        .nav-item.active {
            background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(124,58,237,0.10));
            color: #C4B5FD; border-left: 3px solid #7C3AED;
        }

        /* ── Buttons ───────────────────────────────────── */
        .stButton > button {
            border-radius: 12px; font-weight: 600;
            padding: 0.6rem 1.5rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(124,58,237,0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(124,58,237,0.25);
        }

        /* ── Cards ─────────────────────────────────────── */
        .glass-card {
            background: linear-gradient(135deg, rgba(30,30,50,0.7), rgba(20,20,35,0.9));
            border: 1px solid rgba(124,58,237,0.12);
            border-radius: 16px; padding: 1.5rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-3px);
            border-color: rgba(124,58,237,0.35);
            box-shadow: 0 8px 30px rgba(124,58,237,0.12);
        }

        /* ── Metric Cards ──────────────────────────────── */
        .metric-card {
            background: linear-gradient(135deg, rgba(30,30,50,0.8), rgba(20,20,35,0.9));
            border: 1px solid rgba(124,58,237,0.15);
            border-radius: 16px; padding: 1.25rem; text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(124,58,237,0.12);
        }
        .metric-icon { font-size: 2rem; margin-bottom: 0.4rem; }
        .metric-value {
            font-size: 1.8rem; font-weight: 800;
            background: linear-gradient(135deg, #7C3AED, #EC4899);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .metric-label { font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem; }

        /* ── Feature Cards ─────────────────────────────── */
        .feature-card {
            background: linear-gradient(135deg, rgba(30,30,50,0.6), rgba(20,20,35,0.8));
            border: 1px solid rgba(124,58,237,0.12);
            border-radius: 16px; padding: 1.5rem; text-align: center;
            transition: all 0.3s ease; cursor: pointer;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            border-color: rgba(124,58,237,0.4);
            box-shadow: 0 8px 30px rgba(124,58,237,0.15);
        }
        .feature-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
        .feature-title { font-size: 1.05rem; font-weight: 700; color: #E2E8F0; margin-bottom: 0.4rem; }
        .feature-desc { font-size: 0.88rem; color: #94A3B8; line-height: 1.5; }

        /* ── Chat Bubbles ──────────────────────────────── */
        .chat-user {
            background: linear-gradient(135deg, #7C3AED, #6D28D9);
            color: white; padding: 1rem 1.25rem; border-radius: 16px 16px 4px 16px;
            margin: 0.5rem 0; max-width: 85%; margin-left: auto;
            font-size: 0.95rem; line-height: 1.6;
        }
        .chat-assistant {
            background: linear-gradient(135deg, rgba(30,30,50,0.8), rgba(20,20,35,0.9));
            border: 1px solid rgba(124,58,237,0.15);
            color: #E2E8F0; padding: 1rem 1.25rem;
            border-radius: 16px 16px 16px 4px;
            margin: 0.5rem 0; max-width: 85%;
            font-size: 0.95rem; line-height: 1.6;
        }

        /* ── Flashcard ─────────────────────────────────── */
        .flashcard-container {
            perspective: 1000px; margin: 1rem auto; max-width: 500px;
        }
        .flashcard {
            min-height: 250px; position: relative;
            transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer;
        }
        .flashcard.flipped { transform: rotateY(180deg); }
        .flashcard-front, .flashcard-back {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            backface-visibility: hidden; border-radius: 20px; padding: 2rem;
            display: flex; align-items: center; justify-content: center;
            text-align: center; font-size: 1.1rem; line-height: 1.6;
        }
        .flashcard-front {
            background: linear-gradient(135deg, #7C3AED, #6D28D9);
            color: white; font-weight: 600;
            border: 2px solid rgba(124,58,237,0.4);
        }
        .flashcard-back {
            background: linear-gradient(135deg, rgba(30,30,50,0.9), rgba(20,20,35,1));
            color: #E2E8F0;
            border: 2px solid rgba(124,58,237,0.3);
            transform: rotateY(180deg);
        }

        /* ── Quiz Question ─────────────────────────────── */
        .question-card {
            background: linear-gradient(135deg, rgba(30,30,50,0.7), rgba(20,20,35,0.9));
            border: 1px solid rgba(124,58,237,0.15);
            border-radius: 16px; padding: 2rem; margin: 1rem 0;
        }
        .question-number {
            font-size: 0.85rem; font-weight: 600; color: #7C3AED;
            text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;
        }
        .question-text {
            font-size: 1.15rem; font-weight: 600; color: #E2E8F0; line-height: 1.6;
        }

        /* ── Result Items ──────────────────────────────── */
        .result-correct {
            border-left: 4px solid #10B981;
            background: rgba(16,185,129,0.05);
            padding: 1rem 1.5rem; border-radius: 0 12px 12px 0; margin: 0.75rem 0;
        }
        .result-incorrect {
            border-left: 4px solid #EF4444;
            background: rgba(239,68,68,0.05);
            padding: 1rem 1.5rem; border-radius: 0 12px 12px 0; margin: 0.75rem 0;
        }

        /* ── Score Card ────────────────────────────────── */
        .score-card {
            text-align: center; padding: 2rem;
            background: linear-gradient(135deg, rgba(30,30,50,0.8), rgba(20,20,35,0.9));
            border-radius: 20px; border: 1px solid rgba(124,58,237,0.2); margin: 1rem 0;
        }
        .score-number {
            font-size: 4rem; font-weight: 900;
            background: linear-gradient(135deg, #7C3AED, #EC4899);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .score-label { font-size: 1.2rem; color: #94A3B8; margin-top: 0.5rem; }

        /* ── Progress Bar ──────────────────────────────── */
        .stProgress > div > div {
            background: linear-gradient(90deg, #7C3AED, #EC4899);
            border-radius: 10px;
        }

        /* ── Status Badges ─────────────────────────────── */
        .status-online {
            display: inline-flex; align-items: center; gap: 0.4rem;
            color: #10B981; font-size: 0.82rem; font-weight: 600;
        }
        .status-offline {
            display: inline-flex; align-items: center; gap: 0.4rem;
            color: #EF4444; font-size: 0.82rem; font-weight: 600;
        }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            display: inline-block; animation: blink 2s ease-in-out infinite;
        }
        .status-dot.online { background: #10B981; }
        .status-dot.offline { background: #EF4444; }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* ── Source Citation ────────────────────────────── */
        .source-citation {
            background: rgba(124,58,237,0.08);
            border: 1px solid rgba(124,58,237,0.15);
            border-radius: 10px; padding: 0.75rem 1rem;
            margin: 0.4rem 0; font-size: 0.85rem; color: #94A3B8;
        }

        /* ── Scrollbar ─────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.3); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.5); }

        /* ── Document Card ─────────────────────────────── */
        .doc-card {
            background: linear-gradient(135deg, rgba(30,30,50,0.7), rgba(20,20,35,0.9));
            border: 1px solid rgba(124,58,237,0.12);
            border-radius: 14px; padding: 1.2rem;
            transition: all 0.3s ease; margin-bottom: 0.75rem;
        }
        .doc-card:hover {
            border-color: rgba(124,58,237,0.3);
            box-shadow: 0 4px 15px rgba(124,58,237,0.1);
        }
        .doc-name { font-weight: 600; color: #E2E8F0; font-size: 0.95rem; }
        .doc-meta { font-size: 0.8rem; color: #64748B; margin-top: 0.3rem; }

        /* ── Empty State ───────────────────────────────── */
        .empty-state {
            text-align: center; padding: 3rem 1rem; color: #64748B;
        }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
        .empty-state-text { font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-header">
        <div class="app-title">📚 Student Study Buddy</div>
        <div class="app-subtitle">Your AI-Powered Learning Assistant</div>
    </div>
    """, unsafe_allow_html=True)

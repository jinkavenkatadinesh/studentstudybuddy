"""Test configuration and fixtures for Student Study Buddy."""

import sys
from pathlib import Path

import pytest

# Add project root directory to python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_session_state(monkeypatch):
    """Fixture to mock Streamlit session state."""
    import streamlit as st

    state = {}

    class SessionState:
        def __getattr__(self, name):
            return state.get(name)

        def __setattr__(self, name, value):
            state[name] = value

        def __contains__(self, item):
            return item in state

        def get(self, name, default=None):
            return state.get(name, default)

    monkeypatch.setattr(st, "session_state", SessionState())
    return state

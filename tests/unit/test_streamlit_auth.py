"""Unit tests for Streamlit AuthComponent UI flow state logic."""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add streamlit_app to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../streamlit_app"))

from components.auth import AuthComponent


class DummySessionState(dict):
    """Dummy dict supporting attribute access like Streamlit session_state."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


@pytest.fixture
def mock_streamlit():
    """Mock streamlit module and session state."""
    session_state = DummySessionState({
        'messages': [],
        'user_context': {},
        'authenticated': False,
        'guest_mode': False,
        'auth_page': 'landing'
    })

    with patch('components.auth.st') as mock_st:
        mock_st.session_state = session_state
        mock_st.rerun = MagicMock()
        mock_st.columns = lambda spec: [MagicMock() for _ in range(len(spec) if isinstance(spec, list) else spec)]
        mock_st.container = MagicMock()
        mock_st.form = MagicMock()
        yield mock_st, session_state


@pytest.mark.unit
def test_auth_component_init():
    auth = AuthComponent(api_base_url="http://testserver:8000")
    assert auth.api_base_url == "http://testserver:8000"


@pytest.mark.unit
def test_render_auth_flow_landing(mock_streamlit):
    mock_st, session_state = mock_streamlit
    auth = AuthComponent()

    session_state.auth_page = "landing"
    with patch.object(auth, 'render_landing_page') as mock_landing:
        auth.render_auth_flow()
        mock_landing.assert_called_once()


@pytest.mark.unit
def test_render_auth_flow_login(mock_streamlit):
    mock_st, session_state = mock_streamlit
    auth = AuthComponent()

    session_state.auth_page = "login"
    with patch.object(auth, 'render_login_page') as mock_login:
        auth.render_auth_flow()
        mock_login.assert_called_once()


@pytest.mark.unit
def test_render_auth_flow_register(mock_streamlit):
    mock_st, session_state = mock_streamlit
    auth = AuthComponent()

    session_state.auth_page = "register"
    with patch.object(auth, 'render_register_page') as mock_reg:
        auth.render_auth_flow()
        mock_reg.assert_called_once()


@pytest.mark.unit
def test_logout(mock_streamlit):
    mock_st, session_state = mock_streamlit
    auth = AuthComponent()

    session_state.authenticated = True
    session_state.guest_mode = True
    session_state.access_token = "token123"

    auth.logout()

    assert session_state.authenticated is False
    assert session_state.guest_mode is False
    assert "access_token" not in session_state
    assert session_state.auth_page == "landing"
    mock_st.rerun.assert_called_once()

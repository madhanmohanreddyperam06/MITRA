import streamlit as st
import importlib
import components.auth
import components.theme
importlib.reload(components.auth)
importlib.reload(components.theme)
from components.chat_interface import ChatInterface
from components.sidebar import create_sidebar
from components.auth import AuthComponent
from components.theme import apply_global_theme

# Page config - MITRA Helpdesk Assistant
st.set_page_config(
    page_title="MITRA - Your Intelligent Institution Helpdesk Assisstant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_context' not in st.session_state:
    st.session_state.user_context = {}
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'guest_mode' not in st.session_state:
    st.session_state.guest_mode = False
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'landing'  # 'landing', 'login', 'register'


def main():
    # Apply landing page color scheme globally across the application
    apply_global_theme()

    # Initialize auth component
    auth = AuthComponent()

    # Check authentication state
    if not st.session_state.authenticated:
        auth.render_auth_flow()
        return

    # User is authenticated or continuing as guest - show main application dashboard
    st.title("MITRA")

    if st.session_state.get("guest_mode"):
        st.info("💡 You are exploring in **Guest Mode**. Ask any question about admissions, courses, facilities, fees, or placements! To save account state, use the sidebar to log in or register.")
    else:
        user = st.session_state.get("current_user")
        if user and user.get("full_name"):
            st.success(f"👋 Welcome back, **{user.get('full_name')}**!")
        elif user and user.get("username"):
            st.success(f"👋 Welcome back, **{user.get('username')}**!")
        else:
            st.markdown("Welcome to your intelligent college assistant!")

    # Create sidebar controls & navigation
    create_sidebar()

    # Main chat interface
    chat_interface = ChatInterface()
    chat_interface.display_chat()


if __name__ == "__main__":
    main()



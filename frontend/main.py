import streamlit as st
from components.chat_interface import ChatInterface
from components.sidebar import create_sidebar
from components.auth import AuthComponent
from components.theme import apply_global_theme

# Page config
st.set_page_config(
    page_title="MITRA Helpdesk",
    page_icon="🎓",
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
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'chat'  # 'chat', 'admissions', 'courses', 'facilities'


def render_page_content():
    """Render content based on current page selection"""
    current_page = st.session_state.get('current_page', 'chat')
    
    if current_page == 'chat':
        # Main chat interface
        chat_interface = ChatInterface()
        chat_interface.display_chat()
    
    elif current_page == 'admissions':
        st.title("📋 Admissions Information")
        st.markdown("---")
        
        # Add admissions-specific content
        st.info("💡 Ask me anything about admissions, eligibility, application process, deadlines, etc.")
        
        # Chat interface for admissions
        chat_interface = ChatInterface()
        chat_interface.display_chat()
    
    elif current_page == 'courses':
        st.title("📚 Course Information")
        st.markdown("---")
        
        # Add courses-specific content
        st.info("💡 Ask me about available courses, syllabus, duration, eligibility, etc.")
        
        # Chat interface for courses
        chat_interface = ChatInterface()
        chat_interface.display_chat()
    
    elif current_page == 'facilities':
        st.title("🏗️ Campus Facilities")
        st.markdown("---")
        
        # Add facilities-specific content
        st.info("💡 Ask me about library, hostel, sports, labs, and other campus facilities.")
        
        # Chat interface for facilities
        chat_interface = ChatInterface()
        chat_interface.display_chat()


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
    if st.session_state.get("guest_mode"):
        st.info("💡 You are exploring in **Guest Mode**. Ask any question about admissions, courses, or facilities! To save account state, use the sidebar to log in or register.")
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

    # Render page content based on selection
    render_page_content()


if __name__ == "__main__":
    main()



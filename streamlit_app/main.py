import streamlit as st
from components.chat_interface import ChatInterface
from components.sidebar import create_sidebar
import json

# Page config
st.set_page_config(
    page_title="MITRA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_context' not in st.session_state:
    st.session_state.user_context = {}

def main():
    st.title("🎓 MITRA")
    st.markdown("Welcome to your intelligent college assistant!")

    # Create sidebar
    create_sidebar()

    # Main chat interface
    chat_interface = ChatInterface()
    chat_interface.display_chat()

if __name__ == "__main__":
    main()

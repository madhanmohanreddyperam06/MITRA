import streamlit as st
import sys
import os

# Ensure components directory is in sys.path when run directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.theme import apply_global_theme

def show():
    apply_global_theme()

    if not st.session_state.get("authenticated", False):
        st.warning("🔒 Please log in or continue as guest from the main landing page to access this section.")
        if st.button("⬅️ Go to Landing Page", use_container_width=True, type="primary"):
            st.switch_page("main.py")
        st.stop()

    st.title("📋 Admissions Information")

    st.markdown("""
    ## Admission Process

    ### Undergraduate Programs
    - **Eligibility**: 12th standard with minimum 60% marks
    - **Entrance Test**: College entrance exam or national level exams
    - **Application Period**: March - June

    ### Postgraduate Programs  
    - **Eligibility**: Bachelor's degree with minimum 55% marks
    - **Entrance Test**: Graduate aptitude test
    - **Application Period**: April - July

    ### Documents Required
    - Academic transcripts
    - Entrance test scores
    - Identity proof
    - Passport size photographs
    - Category certificate (if applicable)

    ### Important Dates
    - Application Start: March 1st
    - Last Date to Apply: June 30th
    - Entrance Test: July 15th
    - Result Declaration: July 30th
    - Counseling: August 1st - 15th
    """)

    if st.button("💬 Ask about Admissions", use_container_width=True, type="primary"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "I need detailed information about the admission process"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()



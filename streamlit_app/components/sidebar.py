import streamlit as st

def create_sidebar():
    """Create and manage the sidebar"""

    with st.sidebar:
        st.header("🎓 College Bot Settings")

        # Quick Actions
        st.subheader("Quick Actions")

        if st.button("🏫 Admissions Info"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Tell me about college admissions"
            })
            st.rerun()

        if st.button("📚 Course Information"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "What courses does the college offer?"
            })
            st.rerun()

        if st.button("💰 Fee Structure"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "What is the fee structure?"
            })
            st.rerun()

        if st.button("🏠 Hostel Facilities"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Tell me about hostel facilities"
            })
            st.rerun()

        # User Context
        st.subheader("Your Information")

        student_type = st.selectbox(
            "I am a:",
            ["Prospective Student", "Current Student", "Parent/Guardian", "Alumni"]
        )

        if student_type:
            st.session_state.user_context["student_type"] = student_type

        # Chat Controls
        st.subheader("Chat Controls")

        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.session_state.user_context = {}
            st.rerun()

        if st.button("📥 Download Chat"):
            download_chat()

        # Help Section
        st.subheader("Need Help?")
        st.markdown(""""
        **Sample Questions:**
        - What are the admission requirements?
        - How do I apply for scholarships?
        - What facilities are available in the library?
        - How can I contact the placement cell?
        - What are the hostel rules?
        """)

def download_chat():
    """Prepare chat history for download"""
    if st.session_state.messages:
        chat_text = ""
        for message in st.session_state.messages:
            role = message["role"].title()
            content = message["content"]
            chat_text += f"{role}: {content}\n\n"

        st.download_button(
            label="📄 Download as TXT",
            data=chat_text,
            file_name="college_bot_chat.txt",
            mime="text/plain"
        )
    else:
        st.info("No chat history to download.")

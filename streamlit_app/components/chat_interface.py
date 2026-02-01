import streamlit as st
import requests
import json
from datetime import datetime

class ChatInterface:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"

    def display_chat(self):
        """Display the chat interface"""

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything about college..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.get_bot_response(prompt)
                    st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    def get_bot_response(self, user_input):
        """Get response from backend API"""
        try:
            payload = {
                "user_input": user_input,
                "user_context": st.session_state.user_context,
                "conversation_history": st.session_state.messages[-5:]  # Last 5 messages for context
            }

            response = requests.post(
                f"{self.api_base_url}/chat",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "I'm sorry, I couldn't generate a response.")
            else:
                return "I'm having trouble connecting to the backend. Please try again."

        except requests.exceptions.ConnectionError:
            # Fallback response when backend is not available
            return self.get_fallback_response(user_input)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_fallback_response(self, user_input):
        """Provide fallback responses when backend is not available"""
        user_input_lower = user_input.lower()

        if any(word in user_input_lower for word in ['admission', 'apply', 'application']):
            return "For admission information, please visit our admissions office or check the college website. Our admission team is available Monday-Friday, 9 AM to 5 PM."

        elif any(word in user_input_lower for word in ['course', 'syllabus', 'curriculum']):
            return "Course information and syllabi are available through the academic department. You can also check the student portal for detailed curriculum information."

        elif any(word in user_input_lower for word in ['fee', 'payment', 'tuition']):
            return "For fee-related queries, please contact the accounts department. Fee payment can be made through the online portal or at the college accounts office."

        elif any(word in user_input_lower for word in ['library', 'book', 'resource']):
            return "The library is open Monday-Saturday, 8 AM to 8 PM. You can access digital resources through the library portal with your student ID."

        elif any(word in user_input_lower for word in ['hostel', 'accommodation', 'room']):
            return "For hostel accommodation, please contact the hostel administration office. Room allocation is done based on availability and application date."

        else:
            return "I'm here to help with your college-related queries! You can ask me about admissions, courses, fees, library services, hostel facilities, and more."

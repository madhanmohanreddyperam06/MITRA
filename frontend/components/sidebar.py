import streamlit as st
from components.auth import AuthComponent

def create_sidebar():
    """Create and manage the sidebar with improved UI"""

    with st.sidebar:
        # App Header
        st.markdown(
            """
            <div style='text-align: center; padding: 20px 0;'>
                <h1 style='font-size: 28px; margin: 0;'>🎓 MITRA</h1>
                <p style='color: #888; margin: 5px 0 0 0;'>College Helpdesk</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")

        # Navigation
        st.subheader("📍 Navigation")
        
        page = st.radio(
            "Go to:",
            ["💬 Chat", "📋 Admissions", "📚 Courses", "🏗️ Facilities"],
            label_visibility="collapsed"
        )
        
        if page == "💬 Chat":
            st.session_state.current_page = "chat"
        elif page == "📋 Admissions":
            st.session_state.current_page = "admissions"
        elif page == "📚 Courses":
            st.session_state.current_page = "courses"
        elif page == "🏗️ Facilities":
            st.session_state.current_page = "facilities"

        st.markdown("---")

        # Quick Actions (Interactive)
        st.subheader("⚡ Quick Actions")
        
        with st.expander("📖 Quick Prompts", expanded=False):
            if st.button("🏫 Admission Process", use_container_width=True, key="prompt_admissions"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Tell me about the admission process"
                })
                st.rerun()
            
            if st.button("📚 Course Details", use_container_width=True, key="prompt_courses"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What courses are available?"
                })
                st.rerun()
            
            if st.button("💰 Fee Information", use_container_width=True, key="prompt_fees"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What is the fee structure?"
                })
                st.rerun()
            
            if st.button("🏠 Hostel Info", use_container_width=True, key="prompt_hostel"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Tell me about hostel facilities"
                })
                st.rerun()
            
            if st.button("📞 Contact Info", use_container_width=True, key="prompt_contact"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "How can I contact the college?"
                })
                st.rerun()

        st.markdown("---")

        # User Context (Interactive)
        st.subheader("👤 Your Profile")
        
        student_type = st.selectbox(
            "I am a:",
            ["Prospective Student", "Current Student", "Parent/Guardian", "Alumni"],
            key="student_type_select"
        )

        if student_type:
            st.session_state.user_context["student_type"] = student_type

        # Additional context options
        with st.expander("📝 Additional Info", expanded=False):
            interested_course = st.text_input(
                "Interested Course:",
                placeholder="e.g., Computer Science",
                key="interested_course"
            )
            if interested_course:
                st.session_state.user_context["interested_course"] = interested_course
            
            year_of_study = st.selectbox(
                "Year of Study:",
                ["Not Applicable", "1st Year", "2nd Year", "3rd Year", "4th Year"],
                key="year_of_study"
            )
            if year_of_study != "Not Applicable":
                st.session_state.user_context["year_of_study"] = year_of_study

        st.markdown("---")

        # Chat Controls
        st.subheader("💬 Chat Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Clear", use_container_width=True, key="clear_chat"):
                st.session_state.messages = []
                st.session_state.user_context = {}
                st.rerun()
        
        with col2:
            if st.button("📥 Export", use_container_width=True, key="export_chat"):
                download_chat()

        # Chat history count
        if st.session_state.messages:
            st.caption(f"💬 {len(st.session_state.messages)} messages in chat")

        st.markdown("---")

        # Help Section
        st.subheader("❓ Help & Tips")
        
        with st.expander("💡 Sample Questions", expanded=False):
            st.markdown("""
            **Admissions:**
            - What are the admission requirements?
            - How do I apply for scholarships?
            - What documents are needed?
            
            **Courses:**
            - What courses does the college offer?
            - What is the duration of B.Tech?
            - Are there any new programs?
            
            **Facilities:**
            - What are the library hours?
            - How can I access the gym?
            - What sports facilities are available?
            
            **Contact:**
            - How can I reach the placement cell?
            - What is the principal's office number?
            - Where is the admission office located?
            """)

        st.markdown("---")

        # Account Status (At the bottom)
        st.subheader("🔐 Account Status")
        
        auth = AuthComponent()
        
        if st.session_state.get("authenticated"):
            if st.session_state.get("guest_mode"):
                st.info("👤 **Guest Mode**")
                st.caption("Limited access. Login for full features.")
                
                if st.button("🔑 Login", use_container_width=True, key="guest_login"):
                    st.session_state.authenticated = False
                    st.session_state.guest_mode = False
                    st.session_state.auth_page = "login"
                    st.rerun()
            else:
                # Show user info
                user = st.session_state.get("current_user")
                if user:
                    st.success(f"👋 {user.get('full_name', user.get('username', 'User'))}")
                    st.caption(f"📧 {user.get('email', '')}")
                    
                    if user.get('is_admin'):
                        st.markdown("⭐ **Administrator**")
                    
                    st.caption(f"🕐 Last login: {user.get('last_login_at', 'Never')[:10] if user.get('last_login_at') else 'Never'}")
                
                # Logout button
                if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                    auth.logout()
        else:
            st.warning("🔒 Not Logged In")
            st.caption("Login to save your chat history")
            
            if st.button("🔑 Login", use_container_width=True, key="sidebar_login"):
                st.session_state.auth_page = "login"
                st.rerun()
            
            if st.button("📝 Register", use_container_width=True, key="sidebar_register"):
                st.session_state.auth_page = "register"
                st.rerun()
            
            if st.button("👤 Continue as Guest", use_container_width=True, key="sidebar_guest"):
                st.session_state.authenticated = True
                st.session_state.guest_mode = True
                st.rerun()

        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; padding: 10px; font-size: 12px; color: #666;'>
                <p>MITRA v1.0</p>
                <p>© 2026 College Helpdesk</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def download_chat():
    """Prepare chat history for download"""
    if st.session_state.messages:
        chat_text = "MITRA College Helpdesk - Chat History\n"
        chat_text += "=" * 50 + "\n\n"
        
        for idx, message in enumerate(st.session_state.messages, 1):
            role = message["role"].upper()
            content = message["content"]
            chat_text += f"[{idx}] {role}:\n{content}\n\n"

        st.download_button(
            label="📄 Download Chat History",
            data=chat_text,
            file_name=f"mitra_chat_{st.session_state.get('current_user', {}).get('username', 'guest')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("No chat history to download.")

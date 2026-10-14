import streamlit as st
from components.auth import AuthComponent

def create_sidebar():
    """Create and manage the interactive sidebar with role-based features"""

    with st.sidebar:
        # Custom CSS for sidebar styling
        st.markdown("""
        <style>
            .sidebar-section {
                margin-bottom: 15px;
            }
            .sidebar-header {
                font-size: 0.85rem;
                font-weight: 600;
                color: #94a3b8;
                margin-bottom: 8px;
                padding-bottom: 5px;
                border-bottom: 1px solid #382f4f;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .quick-access-btn {
                width: 100%;
                margin: 4px 0;
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #362e4c;
                background: #221e31;
                color: #e2e8f0;
                font-size: 0.85rem;
                text-align: left;
            }
            .quick-access-btn:hover {
                background: #312a47;
                border-color: #6366f1;
            }
            .new-chat-btn {
                width: 100%;
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #6d28d9;
                background: #4c1d95;
                color: #ffffff;
                font-weight: 600;
                font-size: 0.95rem;
                margin-bottom: 15px;
            }
            .new-chat-btn:hover {
                background: #5b21b6;
                border-color: #7c3aed;
            }
            .account-section {
                margin-top: 20px;
                padding-top: 15px;
                border-top: 2px solid #6d28d9;
            }
        </style>
        """, unsafe_allow_html=True)

        # ============================================
        # 1. New Chat (Prominent Action)
        # ============================================
        if st.button("➕ New Chat", use_container_width=True, key="new_chat"):
            st.session_state.messages = []
            st.session_state.user_context = {}
            st.rerun()

        # ============================================
        # 3. Quick Access (College Topics)
        # ============================================
        st.markdown('<div class="sidebar-header">Quick Access</div>', unsafe_allow_html=True)
        
        quick_access_items = [
            ("Admissions", "Tell me about college admission requirements"),
            ("Courses & Programs", "What courses does the college offer?"),
            ("Fees & Scholarships", "What is the fee structure and available scholarships?"),
            ("Hostel & Facilities", "Tell me about hostel facilities"),
            ("Placements", "What are the placement statistics and companies?"),
            ("Contact Information", "How can I contact different departments?"),
        ]
        
        for label, question in quick_access_items:
            if st.button(label, use_container_width=True, key=f"qa_{label}"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                st.rerun()

        st.markdown("---")

        # ============================================
        # 4. Conversation History (Placeholder for Phase 2)
        # ============================================
        st.markdown('<div class="sidebar-header">Conversations</div>', unsafe_allow_html=True)
        
        # For now, show current session info
        if st.session_state.messages:
            msg_count = len(st.session_state.messages)
            st.caption(f"Current session: {msg_count} message(s)")
        else:
            st.caption("No active conversation")
        
        # Future: Add conversation history with dates
        # Today
        #   • Admission requirements
        #   • CSE course details
        # Yesterday
        #   • Hostel information

        st.markdown("---")

        # ============================================
        # 7. Student Type / User Context
        # ============================================
        st.markdown('<div class="sidebar-header">Your Profile</div>', unsafe_allow_html=True)
        
        st.caption("I am a:")
        student_type = st.radio(
            "Select student type",
            ["Prospective Student", "Current Student", "Parent/Guardian", "Alumni"],
            label_visibility="collapsed",
            key="student_type_radio"
        )

        if student_type:
            st.session_state.user_context["student_type"] = student_type

        st.markdown("---")

        # ============================================
        # 9. Settings (Simple)
        # ============================================
        st.markdown('<div class="sidebar-header">Settings</div>', unsafe_allow_html=True)
        
        with st.expander("Appearance", expanded=False):
            theme = st.radio(
                "Select theme",
                ["Dark", "Light"],
                label_visibility="collapsed",
                key="theme_radio"
            )
        
        with st.expander("Chat Options", expanded=False):
            show_timestamps = st.checkbox("Show timestamps", value=True, key="show_timestamps")
            auto_scroll = st.checkbox("Auto-scroll", value=True, key="auto_scroll")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear", use_container_width=True, key="settings_clear"):
                    st.session_state.messages = []
                    st.session_state.user_context = {}
                    st.rerun()
            with col2:
                if st.button("Download", use_container_width=True, key="settings_download"):
                    download_chat()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear", use_container_width=True, key="settings_clear"):
                    st.session_state.messages = []
                    st.session_state.user_context = {}
                    st.rerun()
            with col2:
                if st.button("Download", use_container_width=True, key="settings_download"):
                    download_chat()

        st.markdown("---")

        # ============================================
        # 10. Help & About
        # ============================================
        st.markdown('<div class="sidebar-header">Help & About</div>', unsafe_allow_html=True)
        
        with st.expander("Help & About", expanded=False):
            st.markdown("""
            **What is MITRA?**
            
            MITRA v2.0 - AI-powered college helpdesk assistant designed to provide quick and reliable college information.
            
            **How to use MITRA:**
            - Type your question in the chat
            - Use Quick Access for common topics
            - Set your profile for personalized responses
            
            **Supported Topics:**
            - Admissions & Eligibility
            - Courses & Programs
            - Fees & Scholarships
            - Hostel & Facilities
            - Placements
            - Contact Information
            """)

        # Spacer to push account section to bottom
        st.markdown("<br><br>", unsafe_allow_html=True)

        # ============================================
        # 5. User Profile Section (at bottom, role-based)
        # ============================================
        st.markdown('<div class="account-section"></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="sidebar-header">Account</div>', unsafe_allow_html=True)
        
        # Get user info
        user = st.session_state.get("current_user")
        is_guest = st.session_state.get("guest_mode", False)
        is_admin = user and user.get("is_admin", False) if user else False
        
        if is_guest:
            # Guest User
            st.info("Guest User")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True, key="guest_login"):
                    st.session_state.auth_page = "login"
                    st.rerun()
            with col2:
                if st.button("Register", use_container_width=True, key="guest_register"):
                    st.session_state.auth_page = "register"
                    st.rerun()
        
        elif user:
            # Authenticated User
            username = user.get("username", "User")
            full_name = user.get("full_name", "")
            email = user.get("email", "")
            
            if is_admin:
                st.success(f"{username}")
                st.caption("Administrator")
            else:
                st.success(f"{username}")
                st.caption("Registered User")
            
            if full_name:
                st.caption(full_name)
            
            # Settings, Help, Logout buttons
            if st.button("Settings", use_container_width=True, key="user_settings"):
                pass  # Expand settings above
            
            if st.button("Help & About", use_container_width=True, key="user_help"):
                pass  # Expand help above
            
            # Admin-only options
            if is_admin:
                st.markdown("---")
                st.markdown('<div class="sidebar-header">Administration</div>', unsafe_allow_html=True)
                
                admin_options = [
                    ("User Management", "/admin/users"),
                    ("Knowledge Base", "/admin/knowledge"),
                    ("Q&A Management", "/admin/qa"),
                    ("Analytics", "/admin/analytics"),
                ]
                
                for label, path in admin_options:
                    if st.button(label, use_container_width=True, key=f"admin_{label}"):
                        st.info(f"Admin panel: {path} (Coming soon)")
            
            st.markdown("---")
            if st.button("Logout", use_container_width=True, key="user_logout"):
                auth = AuthComponent()
                auth.logout()

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
            file_name="mitra_chat.txt",
            mime="text/plain"
        )
    else:
        st.info("No chat history to download.")

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
            .new-chat-btn {
                width: 100%;
                padding: 8px;
                border-radius: 8px;
                border: 2px solid #6d28d9;
                background: #4c1d95;
                color: #ffffff;
                font-weight: 600;
                font-size: 0.95rem;
                margin-bottom: 10px;
            }
            .new-chat-btn:hover {
                background: #5b21b6;
                border-color: #7c3aed;
            }
            .account-section {
                margin-top: 0px;
                padding-top: 0px;
            }
            /* Reduce spacing around New Chat button */
            .stButton > button {
                margin-top: 0px !important;
                margin-bottom: 0px !important;
                padding: 8px !important;
            }
            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
                gap: 0.5rem !important;
            }
            section[data-testid="stSidebar"] > div {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
            }
            /* Remove space above and below button container */
            div[data-testid="stVerticalBlock"] > div:has(.stButton) {
                margin-top: 0px !important;
                margin-bottom: 0px !important;
            }
            /* Fix expander arrow icons - use font that supports arrows */
            div[data-testid="stExpander"] > div > div > button {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }
            div[data-testid="stExpander"] svg {
                fill: #e2e8f0 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # ============================================
        # 1. New Chat (Prominent Action)
        # ============================================
        if st.button("➕ New Chat", width='stretch', key="new_chat"):
            st.session_state.messages = []
            st.session_state.user_context = {}
            st.rerun()

        if st.button("Clear Chat", width='stretch', key="clear_chat"):
            st.session_state.messages = []
            st.session_state.user_context = {}
            st.rerun()

        st.markdown("---")

        # ============================================
        # 8. Settings (Simple)
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
                if st.button("Clear", width='stretch', key="settings_clear"):
                    st.session_state.messages = []
                    st.session_state.user_context = {}
                    st.rerun()
            with col2:
                if st.button("Download", width='stretch', key="settings_download"):
                    download_chat()

        st.markdown("---")

        # ============================================
        # 9. Help & About
        # ============================================
        st.markdown('<div class="sidebar-header">Help & About</div>', unsafe_allow_html=True)
        
        with st.expander("Help & About", expanded=False):
            st.markdown("""
            **What is MITRA?**
            
            MITRA v2.0 - AI-powered college helpdesk assistant designed to provide quick and reliable college information.
            
            **How to use MITRA:**
            - Type your question in the chat
            - Explore topics using the sidebar navigation pages
            
            **Supported Topics:**
            - Admissions & Eligibility
            - Courses & Programs
            - Fees & Scholarships
            - Hostel & Facilities
            - Placements
            - Contact Information
            """)

        # Spacer to push account section to bottom
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
                if st.button("Login", width='stretch', key="guest_login"):
                    st.session_state.auth_page = "login"
                    st.rerun()
            with col2:
                if st.button("Register", width='stretch', key="guest_register"):
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
            if st.button("Settings", width='stretch', key="user_settings"):
                pass  # Expand settings above
            
            if st.button("Help & About", width='stretch', key="user_help"):
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
                    if st.button(label, width='stretch', key=f"admin_{label}"):
                        st.info(f"Admin panel: {path} (Coming soon)")
            
            st.markdown("---")
            if st.button("Logout", width='stretch', key="user_logout"):
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

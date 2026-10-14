"""Authentication component for Streamlit frontend."""
import streamlit as st
import requests
import os


class AuthComponent:
    """Handle authentication in Streamlit app."""

    def __init__(self, api_base_url=None):
        # Use environment variable if available, otherwise default to localhost
        if api_base_url is None:
            api_base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_base_url = api_base_url

    def render_auth_flow(self):
        """Render the appropriate authentication page based on session state."""
        # Custom CSS for minimal dark theme matching the reference design exactly
        st.markdown(
            """
            <style>
                /* Hide sidebar on auth/landing pages */
                [data-testid="stSidebar"] { display: none; }

                /* Pitch Dark Canvas Background */
                .stApp {
                    background: #0c0b12 !important;
                    color: #e2e8f0;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }

                /* Title Bar matching reference image style */
                .mitra-title-bar {
                    background-color: #231f32;
                    border: 1px solid #382f4f;
                    border-top: 3px solid #6d28d9;
                    border-radius: 4px;
                    padding: 4px 24px;
                    text-align: center;
                    margin-bottom: 10px;
                    margin-top: 20px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                }

                .mitra-title-text {
                    color: #ffffff !important;
                    font-size: 1.25rem !important;
                    font-weight: bold !important;
                    font-family: Georgia, "Times New Roman", Times, serif;
                    margin: 0 !important;
                    letter-spacing: -0.3px;
                }

                /* Subtitle prompt matching reference prompt style */
                .mitra-prompt {
                    color: #cbd5e1;
                    font-size: 0.88rem;
                    margin-top: 280px;
                    margin-bottom: 14px;
                    font-weight: 500;
                    text-align: center;
                }

                /* Tagline styling between header title and buttons */
                .mitra-tagline {
                    color: #a5b4fc;
                    font-size: 1.05rem;
                    font-weight: 500;
                    text-align: center;
                    margin-top: 18px;
                    margin-bottom: 24px;
                    line-height: 1.5;
                    letter-spacing: 0.2px;
                }

                /* Compact Button Styling (Not long or big) */
                div.stButton > button {
                    background-color: #221e31 !important;
                    color: #e2e8f0 !important;
                    border: 1px solid #362e4c !important;
                    border-radius: 6px !important;
                    font-size: 0.88rem !important;
                    font-weight: 500 !important;
                    padding: 8px 14px !important;
                    height: auto !important;
                    min-height: 38px !important;
                    transition: all 0.2s ease !important;
                    width: 100% !important;
                }

                div.stButton > button:hover {
                    background-color: #312a47 !important;
                    color: #ffffff !important;
                    border-color: #6366f1 !important;
                    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
                }

                div.stButton > button[kind="primary"] {
                    background-color: #4c1d95 !important;
                    border: 1px solid #6d28d9 !important;
                    color: #ffffff !important;
                }

                div.stButton > button[kind="primary"]:hover {
                    background-color: #5b21b6 !important;
                    border-color: #7c3aed !important;
                }

                /* Mobile view - side-by-side buttons with reduced size */
                @media (max-width: 768px) {
                    /* Prevent Streamlit columns from stacking vertically on mobile */
                    [data-testid="stHorizontalBlock"],
                    div[class*="stHorizontalBlock"] {
                        display: flex !important;
                        flex-direction: row !important;
                        flex-wrap: nowrap !important;
                        width: 100% !important;
                        gap: 6px !important;
                        align-items: center !important;
                    }

                    /* Hide empty outer spacer columns on mobile to maximize button row width */
                    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)),
                    [data-testid="stHorizontalBlock"] > [data-testid="column"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)),
                    div[class*="stHorizontalBlock"] > div[class*="stColumn"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)) {
                        display: none !important;
                        width: 0 !important;
                        flex: 0 0 0px !important;
                        margin: 0 !important;
                        padding: 0 !important;
                    }

                    /* Active columns take equal space side-by-side */
                    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
                    [data-testid="stHorizontalBlock"] > [data-testid="column"],
                    div[class*="stHorizontalBlock"] > div[class*="stColumn"],
                    [data-testid="stColumn"],
                    [data-testid="column"] {
                        width: auto !important;
                        min-width: 0 !important;
                        flex: 1 1 0% !important;
                    }

                    /* Reduce button font size, padding, and height so login, register, guest buttons fit side-by-side */
                    div.stButton > button {
                        padding: 6px 4px !important;
                        font-size: 0.78rem !important;
                        font-weight: 500 !important;
                        min-height: 36px !important;
                        height: auto !important;
                        white-space: nowrap !important;
                        overflow: hidden !important;
                        text-overflow: ellipsis !important;
                        width: 100% !important;
                    }
                }

                /* Footer link matching reference image */
                .mitra-footer-link {
                    color: #94a3b8;
                    font-size: 0.82rem;
                    margin-top: 24px;
                    text-align: left;
                }

                .mitra-footer-link a {
                    color: #818cf8;
                    text-decoration: underline;
                }

                .mitra-footer-link a:hover {
                    color: #a5b4fc;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        current_page = st.session_state.get("auth_page", "landing")

        if current_page == "login":
            self.render_login_page()
        elif current_page == "register":
            self.render_register_page()
        else:
            self.render_landing_page()

    def render_landing_page(self):
        """Display a minimal, compact dark-themed Landing Page matching the reference image."""

        # Centered container matching reference proportions
        col_outer1, col_center, col_outer2 = st.columns([1, 4, 1])

        with col_center:
            # Title Bar Banner (Exact reference image style)
            st.markdown(
                """
                <div class="mitra-title-bar">
                    <h1 class="mitra-title-text">Welcome to MITRA Helpdesk!</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Tagline in between header title and button section
            st.markdown(
                """
                <div class="mitra-tagline">
                    Your Intelligent Assistant for Institution information, guidance and support.
                </div>
                """,
                unsafe_allow_html=True
            )

            # Subtitle Prompt
            st.markdown(
                "<p class='mitra-prompt' style='margin-top: 120px;'>Select an option below to start your session:</p>",
                unsafe_allow_html=True
            )

            # Action Buttons (Compact row)
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("Login", type="primary", use_container_width=True, key="landing_login"):
                    st.session_state.auth_page = "login"
                    st.rerun()

            with col2:
                if st.button("Register", use_container_width=True, key="landing_register"):
                    st.session_state.auth_page = "register"
                    st.rerun()

            with col3:
                if st.button("Guest Access", use_container_width=True, key="landing_guest"):
                    st.session_state.authenticated = True
                    st.session_state.guest_mode = True
                    st.rerun()

            # Footer link matching reference image ("Create your own adventure visit GitHub")
            st.markdown(
                """
                <div class="mitra-footer-link">
                    To learn more about MITRA assistant visit <a href="https://github.com" target="_blank">GitHub</a>
                </div>
                """,
                unsafe_allow_html=True
            )





    def render_login_page(self):
        """Display dedicated Login page."""
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            # Title Bar with upperline
            st.markdown(
                """
                <div class="mitra-title-bar">
                    <h1 class="mitra-title-text">Login to your Account</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("Sign in to access your personalized assistant")
            st.write("")

            with st.container():
                with st.form("login_form"):
                    username_or_email = st.text_input("Username or Email", placeholder="Enter your username or email")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")

                    submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True, key="login_submit")

                    if submitted:
                        if not username_or_email or not password:
                            st.error("Please fill in all fields.")
                        else:
                            token = self.login(username_or_email, password)
                            if token:
                                st.session_state.access_token = token
                                st.session_state.authenticated = True
                                st.session_state.guest_mode = False
                                st.session_state.auth_page = "landing"
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("Invalid credentials. Please check your username/email and password.")

            st.write("")
            # Navigation links
            nav1, nav2, nav3 = st.columns([1, 1, 1])
            with nav1:
                if st.button("Back to Landing", use_container_width=True, key="login_back"):
                    st.session_state.auth_page = "landing"
                    st.rerun()
            with nav2:
                if st.button("Need an account? Register", use_container_width=True, key="login_to_register"):
                    st.session_state.auth_page = "register"
                    st.rerun()
            with nav3:
                if st.button("Continue as Guest", use_container_width=True, key="login_guest"):
                    st.session_state.authenticated = True
                    st.session_state.guest_mode = True
                    st.rerun()

    def render_register_page(self):
        """Display dedicated Registration page."""
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            # Title Bar with upperline
            st.markdown(
                """
                <div class="mitra-title-bar">
                    <h1 class="mitra-title-text">Create Account</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("Register for an account to unlock all features")
            st.write("")

            with st.container(border=True):
                with st.form("register_form"):
                    reg_username = st.text_input("Username", placeholder="e.g. john_doe")
                    reg_email = st.text_input("Email", placeholder="e.g. john@example.com")
                    reg_full_name = st.text_input("Full Name (Optional)", placeholder="e.g. John Doe")
                    reg_password = st.text_input("Password (minimum 8 characters)", type="password", placeholder="Password")
                    reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

                    reg_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True, key="register_submit")

                    if reg_submitted:
                        if not reg_username or not reg_email or not reg_password:
                            st.error("Please fill in all required fields (Username, Email, Password).")
                        elif reg_password != reg_confirm:
                            st.error("Passwords do not match. Please re-enter your password.")
                        elif len(reg_password) < 8:
                            st.error("Password must be at least 8 characters long.")
                        else:
                            success = self.register(reg_username, reg_email, reg_password, reg_full_name)
                            if success:
                                st.session_state.registration_success = True

            if st.session_state.get("registration_success"):
                st.success("Registration successful! You can now log in with your credentials.")
                if st.button("Proceed to Login", type="primary", use_container_width=True, key="register_to_login"):
                    st.session_state.registration_success = False
                    st.session_state.auth_page = "login"
                    st.session_state.is_admin = False
                    st.rerun()

            st.write("")
            # Navigation links
            nav1, nav2 = st.columns([1, 1])
            with nav1:
                if st.button("Back to Landing", use_container_width=True, key="register_back"):
                    st.session_state.auth_page = "landing"
                    st.session_state.registration_success = False
                    st.rerun()
            with nav2:
                if st.button("Already registered? Login", use_container_width=True, key="register_to_login2"):
                    st.session_state.auth_page = "login"
                    st.session_state.registration_success = False
                    st.rerun()

    def login_page(self):
        """Backwards compatible method wrapper for login page rendering."""
        self.render_auth_flow()

    def login(self, username_or_email: str, password: str) -> str:
        """Authenticate user and return JWT token."""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/auth/login",
                json={
                    "username_or_email": username_or_email,
                    "password": password
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
            else:
                return None

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend API. Please ensure the backend is running.")
            return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    def register(self, username: str, email: str, password: str, full_name: str = None) -> bool:
        """Register a new user account."""
        try:
            payload = {
                "username": username,
                "email": email,
                "password": password
            }
            if full_name:
                payload["full_name"] = full_name

            response = requests.post(
                f"{self.api_base_url}/api/auth/register",
                json=payload,
                timeout=10
            )

            if response.status_code == 201:
                return True
            else:
                detail = response.json().get("detail", "Registration failed.")
                st.error(f"Registration failed: {detail}")
                return False

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend API. Please ensure the backend is running.")
            return False
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return False

    def logout(self):
        """Clear authentication state."""
        if "access_token" in st.session_state:
            del st.session_state.access_token
        if "authenticated" in st.session_state:
            st.session_state.authenticated = False
        if "guest_mode" in st.session_state:
            st.session_state.guest_mode = False
        if "is_admin" in st.session_state:
            del st.session_state.is_admin
        if "redirect_to_admin" in st.session_state:
            del st.session_state.redirect_to_admin
        if "current_user" in st.session_state:
            del st.session_state.current_user
        if "registration_success" in st.session_state:
            del st.session_state.registration_success
        st.session_state.auth_page = "landing"
        st.success("Session ended.")
        st.rerun()

    def get_current_user(self) -> dict:
        """Get current user information from API."""
        if st.session_state.get("guest_mode") or "access_token" not in st.session_state:
            return None

        try:
            response = requests.get(
                f"{self.api_base_url}/api/auth/me",
                headers={
                    "Authorization": f"Bearer {st.session_state.access_token}"
                },
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                self.logout()
                return None

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend.")
            return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    def get_auth_headers(self) -> dict:
        """Get authorization headers for API requests."""
        if "access_token" in st.session_state and not st.session_state.get("guest_mode"):
            return {"Authorization": f"Bearer {st.session_state.access_token}"}
        return {}

    def display_logout_button(self):
        """Display user status and logout/exit button in sidebar."""
        if st.session_state.get("authenticated"):
            with st.sidebar:
                st.subheader("👤 Account Status")

                if st.session_state.get("guest_mode"):
                    st.info("Browsing as **Guest User**")
                    if st.button("🔑 Log In / Register", use_container_width=True):
                        self.logout()
                else:
                    if "current_user" not in st.session_state or st.session_state.current_user is None:
                        st.session_state.current_user = self.get_current_user()

                    if st.session_state.current_user:
                        user = st.session_state.current_user
                        st.markdown(f"**Username:** `{user.get('username', 'N/A')}`")
                        st.markdown(f"**Email:** `{user.get('email', 'N/A')}`")

                    if st.button("🚪 Logout", type="secondary", use_container_width=True):
                        self.logout()

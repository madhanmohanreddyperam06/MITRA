"""Global theme styling component for MITRA Streamlit application."""
import streamlit as st

def apply_global_theme():
    """Apply the landing page dark color scheme to the entire application."""
    st.markdown(
        """
        <style>
            /* Global Canvas Background */
            .stApp {
                background-color: #0c0b12 !important;
                color: #e2e8f0 !important;
                font-family: "Times New Roman", Times, serif !important;
            }

            /* Apply Times New Roman to text elements only */
            body, p, h1, h2, h3, h4, h5, h6, label, input, textarea, select {
                font-family: "Times New Roman", Times, serif !important;
            }

            /* Keep system font for UI elements with icons (buttons, expanders) */
            button, div[data-testid="stExpander"] > div > div > button {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }

            /* Sidebar Dark Theme Styling */
            [data-testid="stSidebar"] {
                background-color: #151221 !important;
                border-right: 1px solid #2b2542 !important;
            }

            [data-testid="stSidebar"] * {
                color: #e2e8f0 !important;
            }

            /* Containers & Bordered Cards */
            [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"],
            div[data-testid="stExpander"] {
                background-color: #171424 !important;
                border: 1px solid #362e4c !important;
                border-radius: 8px !important;
            }

            /* Global Button Styling matching Landing Page */
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

            /* Mobile View - side-by-side layout for buttons and columns */
            @media (max-width: 768px) {
                [data-testid="stHorizontalBlock"],
                div[class*="stHorizontalBlock"] {
                    display: flex !important;
                    flex-direction: row !important;
                    flex-wrap: nowrap !important;
                    width: 100% !important;
                    gap: 6px !important;
                    align-items: center !important;
                }

                [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)),
                [data-testid="stHorizontalBlock"] > [data-testid="column"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)),
                div[class*="stHorizontalBlock"] > div[class*="stColumn"]:not(:has(button)):not(:has(h1)):not(:has(p)):not(:has(form)):not(:has(input)):not(:has(span)) {
                    display: none !important;
                    width: 0 !important;
                    flex: 0 0 0px !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
                [data-testid="stHorizontalBlock"] > [data-testid="column"],
                div[class*="stHorizontalBlock"] > div[class*="stColumn"],
                [data-testid="stColumn"],
                [data-testid="column"] {
                    width: auto !important;
                    min-width: 0 !important;
                    flex: 1 1 0% !important;
                }

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

            /* Form Inputs, Selectboxes & Text Inputs */
            div[data-baseweb="input"],
            div[data-baseweb="select"] > div {
                background-color: #1a1628 !important;
                border: 1px solid #362e4c !important;
                color: #e2e8f0 !important;
                border-radius: 6px !important;
            }

            /* Chat Input Styling */
            div[data-testid="stChatInput"] input {
                background-color: #1a1628 !important;
                color: #e2e8f0 !important;
                border: 1px solid #3b3254 !important;
            }

            /* Chat Message Bubbles */
            [data-testid="stChatMessage"] {
                background-color: #171424 !important;
                border: 1px solid #2d2544 !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
                margin-bottom: 12px !important;
            }

            /* Headings & Text */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }

            p, span, label {
                color: #cbd5e1 !important;
            }

            /* Info, Success, Warning Banners */
            div[data-testid="stNotification"] {
                background-color: #1c182b !important;
                border: 1px solid #3d335a !important;
                color: #e2e8f0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

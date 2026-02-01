# Configuration settings for Smart College Helpdesk Bot

# API Configuration
API_HOST = "localhost"
API_PORT = 8000
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Streamlit Configuration
STREAMLIT_HOST = "localhost" 
STREAMLIT_PORT = 8501

# Database Configuration
DB_PATH = "data/knowledge_base/college_info.db"

# NLP Configuration
SPACY_MODEL = "en_core_web_sm"
MAX_RESPONSE_LENGTH = 1000
CONFIDENCE_THRESHOLD = 0.5

# Chat Configuration
MAX_CONVERSATION_HISTORY = 10
DEFAULT_RESPONSE_TIMEOUT = 30

# College Information
COLLEGE_NAME = "ABC College of Technology"
COLLEGE_ADDRESS = "123 Education Street, Knowledge City, State - 123456"
COLLEGE_PHONE = "+91-123-456-7890"
COLLEGE_EMAIL = "info@abccollege.edu"
COLLEGE_WEBSITE = "www.abccollege.edu"

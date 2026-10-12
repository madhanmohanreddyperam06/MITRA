# MITRA - AI Powered College Helpdesk Bot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

An intelligent chatbot system for college helpdesk services built with Streamlit frontend and FastAPI backend. MITRA provides instant responses to student queries about admissions, courses, facilities, and more using NLP techniques with spaCy.

## Features

- 🎓 **Admission Information**: Get details about admission process, eligibility, and requirements
- 📚 **Course Information**: Browse available courses and programs
- 💰 **Fee Structure**: Information about fees, scholarships, and payment options
- 🏠 **Hostel Facilities**: Details about accommodation and hostel services
- 📖 **Library Services**: Library facilities and resources information
- 🏢 **Placement Support**: Career guidance and placement statistics
- 📞 **Contact Information**: Department contacts and office locations
- 🔐 **User Authentication**: Secure JWT-based registration and login system
- 🗄️ **MySQL Database**: Robust relational storage using MySQL 8.x, SQLAlchemy 2.0, and Alembic migrations
- 👤 **Guest Mode**: Explore the system without registration

## Completed Tasks & Status

- ✅ **Architecture Modernization**: Modular layered architecture (API routes, Services, Repositories, Schemas, Core)
- ✅ **MySQL Database**: Complete migration to MySQL with SQLAlchemy 2.0 ORM
- ✅ **Authentication System**: JWT tokens, Bcrypt password hashing, user registration, and login
- ✅ **NLP Intent & Entity Engine**: spaCy pipeline with keyword fallback matching for college queries
- ✅ **Multi-page Frontend**: Streamlit app with landing page, chat interface, and information pages
- ✅ **Test Automation**: Pytest suite covering configuration, NLP logic, repository methods, and API integration

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **NLP**: spaCy (`en_core_web_sm`)
- **Database**: MySQL 8.x
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT + Bcrypt
- **Testing**: Pytest

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 8.x Server
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone <https://github.com/madhanmohanreddyperam06/MITRA.git>
cd MITRA
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 5. Initialize the database (MySQL)

1. Create a MySQL database:
   ```sql
   CREATE DATABASE mitra CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Configure environment variables in `backend/.env` (or copy from `.env.example`):
   ```bash
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/mitra
   ```

3. Run Alembic database migrations:
   ```bash
   cd backend
   alembic upgrade head
   cd ..
   ```

### 6. Run tests (Optional)

Verify installation using Pytest:

```bash
python -m pytest tests/ -v
```

## Usage

Start both the backend API server and the Streamlit frontend.

### 1. Running the Backend API

From the project root (with `venv` activated):

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

### 2. Running the Streamlit Frontend

Open a second terminal, navigate to the project root, activate `venv`, then run:

```bash
cd frontend
python -m streamlit run main.py
```

*(Note: Using `python -m streamlit run main.py` ensures the app uses python from your active virtual environment).*

The Streamlit interface will open automatically in your browser at `http://localhost:8501`.

**Note**: Both backend and frontend services must be running simultaneously.

## Project Structure

```
MITRA/
├── frontend/                   # Frontend application
│   ├── main.py                 # Main Streamlit app
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication component
│   │   ├── chat_interface.py   # Chat interface component
│   │   ├── sidebar.py          # Sidebar component
│   │   └── theme.py            # Theme configuration
│   └── pages/                  # Multi-page app pages
│       ├── 1_Admissions.py     # Admissions information page
│       ├── 2_Courses.py        # Courses information page
│       └── 3_Facilities.py     # Facilities information page
├── backend/                    # Backend API
│   ├── app/                    # Application code
│   │   ├── api/                # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── chat.py         # Chat endpoint
│   │   │   ├── health.py       # Health check endpoint
│   │   │   ├── intents.py      # Intents endpoint
│   │   │   └── knowledge.py    # Q&A management endpoints
│   │   ├── core/               # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Configuration management
│   │   │   ├── logging.py      # Logging configuration
│   │   │   ├── exceptions.py   # Custom exceptions
│   │   │   ├── error_handlers.py # Global error handlers
│   │   │   └── security.py     # Security utilities
│   │   ├── database/           # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── connection.py   # Database connection management
│   │   │   ├── models.py       # SQLAlchemy models
│   │   │   └── repositories/  # Repository pattern
│   │   │       ├── __init__.py
│   │   │       ├── admissions.py
│   │   │       ├── courses.py
│   │   │       ├── facilities.py
│   │   │       ├── contacts.py
│   │   │       ├── qa.py
│   │   │       └── users.py
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication schemas
│   │   │   ├── chat.py         # Chat schemas
│   │   │   └── knowledge.py    # Q&A schemas
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py  # Authentication service
│   │   │   ├── chat_service.py  # Chat service
│   │   │   └── qa_service.py    # Q&A service
│   │   └── main.py             # FastAPI application
│   ├── alembic/                # Database migrations
│   │   ├── versions/           # Migration scripts
│   │   └── env.py              # Alembic environment
│   ├── alembic.ini             # Alembic configuration
│   ├── nlp_pipeline.py         # NLP processing pipeline
│   └── .env                    # Environment variables
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest configuration and fixtures
│   ├── README.md               # Test documentation
│   ├── unit/                   # Unit tests
│   │   ├── test_config.py
│   │   ├── test_database.py
│   │   ├── test_nlp.py
│   │   └── test_repositories.py
│   └── integration/            # Integration tests
│       └── test_api.py
├── docs/                       # Documentation
│   ├── DATABASE_MIGRATION.md   # Database migration guide
│   └── MITRA_BACKEND_ARCHITECTURE.md # Backend architecture documentation
├── venv/                       # Virtual environment (created during installation)
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .env.example                # Environment variables example
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Configuration

The application settings are configured using environment variables. Create a `.env` file in the `backend/` directory (see `.env.example` for reference):

### Environment Variables

- `DATABASE_URL`: Database connection string (default: `mysql+pymysql://mitra_user:password@localhost:3306/mitra_db`)
  - MySQL: `mysql+pymysql://user:password@localhost:3306/database_name`
- `API_HOST`: API host (default: `127.0.0.1`)
- `API_PORT`: API port (default: `8000`)
- `APP_ENV`: Application environment (default: `development`)
- `DEBUG`: Debug mode (default: `True`)
- `SPACY_MODEL`: spaCy model name (default: `en_core_web_sm`)
- `CONFIDENCE_THRESHOLD`: NLP confidence threshold (default: `0.5`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `JWT_SECRET_KEY`: Secret key for JWT token signing (default: test-secret)
- `JWT_ALGORITHM`: JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time in minutes (default: `30`)

### Example `.env` file

```bash
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/mitra_db

# API
API_HOST=127.0.0.1
API_PORT=8000

# Application
APP_ENV=development
DEBUG=True

# NLP
SPACY_MODEL=en_core_web_sm
CONFIDENCE_THRESHOLD=0.5

# Logging
LOG_LEVEL=INFO

# Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Health Check
- `GET /`: API health check
- `GET /health`: Detailed health status

### Chat
- `POST /chat`: Main chat endpoint for processing user queries (supports both authenticated and guest users)
  - Request body: `{"user_input": "string", "user_context": {}, "conversation_history": []}`
  - Response: `{"response": "string", "intent": "string", "confidence": float, "entities": []}`

### Authentication
- `POST /api/auth/register`: Register a new user
  - Request body: `{"username": "string", "email": "string", "password": "string", "full_name": "string"}`
  - Response: User object (without password hash)
- `POST /api/auth/login`: Login with username/email and password
  - Request body: `{"username_or_email": "string", "password": "string"}`
  - Response: `{"access_token": "string", "token_type": "bearer"}`
- `GET /api/auth/me`: Get current authenticated user
  - Requires: Bearer token in Authorization header
  - Response: User object

### Q&A Management (Requires Authentication)
- `POST /qa`: Add a new Q&A pair to the knowledge base
  - Requires: Bearer token in Authorization header
  - Request body: `{"question": "string", "answer": "string"}`
  - Response: `{"message": "string", "id": int}`
- `GET /qa`: Retrieve Q&A pairs (optional question filter)
  - Requires: Bearer token in Authorization header
  - Query param: `?question=search_term`
  - Response: Array of Q&A pairs

### Intents
- `GET /intents`: Get list of available intents
  - Response: `{"intents": ["admission", "course", "facility", "contact", "general"]}`

For detailed API documentation, visit `http://localhost:8000/docs` when the backend is running.

## Database Migrations

The project uses Alembic for database migrations. This allows you to version control your database schema and make changes in a structured way.

### Creating a New Migration

```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

### Applying Migrations

```bash
cd backend
alembic upgrade head
```

### Rolling Back Migrations

```bash
cd backend
alembic downgrade -1
```

### Migration History

```bash
cd backend
alembic history
```

For more details, see [DATABASE_MIGRATION.md](docs/DATABASE_MIGRATION.md).

## Development

### Running in Development Mode

Backend with auto-reload:

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Streamlit with auto-reload:

```bash
cd frontend
streamlit run main.py --server.runOnSave true
```

### Testing

The project uses pytest for testing. The test suite is organized into unit tests and integration tests.

#### Run All Tests

```bash
pytest tests/ -v
```

#### Run Only Unit Tests

```bash
pytest tests/ -m unit -v
```

#### Run Only Integration Tests

```bash
pytest tests/ -m integration -v
```

#### Run with Coverage

```bash
pytest tests/ --cov=backend/app --cov-report=html
```

For detailed testing documentation, see [tests/README.md](tests/README.md).

## Deployment

### MySQL Setup

#### 1. Set up MySQL Server

Install MySQL 8.x on your server or use a managed MySQL service (AWS RDS, Google Cloud SQL, etc.).

#### 2. Create Database

```sql
CREATE DATABASE mitra CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mitra_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON mitra.* TO 'mitra_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. Configure Environment Variables

Set the `DATABASE_URL` environment variable:

```bash
DATABASE_URL=mysql+pymysql://mitra_user:secure_password@localhost:3306/mitra
```

#### 4. Run Migrations

```bash
cd backend
alembic upgrade head
```

#### 5. Start the Application

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Cloud Deployment

- **Frontend**: Deploy on Streamlit Community Cloud
- **Backend**: Deploy on Heroku, AWS, or similar platforms
- **Database**: Use managed MySQL service (AWS RDS, Google Cloud SQL, etc.)

#### Heroku Example

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create mitra-backend

# Set environment variables
heroku config:set DATABASE_URL=mysql+pymysql://...

# Deploy
git push heroku main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable (follow the testing guidelines in `tests/README.md`)
5. Ensure all tests pass: `pytest tests/ -v`
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please contact the development team or create an issue in the repository.

## Contact

**Developer**: Madhan Mohan Reddy  
**Email**: [madhanmohanreddyperam06@gmail.com](mailto:madhanmohanreddyperam06@gmail.com)  
**Mobile**: +91 9110395993  

Feel free to reach out for collaborations, support, or any inquiries about the MITRA project.

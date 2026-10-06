# MITRA Backend Architecture - Phase 1, Phase 2, and Phase 3

## Overview

This document describes the refactored backend architecture implemented in Phase 1 of MITRA 2.0, with MySQL migration in Phase 2 and authentication/user management in Phase 3. The architecture follows a layered pattern that separates concerns and supports secure multi-user access.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                             │
│         (FastAPI Routes & Request Handling)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Authentication Layer                         │
│      (JWT Validation & Authorization Dependencies)        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Service Layer                           │
│         (Business Logic & Coordination)                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                Repository Layer                           │
│            (Data Access Abstraction)                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              SQLAlchemy ORM                               │
│         (Database Abstraction Layer)                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  MySQL 8.x Database                     │
│         (Migrated from SQLite in Phase 2)               │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### API Layer (`app/api/`)

**Purpose:** Handle HTTP requests and responses, request validation, and HTTP-specific concerns.

**Components:**
- `chat.py` - Chat endpoint for processing user queries
- `knowledge.py` - Q&A management endpoints
- `health.py` - Health check and root endpoints
- `intents.py` - Intent listing endpoint
- `auth.py` - Authentication endpoints (register, login, me) (Phase 3)
- `users.py` - User management endpoints (admin-only) (Phase 3)

**Responsibilities:**
- Receive and validate HTTP requests using Pydantic schemas
- Call appropriate service layer methods
- Return structured HTTP responses
- Handle HTTP-specific errors
- Log request metadata (method, path, status, timing)
- Apply authentication and authorization dependencies

**Example:**
```python
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Validate request (handled by Pydantic)
    # User is authenticated (current_user from JWT)
    # Call service layer
    # Return response
```

### Authentication Layer (`app/core/security.py`)

**Purpose:** Provide reusable authentication and authorization dependencies.

**Components:**
- `get_current_user` - JWT validation and user retrieval
- `get_current_active_user` - Ensures user is active
- `get_current_admin` - Ensures user is administrator
- `get_auth_service` - Dependency injection for AuthService

**Responsibilities:**
- Validate JWT tokens from Authorization header
- Decode tokens and extract user identity
- Fetch user from database
- Verify user is active
- Verify user is admin (for admin endpoints)
- Return appropriate HTTP errors for unauthorized access

**Example:**
```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user_id = payload.get("sub")
    user = auth_service.user_repo.get_by_id(user_id)
    if not user or not user['is_active']:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
```

**Security Features:**
- JWT tokens with configurable expiration (default 30 minutes)
- Bcrypt password hashing (never plaintext)
- Single admin account enforcement
- Inactive user rejection
- Admin self-destruction prevention
- Generic error messages (don't reveal account existence)

### Service Layer (`app/services/`)

**Purpose:** Coordinate business logic and orchestrate data access.

**Components:**
- `chat_service.py` - Chat query processing and response generation
- `auth_service.py` - Authentication and user management business logic

**Responsibilities:**
- Implement business logic
- Coordinate multiple repositories
- Process data from repositories into business objects
- Handle application-level exceptions
- No direct database access - only through repositories

**AuthService (Phase 3):**
- Password hashing and verification (bcrypt)
- JWT token creation and validation
- User registration with validation
- User authentication with credentials
- Admin user creation (restricted)
- User activation/deactivation
- Email normalization
- Password policy enforcement

**Example:**
```python
class ChatService:
    def __init__(self, admission_repo, course_repo, ...):
        self.admission_repo = admission_repo
        # ...

    def process_query(self, intent, entities, ...):
        if intent == "admission_info":
            return self._handle_admission_query(...)
        # Business logic here
```

### Repository Layer (`app/database/repositories/`)

**Purpose:** Abstract data access and provide a clean interface to the database.

**Components:**
- `admissions.py` - Admission data access
- `courses.py` - Course data access
- `facilities.py` - Facility data access
- `contacts.py` - Contact information access
- `qa.py` - Q&A dataset access
- `users.py` - User management data access (Phase 3)

**Responsibilities:**
- Execute database queries
- Map database rows to domain objects/dictionaries
- Handle database-specific errors
- Provide CRUD operations
- No business logic

**UserRepository (Phase 3):**
- `get_by_id` - Fetch user by ID
- `get_by_email` - Fetch user by email
- `get_by_username` - Fetch user by username
- `get_by_email_with_hash` - Fetch user with password hash (for auth)
- `get_by_username_with_hash` - Fetch user with password hash (for auth)
- `list_users` - List all users
- `create_user` - Create new user
- `update_user` - Update user fields
- `delete_user` - Delete user
- `count_admins` - Count admin users (for single-admin enforcement)
- `update_last_login` - Update last login timestamp

**Example:**
```python
class AdmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict]:
        result = self.db.execute(select(Admission))
        return [/* map to dict */ for admission in result.scalars()]
```

### Database Layer (`app/database/`)

**Purpose:** Provide database connection management and ORM models.

**Components:**
- `connection.py` - Database engine and session management
- `models.py` - SQLAlchemy ORM models matching actual database schema

**Responsibilities:**
- Manage database connections
- Provide session lifecycle management
- Define database schema in code
- Handle connection pooling
- Abstract database-specific details

**Key Features:**
- Single engine instance
- Session factory for creating sessions
- Dependency injection pattern for sessions
- Automatic session cleanup

### Core Layer (`app/core/`)

**Purpose:** Provide cross-cutting concerns and shared utilities.

**Components:**
- `config.py` - Centralized configuration management
- `logging.py` - Structured logging configuration
- `exceptions.py` - Custom application exceptions
- `error_handlers.py` - Global FastAPI error handlers
- `security.py` - Authentication and authorization dependencies (Phase 3)

**Responsibilities:**
- Load and validate configuration
- Configure application logging
- Define domain-specific exceptions
- Handle errors consistently across the application

## Configuration Management

Configuration is centralized in `app/core/config.py` using Pydantic Settings:

**Features:**
- Environment variable support via `.env` file
- Type-safe configuration
- Default values for all settings
- Validation at startup
- Environment-specific settings (development/production)

**Key Settings:**
- `APP_NAME`, `APP_ENV`, `DEBUG` - Application configuration
- `API_HOST`, `API_PORT` - API server configuration
- `DATABASE_URL` - Database connection string
- `CORS_ALLOWED_ORIGINS` - CORS configuration
- `JWT_SECRET_KEY` - JWT signing secret (Phase 3)
- `JWT_ALGORITHM` - JWT algorithm (Phase 3)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration (Phase 3)
- `SPACY_MODEL`, `CONFIDENCE_THRESHOLD` - NLP configuration
- `LOG_LEVEL` - Logging configuration

**Usage:**
```python
from app.core.config import settings

db_url = settings.DATABASE_URL
log_level = settings.LOG_LEVEL
```

## Logging

Centralized logging configuration in `app/core/logging.py`:

**Features:**
- Structured log format with timestamp, logger name, level, and message
- Configurable log level via environment
- UTF-8 encoding support for special characters
- Separate log levels for different libraries
- Request/response logging middleware

**Log Levels:**
- **INFO**: Application startup, API requests, successful operations
- **WARNING**: Low confidence intent detection, missing knowledge
- **ERROR**: Database failures, unexpected exceptions

**Request Logging:**
All HTTP requests are logged with:
- HTTP method
- Endpoint path
- Status code
- Response time in milliseconds

**Example:**
```
2026-10-05 19:26:05 - app.core.logging - INFO - POST /chat -> 200 -> 89ms
```

## Error Handling

Custom exceptions defined in `app/core/exceptions.py`:

**Exception Hierarchy:**
```
MITRAError (base)
├── DatabaseError
├── KnowledgeNotFoundError
├── InvalidQueryError
├── NLPProcessingError
└── ConfigurationError
```

**Global Error Handlers:**
- Custom MITRA exceptions return structured error responses
- Generic exceptions return safe internal error messages
- No stack traces or internal details exposed to users

**Error Response Format:**
```json
{
  "success": false,
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Failed to fetch admission info"
  }
}
```

## CORS Configuration

CORS is configuration-driven via `settings.CORS_ALLOWED_ORIGINS`:

**Features:**
- Configured from environment variables
- Default allows Streamlit development server
- Production origins set via environment
- Credentials, methods, and headers properly configured

**Example:**
```python
# Development
CORS_ALLOWED_ORIGINS=["http://localhost:8501"]

# Production
CORS_ALLOWED_ORIGINS=["https://mitra.example.com"]
```

## API Validation

Request validation using Pydantic schemas in `app/schemas/`:

**Chat Request Validation:**
- `user_input`: Required, 1-1000 characters, non-empty after stripping
- `user_context`: Optional dictionary
- `conversation_history`: Optional list, max 20 entries

**Knowledge Request Validation:**
- `question`: Required, 1-500 characters
- `answer`: Required, 1-2000 characters

**Authentication Request Validation (Phase 3):**
- `UserRegister`: username (3-50 chars, alphanumeric), email (valid email), password (8-128 chars), full_name (optional)
- `UserLogin`: username_or_email (required), password (required)
- `UserStatusUpdate`: is_active (boolean)

**Benefits:**
- Automatic validation before business logic
- Clear error messages for invalid input
- Type safety
- OpenAPI documentation generation

## Database Models

SQLAlchemy models in `app/database/models.py` match the actual database schema:

**Models:**
- `Admission` - Admissions table
- `Course` - Courses table
- `Facility` - Facilities table
- `ContactInfo` - Contact information table
- `QADataset` - Q&A dataset table
- `User` - Users table (Phase 3)

**User Model (Phase 3):**
- `id` - Primary key, auto-increment
- `username` - Unique, indexed, lowercase
- `email` - Unique, indexed, normalized to lowercase
- `password_hash` - Bcrypt hash (never plaintext)
- `full_name` - Optional display name
- `is_active` - Account status (default: True)
- `is_admin` - Admin flag (default: False)
- `created_at` - UTC timestamp of creation
- `updated_at` - UTC timestamp of last update
- `last_login_at` - UTC timestamp of last login

**Key Points:**
- Models reflect actual database schema (not the initial schema mismatch)
- Primary keys are auto-incrementing integers
- User model includes timestamps for tracking
- Ready for future schema evolution

## Session Management

Database sessions follow the dependency injection pattern:

**Pattern:**
```python
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Usage in Routes:**
```python
@router.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # Use db for repository operations
    repo = AdmissionRepository(db)
    # Session automatically closed after request
```

**Benefits:**
- Automatic session cleanup
- No resource leaks
- Testable with dependency injection
- Clear session lifecycle

## Backward Compatibility

The refactored architecture maintains backward compatibility:

**Existing Endpoints Preserved:**
- `GET /` - Root endpoint (public)
- `GET /health` - Health check (public)
- `GET /intents` - Available intents (public)
- `POST /chat` - Chat endpoint (now requires authentication)
- `GET /qa` - Get Q&A pairs (now requires authentication)
- `POST /qa` - Add Q&A pair (now requires authentication)

**New Endpoints (Phase 3):**
- `POST /api/auth/register` - User registration (public)
- `POST /api/auth/login` - User login (public)
- `GET /api/auth/me` - Get current user (authenticated)
- `GET /api/users` - List users (admin-only)
- `GET /api/users/{id}` - Get user by ID (admin-only)
- `PATCH /api/users/{id}/status` - Update user status (admin-only)
- `DELETE /api/users/{id}` - Delete user (admin-only)

**Authorization Changes (Phase 3):**
- Chat endpoint supports both authenticated and guest users (optional authentication)
- Knowledge endpoints now require JWT authentication
- User management endpoints require admin authentication
- Streamlit frontend updated to handle login/logout

**No Breaking Changes:**
- Request/response formats for existing endpoints unchanged
- Original NLP pipeline preserved
- Original response generation logic preserved
- Database schema extended (users table added)

## Testing Strategy

Test suite organized into unit and integration tests:

**Unit Tests (`tests/unit/`):**
- `test_config.py` - Configuration management
- `test_repositories.py` - Repository layer with in-memory database
- `test_auth.py` - Authentication service and password hashing (Phase 3)
- `test_nlp.py` - NLP pipeline (baseline)
- `test_response_generator.py` - Response generator (baseline)
- `test_database.py` - Knowledge base (baseline)

**Integration Tests (`tests/integration/`):**
- `test_api.py` - API endpoints with test database
- `test_auth.py` - Authentication API endpoints (Phase 3)
- `test_mysql_integration.py` - MySQL database integration (Phase 2)

**Test Isolation:**
- Unit tests use in-memory SQLite databases
- Integration tests use temporary SQLite databases
- No modification to production database
- Tests clean up after themselves

## Future Readiness

The architecture is designed to support future enhancements:

**SQLite → MySQL Migration (Phase 2 - Completed):**
- Database URL is configuration-driven
- SQLAlchemy abstracts database-specific details
- Repository layer unchanged
- Service layer unchanged
- Alembic migrations for schema version control
- Production-ready MySQL 8.x database

**Authentication (Phase 3 - Completed):**
- JWT-based authentication with bcrypt password hashing
- Single-admin model with user management
- Protected endpoints for chat and knowledge base
- Streamlit login/logout integration
- Comprehensive security test coverage
- Authentication documentation

**RAG/LLM Integration (Future Phase):**
- Service layer can be extended with RAG logic
- Repository layer can add vector database access
- NLP pipeline can be enhanced with LLM
- Current template-based responses remain as fallback

**RAG/LLM Integration (Future Phase):**
- Service layer can be extended with RAG logic
- Repository layer can add vector database access
- NLP pipeline can be enhanced with LLM
- Current template-based responses remain as fallback

## File Structure

```
backend/
├── app/
│   ├── main.py                          # FastAPI application entry point
│   ├── api/                             # API layer
│   │   ├── __init__.py
│   │   ├── chat.py                      # Chat endpoints
│   │   ├── knowledge.py                 # Knowledge management endpoints
│   │   ├── health.py                    # Health check endpoints
│   │   ├── intents.py                   # Intent listing endpoint
│   │   ├── auth.py                      # Authentication endpoints (Phase 3)
│   │   └── users.py                     # User management endpoints (Phase 3)
│   ├── core/                            # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuration management
│   │   ├── logging.py                   # Logging configuration
│   │   ├── exceptions.py                # Custom exceptions
│   │   └── error_handlers.py            # Global error handlers
│   ├── database/                        # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py                # Database connection management
│   │   ├── models.py                    # SQLAlchemy ORM models
│   │   └── repositories/               # Repository layer
│   │       ├── __init__.py
│   │       ├── admissions.py
│   │       ├── courses.py
│   │       ├── facilities.py
│   │       ├── contacts.py
│   │       └── qa.py
│   ├── schemas/                         # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── chat.py                      # Chat request/response schemas
│   │   ├── knowledge.py                 # Knowledge management schemas
│   │   └── auth.py                      # Authentication schemas (Phase 3)
│   ├── services/                        # Service layer
│   │   ├── __init__.py
│   │   ├── chat_service.py              # Chat business logic
│   │   └── auth_service.py              # Authentication business logic (Phase 3)
│   └── nlp/                             # NLP layer (preserved)
│       └── __init__.py
├── scripts/                             # Utility scripts
│   ├── create_admin.py                  # Admin initialization script (Phase 3)
│   ├── migrate_sqlite_to_mysql.py       # SQLite to MySQL migration (Phase 2)
│   └── validate_mysql_migration.py     # Migration validation (Phase 2)
├── knowledge_base.py                    # Legacy knowledge base (preserved)
├── nlp_pipeline.py                      # Legacy NLP pipeline (preserved)
├── response_generator.py                # Legacy response generator (preserved)
├── main.py                              # Legacy main entry point (preserved)
├── .env.example                         # Environment variables template
└── requirements.txt                     # Python dependencies

streamlit_app/
├── main.py                              # Streamlit application entry point
├── components/                          # Streamlit components
│   ├── __init__.py
│   ├── chat_interface.py               # Chat UI component
│   ├── sidebar.py                      # Sidebar component
│   └── auth.py                         # Authentication component (Phase 3)
└── pages/                               # Streamlit pages (if any)
```

## Summary

The Phase 1 refactoring successfully:

1. **Separated Concerns**: Clear separation between API, service, and repository layers
2. **Abstracted Database**: SQLAlchemy provides database abstraction for easy migration
3. **Centralized Configuration**: Environment-based configuration management
4. **Structured Logging**: Consistent, structured logging throughout the application
5. **Improved Error Handling**: Custom exceptions and global error handlers
6. **Enhanced Validation**: Pydantic schemas for request validation
7. **Configured CORS**: Environment-driven CORS configuration
8. **Maintained Compatibility**: All existing functionality preserved
9. **Expanded Testing**: Comprehensive test suite with unit and integration tests
10. **Future-Ready**: Architecture supports MySQL migration, authentication, and RAG/LLM integration

Phase 2 added:

11. **MySQL Migration**: Successful migration from SQLite to MySQL 8.x
12. **Alembic Integration**: Database version control and migrations
13. **Production Database**: Production-ready MySQL database setup

Phase 3 added:

14. **Authentication Layer**: JWT-based authentication with bcrypt password hashing
15. **User Management**: Single-admin model with user CRUD operations
16. **Secure Endpoints**: Protected chat and knowledge endpoints
17. **Streamlit Auth**: Login/logout integration in Streamlit frontend
18. **Admin Protection**: Safety mechanisms to prevent admin lockout
19. **Security Tests**: Comprehensive authentication and authorization test coverage
20. **Security Documentation**: Detailed authentication and security documentation

The architecture is now clean, maintainable, secure, and ready for future enhancements including RBAC, persistent conversations, and RAG/LLM integration.

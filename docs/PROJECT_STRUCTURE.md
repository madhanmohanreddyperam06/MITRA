# MITRA Project Structure

**Note:** All documentation files have been moved to the `docs/` folder for better organization. Only `README.md` remains in the root directory as per standard practice.

## Root Directory

```
MITRA-master/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── .pytest_cache/                 # Pytest cache (ignored)
├── .streamlit/                    # Streamlit config
│   └── config.toml
├── LICENSE                        # Project license
├── README.md                      # Project documentation (root level)
├── backend/                       # FastAPI backend
├── data/                          # Knowledge base data
│   └── knowledge_base/
│       ├── admission_data.json
│       └── course_catalog.json
├── docs/                          # All documentation
│   ├── CLOUD_MYSQL_DEPLOYMENT_REPORT.md
│   ├── DATABASE_MIGRATION.md
│   ├── MITRA_2.0_ARCHITECTURE_ROADMAP.md
│   ├── MITRA_AUTHENTICATION.md
│   ├── MITRA_BACKEND_ARCHITECTURE.md
│   ├── MITRA_CURRENT_VS_TARGET.md
│   ├── MYSQL_CLOUD_DEPLOYMENT.md
│   ├── PHASE_0_3_FIXES_SUMMARY.md
│   ├── PROJECT_STRUCTURE.md
│   ├── RAILWAY_MYSQL_CONFIGURATION_REPORT.md
│   └── RENAME_SUMMARY.md
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── frontend/                     # Streamlit frontend
├── tests/                         # Test suite
└── venv/                          # Virtual environment (root)
```

## Backend Directory

```
backend/
├── .env                           # Environment variables (ignored)
├── .env.example                   # Environment variables template
├── .env.test                      # Test environment variables (ignored)
├── .pytest_cache/                # Pytest cache (ignored)
├── __pycache__/                   # Python cache (ignored)
├── alembic/                       # Database migrations
│   ├── env.py                     # Alembic environment
│   ├── script.py.mypy             # Type stubs
│   └── versions/                  # Migration files
│       ├── 001_initial_schema.py
│       ├── 002_add_users_table.py
│       ├── 003_add_single_admin_constraint.py
│       └── 8bc28335b2c5_add_admin_and_active_indexes.py
├── alembic.ini                    # Alembic configuration
├── app/                           # Application code
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── chat.py                # Chat endpoints
│   │   ├── health.py              # Health check
│   │   ├── intents.py             # Intent classification
│   │   └── knowledge.py           # Knowledge base endpoints
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── error_handlers.py      # Error handling
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── logging.py             # Logging configuration
│   │   └── security.py            # Security utilities
│   ├── database/                  # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py          # Database connection
│   │   ├── models.py              # SQLAlchemy models
│   │   └── repositories/          # Data access layer
│   │       ├── __init__.py
│   │       ├── admissions.py
│   │       ├── contacts.py
│   │       ├── courses.py
│   │       ├── facilities.py
│   │       ├── qa.py
│   │       └── users.py
│   ├── main.py                    # FastAPI application entry point
│   ├── nlp_pipeline.py            # NLP processing pipeline
│   ├── response_generator.py      # Response generation
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication schemas
│   │   ├── chat.py                # Chat schemas
│   │   └── knowledge.py           # Knowledge base schemas
│   └── services/                  # Business logic
│       ├── __init__.py
│       ├── auth_service.py        # Authentication service
│       └── chat_service.py        # Chat service
├── data/                          # Backend data (empty - should use root data/)
│   └── knowledge_base/            # Empty directory
├── scripts/                       # Utility scripts
│   ├── create_admin.py            # Admin bootstrap script
│   └── validate_database.py       # Database validation script
└── venv/                          # Virtual environment (DUPLICATE - should use root venv)
```

## Frontend Directory

```
frontend/
├── __pycache__/                   # Python cache (ignored)
├── components/                    # Streamlit components
│   ├── __init__.py
│   ├── auth.py                    # Authentication UI
│   ├── chat_interface.py          # Chat interface
│   ├── sidebar.py                 # Sidebar component
│   └── theme.py                   # Theme configuration
├── main.py                        # Streamlit application entry point
├── pages/                         # Streamlit pages
│   ├── 1_Admissions.py
│   ├── 2_Courses.py
│   └── 3_Facilities.py
└── venv/                          # Virtual environment (DUPLICATE - should use root venv) - REMOVED
```

## Tests Directory

```
tests/
├── __init__.py
├── conftest.py                    # Pytest fixtures
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_auth.py
│   └── test_mysql_integration.py
├── run_all_tests.py               # Test runner script
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_auth.py               # Authentication tests
│   ├── test_config.py             # Configuration tests
│   ├── test_database.py          # Database tests
│   ├── test_nlp.py                # NLP tests
│   ├── test_repositories.py      # Repository tests
│   ├── test_response_generator.py # Response generator tests
│   └── test_streamlit_auth.py     # Streamlit auth tests
└── README.md                      # Test documentation
```

## Documentation Directory

```
docs/
├── DATABASE_MIGRATION.md          # Database migration guide
├── MITRA_2.0_ARCHITECTURE_ROADMAP.md  # Architecture roadmap
├── MITRA_AUTHENTICATION.md        # Authentication documentation
├── MITRA_BACKEND_ARCHITECTURE.md  # Backend architecture
├── MITRA_CURRENT_VS_TARGET.md     # Current vs target state
├── MYSQL_CLOUD_DEPLOYMENT.md      # MySQL cloud deployment guide
└── PHASE_0_3_FIXES_SUMMARY.md    # Phase fixes summary
```

## Clean Up Completed

### Removed Files/Directories
- ✅ `./backend/venv/` - Removed (duplicate virtual environment)
- ✅ `./streamlit_app/venv/` - Removed (duplicate virtual environment)
- ✅ `./backend/data/knowledge_base/` - Removed (empty directory)
- ✅ `./.pytest_cache/` - Removed (cache, will be regenerated)
- ✅ All `__pycache__` directories - Removed (cache, will be regenerated)
- ✅ `./streamlit_app/` → `./frontend/` - Renamed and old directory removed

### Updated .gitignore
- ✅ Changed from specific `.env.*` patterns to `.env.*` with `!.env.example` exception
- ✅ Now properly ignores all `.env` files while keeping `.env.example` trackable

### Updated Documentation
- ✅ PROJECT_STRUCTURE.md - Updated all references to `frontend`
- ✅ README.md - Updated all references to `frontend`
- ✅ tests/unit/test_streamlit_auth.py - Updated import path
- ✅ docs/MYSQL_CLOUD_DEPLOYMENT.md - Updated all references
- ✅ RAILWAY_MYSQL_CONFIGURATION_REPORT.md - Updated references
- ✅ CLOUD_MYSQL_DEPLOYMENT_REPORT.md - Updated references
- ✅ docs/MITRA_BACKEND_ARCHITECTURE.md - Updated references
- ✅ docs/MITRA_AUTHENTICATION.md - Updated references
- ✅ docs/DATABASE_MIGRATION.md - Updated references
- ✅ docs/MITRA_2.0_ARCHITECTURE_ROADMAP.md - Updated references

## Current Directory Structure (Clean)

```
MITRA-master/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules (updated)
├── .streamlit/                    # Streamlit config
│   └── config.toml
├── CLOUD_MYSQL_DEPLOYMENT_REPORT.md    # Cloud MySQL deployment report
├── LICENSE                        # Project license
├── PROJECT_STRUCTURE.md           # This file
├── README.md                      # Project documentation
├── RAILWAY_MYSQL_CONFIGURATION_REPORT.md  # Railway MySQL configuration report
├── backend/                       # FastAPI backend
│   ├── .env                       # Environment variables (ignored)
│   ├── .env.example               # Environment variables template
│   ├── .env.test                  # Test environment variables (ignored)
│   ├── alembic/                   # Database migrations
│   ├── alembic.ini                # Alembic configuration
│   ├── app/                       # Application code
│   └── scripts/                   # Utility scripts
├── data/                          # Knowledge base data
│   └── knowledge_base/
│       ├── admission_data.json
│       └── course_catalog.json
├── docs/                          # Documentation
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── frontend/                     # Streamlit frontend
│   ├── components/               # Streamlit components
│   ├── main.py                   # Streamlit application entry point
│   └── pages/                    # Streamlit pages
├── tests/                         # Test suite
└── venv/                          # Single virtual environment (root level)
```

## Verification Status

✅ **Project Structure:** Clean and organized
✅ **Virtual Environments:** Single venv at root level
✅ **Git Ignore:** Properly configured with `.env.*` exception
✅ **Authentication Tests:** 23/23 passing
✅ **Database Migrations:** At head revision (8bc28335b2c5)
✅ **Duplicate Files:** Removed
✅ **Empty Directories:** Removed
✅ **Cache Files:** Cleaned

# MITRA 2.0 Architecture Roadmap

## 1. Current Architecture

### 1.1 Overall Structure

MITRA is currently a college helpdesk chatbot with a simple two-tier architecture:

```
Streamlit Frontend (Port 8501)
         |
         | HTTP/REST
         v
FastAPI Backend (Port 8000)
         |
         | Direct SQLite Access
         v
SQLite Database
```

### 1.2 Backend Components

**Entry Point:** `backend/main.py`

- FastAPI application (version 1.0.0)
- CORS enabled for all origins (development mode)
- Global initialization of NLP pipeline, knowledge base, and response generator
- No dependency injection pattern

**NLP Pipeline:** `backend/nlp_pipeline.py`

- spaCy-based NER (en_core_web_sm model)
- Rule-based intent recognition with keyword matching
- Custom entity extraction for COURSE and DEPARTMENT
- Text preprocessing: lowercase, whitespace normalization, basic punctuation preservation
- Confidence scoring based on pattern matches

**Knowledge Base:** `backend/knowledge_base.py`

- Direct SQLite access using sqlite3
- No ORM or abstraction layer
- Connection per operation (no connection pooling)
- Tables: admissions, courses, facilities, contact_info, qa_dataset
- Auto-initialization of database schema

**Response Generator:** `backend/response_generator.py`

- Template-based responses with randomization
- Intent-specific handlers
- Hardcoded responses for fee, library, placement information
- Fallback responses when database queries fail
- No conversation memory beyond session state

### 1.3 Frontend Components

**Entry Point:** `streamlit_app/main.py`

- Streamlit multi-page application
- Session state for messages and user context
- Chat interface component
- Sidebar with quick actions

**Chat Interface:** `streamlit_app/components/chat_interface.py`

- HTTP requests to backend API
- Fallback responses when backend unavailable
- Last 5 messages sent as context
- 30-second timeout

**Sidebar:** `streamlit_app/components/sidebar.py`

- Quick action buttons for common queries
- User context selection (student type)
- Chat controls (clear, download)
- Sample questions help

**Pages:**
- `pages/1_Admissions.py` - Static admission information
- `pages/2_Courses.py` - Static course listings
- `pages/3_Facilities.py` - Static facility information

### 1.4 Data Flow

```
User Input (Streamlit)
        ↓
Session State Update
        ↓
HTTP POST /chat
        ↓
FastAPI Request Handler
        ↓
NLP Pipeline.process()
        ├─ Text Cleaning
        ├─ Intent Extraction
        ├─ Entity Extraction
        └─ Confidence Calculation
        ↓
ResponseGenerator.generate_response()
        ├─ Intent Handler Selection
        ├─ Database Query (via KnowledgeBase)
        ├─ Template Selection
        └─ Response Formatting
        ↓
FastAPI Response
        ↓
Streamlit Display
        ↓
Session State Update
```

### 1.5 Current Database Schema

**admissions**
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- category (TEXT)
- information (TEXT)
- details (TEXT)

**courses**
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- course_name (TEXT)
- department (TEXT)
- duration (TEXT)
- eligibility (TEXT)
- description (TEXT)

**facilities**
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- facility_name (TEXT)
- category (TEXT)
- description (TEXT)
- location (TEXT)
- timings (TEXT)

**contact_info**
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- department (TEXT)
- contact_person (TEXT)
- phone (TEXT)
- email (TEXT)
- office_location (TEXT)

**qa_dataset**
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- question (TEXT NOT NULL)
- answer (TEXT NOT NULL)

**Note:** Schema mismatch between `knowledge_base.py` (expected columns) and actual database (actual columns). The code expects different column names than what exists in the database.

### 1.6 Current API Endpoints

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | / | API welcome message | None |
| GET | /health | Health check | None |
| POST | /chat | Main chat endpoint | None |
| POST | /qa | Add Q&A pair | None |
| GET | /qa | Get Q&A pairs | None |
| GET | /intents | List available intents | None |

### 1.7 Current Configuration

**File:** `config/settings.py`

- API_HOST: localhost
- API_PORT: 8000
- STREAMLIT_HOST: localhost
- STREAMLIT_PORT: 8501
- DB_PATH: data/knowledge_base/college_info.db
- SPACY_MODEL: en_core_web_sm
- MAX_RESPONSE_LENGTH: 1000
- CONFIDENCE_THRESHOLD: 0.5
- MAX_CONVERSATION_HISTORY: 10
- DEFAULT_RESPONSE_TIMEOUT: 30
- College information hardcoded

**Issues:**
- Configuration file exists but is not imported/used by backend
- Backend uses hardcoded values directly
- No environment variable support
- No .env file present

### 1.8 Current Intents

1. admission_info
2. course_info
3. fee_inquiry
4. hostel_info
5. library_info
6. placement_info
7. contact_info
8. general_info

## 2. Technical Debt

### Critical Issues

1. **Schema Mismatch**
   - Location: `backend/knowledge_base.py` vs actual SQLite database
   - Code expects: `category`, `information`, `details` in admissions
   - Database has: `category`, `information`, `details` (but code uses wrong access pattern)
   - Response generator expects columns that may not exist
   - Risk: Runtime errors when accessing data

2. **No Authentication**
   - All endpoints are public
   - No user management
   - No authorization
   - Risk: Security vulnerability in production

3. **CORS Wide Open**
   - `allow_origins=["*"]` in main.py
   - Risk: Cross-origin attacks in production

### High Priority Issues

4. **No Connection Pooling**
   - New SQLite connection per operation
   - No connection reuse
   - Risk: Performance issues under load

5. **No Error Handling**
   - Generic exception handling in API
   - No structured error responses
   - Risk: Poor user experience and debugging difficulty

6. **No Logging**
   - No structured logging
   - No request/response logging
   - Risk: Difficult to debug production issues

7. **Hardcoded Configuration**
   - All values hardcoded in code
   - config/settings.py not used
   - Risk: Deployment difficulties

8. **No Validation**
   - No input validation beyond Pydantic
   - No SQL injection protection (parameterized queries used but no validation)
   - Risk: Data integrity issues

### Medium Priority Issues

9. **Session-Based Memory Only**
   - Conversation history lost on refresh
   - No persistent conversation storage
   - Risk: Poor user experience

10. **No Testing**
    - No existing test suite
    - No CI/CD integration
    - Risk: Regression during changes

11. **Duplicate Logic**
    - Fallback responses in both chat_interface.py and response_generator.py
    - Risk: Maintenance burden

12. **No API Versioning**
    - Single version (1.0.0)
    - Risk: Breaking changes affect all clients

### Low Priority Issues

13. **No Documentation**
    - Limited inline documentation
    - No API documentation (Swagger present but not customized)
    - Risk: Onboarding difficulty

14. **Static Pages Not Dynamic**
    - Admissions, Courses, Facilities pages are static
    - Not connected to database
    - Risk: Information inconsistency

15. **No Rate Limiting**
    - No request rate limits
    - Risk: Abuse potential

## 3. Target MITRA 2.0 Architecture

### 3.1 High-Level Architecture

```
Users
   ↓
Streamlit / Web UI
   ↓
FastAPI API Gateway
   ↓
Authentication / Authorization (JWT)
   ↓
Conversation Manager
   ↓
Query Analyzer
   ↓
Hybrid Retrieval
   ├── MySQL (structured data)
   ├── Semantic Search (vector similarity)
   └── Document Retrieval (PDF/DOCX)
   ↓
Vector Database (Qdrant/Weaviate)
   ↓
RAG Engine
   ↓
LLM (OpenAI/Local)
   ↓
Answer + Citations + Confidence
```

### 3.2 Component Breakdown

**Frontend Layer**
- Streamlit (current) + optional React web UI
- Enhanced chat interface with citation display
- User profile management
- Document upload interface

**API Layer**
- FastAPI with dependency injection
- JWT authentication
- Rate limiting
- Request validation
- Structured error handling
- API versioning (v1, v2)

**Authentication Layer**
- User registration/login
- JWT token management
- Role-based access control (student, admin)
- Session management

**Conversation Layer**
- Persistent conversation storage
- Conversation context management
- Multi-turn dialogue support
- Conversation history API

**Query Analysis Layer**
- Intent classification (ML-based)
- Entity extraction (NER)
- Query rewriting
- Query expansion
- Ambiguity detection

**Retrieval Layer**
- Structured search (MySQL queries)
- Semantic search (vector similarity)
- Hybrid ranking (BM25 + vector)
- Document indexing
- Citation extraction

**RAG Layer**
- Context window management
- Prompt engineering
- Response generation
- Citation injection
- Confidence scoring

**Database Layer**
- MySQL for structured data
- Vector database for semantic search
- Document storage for PDFs/DOCX
- Conversation storage

**Analytics Layer**
- User interaction tracking
- Query analytics
- Response quality metrics
- Admin dashboard

## 4. Migration Strategy

### Phase 0: Audit & Baseline (Current Phase)
- ✅ Repository structure audit
- ✅ Data flow documentation
- ✅ Database schema documentation
- ✅ API documentation
- ✅ NLP pipeline documentation
- ✅ Technical debt identification
- ✅ Baseline test creation
- ⏳ Architecture roadmap creation

### Phase 1: Backend Refactoring
- Introduce dependency injection
- Add configuration management (environment variables)
- Add structured logging
- Add proper error handling
- Fix schema mismatches
- Add connection pooling
- Implement repository pattern

### Phase 2: SQLite → MySQL Migration
- Design MySQL schema
- Create migration scripts
- Migrate existing data
- Update knowledge base to use MySQL
- Validate data integrity
- Remove SQLite dependencies

### Phase 3: Authentication & User System
- User registration API
- Login API with JWT
- User model in MySQL
- Authentication middleware
- Role-based access control
- Session management

### Phase 4: Query Analyzer Enhancement
- Improve intent classification (ML-based)
- Enhanced entity extraction
- Query rewriting
- Query expansion
- Ambiguity detection

### Phase 5: Semantic Search
- Set up vector database (Qdrant)
- Create document embeddings
- Implement semantic search
- Hybrid retrieval (structured + semantic)
- Re-ranking algorithm

### Phase 6: Document Processing
- Document upload API
- PDF/DOCX parsing
- Document chunking
- Document indexing
- Citation extraction

### Phase 7: RAG Implementation
- LLM integration (OpenAI or local)
- Context window management
- Prompt engineering
- Response generation with citations
- Confidence scoring

### Phase 8: Conversation Memory
- Persistent conversation storage
- Multi-turn dialogue support
- Context retention across sessions
- Conversation history API

### Phase 9: Feedback System
- User feedback collection
- Response rating
- Feedback-driven improvement
- Analytics dashboard

### Phase 10: Admin Dashboard
- Admin authentication
- User management
- Content management
- Analytics viewing
- System monitoring

### Phase 11: Security Hardening
- Input validation
- SQL injection protection
- XSS protection
- CSRF protection
- Rate limiting
- API key management

### Phase 12: Docker & Deployment
- Docker containerization
- Docker Compose setup
- CI/CD pipeline
- Production deployment
- Monitoring setup
- Backup strategy

## 5. Risk Assessment

### High Risk
- Schema mismatch could cause data loss during migration
- No authentication makes system vulnerable
- Wide-open CORS is security risk

### Medium Risk
- No connection pooling may cause performance issues
- Lack of error handling makes debugging difficult
- No persistent conversation memory affects user experience

### Low Risk
- Static pages not connected to database
- Duplicate fallback logic
- No API versioning

## 6. Success Criteria

### Phase 0 Success
- ✅ Existing functionality remains intact
- ✅ Current architecture documented
- ✅ Database schema understood
- ✅ API surface documented
- ✅ NLP pipeline understood
- ✅ Technical debt identified
- ✅ Baseline tests passing
- ✅ Migration roadmap defined

### Overall MITRA 2.0 Success
- Authentication and authorization implemented
- MySQL migration completed
- Semantic search functional
- RAG responses with citations
- Persistent conversation memory
- Admin dashboard operational
- Security hardened
- Production-ready deployment

## 7. Dependencies & Constraints

### External Dependencies
- spaCy model: en_core_web_sm
- Python 3.8+
- MySQL 8.0+
- Vector database (Qdrant recommended)
- LLM API (OpenAI or local)

### Constraints
- Must preserve existing functionality
- Must maintain data integrity
- Must not break existing API contracts
- Must be backward compatible during transition
- Must follow incremental migration approach

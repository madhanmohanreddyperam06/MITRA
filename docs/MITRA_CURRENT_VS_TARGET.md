# MITRA Current vs Target Architecture

## Component Comparison

| Component | Current (v1.0) | Target (v2.0) | Migration Priority |
|-----------|---------------|--------------|-------------------|
| **Frontend** | Streamlit only | Streamlit + optional React UI | Low |
| **API Framework** | FastAPI 0.104.1 | FastAPI (latest) + dependency injection | High |
| **Database** | SQLite | MySQL 8.0+ | High |
| **ORM** | None (raw sqlite3) | SQLAlchemy 2.x | High |
| **Authentication** | None | JWT + User Management | Critical |
| **Authorization** | None | Role-based (Student, Admin) | Critical |
| **Users** | None/current | Registered users with profiles | Critical |
| **Admin** | None | Admin dashboard | Medium |
| **NLP** | Rule-based + spaCy NER | Query Analyzer + ML-based intent + Enhanced NER | Medium |
| **Intent Recognition** | Keyword matching | ML-based classification | Medium |
| **Entity Extraction** | spaCy + custom rules | Enhanced spaCy + custom entities | Medium |
| **Search** | SQL/LIKE | Hybrid (Structured + Semantic) | High |
| **Vector Search** | None | Vector Database (Qdrant) | High |
| **Documents** | None/limited | PDF/DOCX upload & processing | Medium |
| **RAG** | None | RAG Engine with LLM | High |
| **LLM** | None | OpenAI API or Local LLM | High |
| **Sources/Citations** | None | Citation extraction & display | High |
| **Memory** | Session-based only | Persistent conversation memory | Medium |
| **Feedback** | None | User feedback & rating system | Low |
| **Analytics** | None | Admin analytics dashboard | Low |
| **Configuration** | Hardcoded in code | Environment variables + .env | High |
| **Logging** | None | Structured logging (Python logging) | High |
| **Error Handling** | Generic try/catch | Structured error responses | High |
| **Connection Pooling** | None | SQLAlchemy connection pool | High |
| **Testing** | None | Pytest test suite | High |
| **CI/CD** | None | GitHub Actions or similar | Medium |
| **API Versioning** | None (v1.0.0) | Versioned API (v1, v2) | Medium |
| **Rate Limiting** | None | Request rate limiting | Medium |
| **Documentation** | Basic README | Comprehensive API docs + Swagger | Medium |
| **Docker** | None | Docker containerization | Low |
| **Deployment** | Manual | Automated deployment pipeline | Low |

## Detailed Comparison

### Frontend

**Current:**
- Single Streamlit application
- Chat interface with basic features
- Static pages for Admissions, Courses, Facilities
- Session state for conversation history
- Quick action buttons
- Chat download functionality

**Target:**
- Enhanced Streamlit UI with better UX
- Optional React web interface for broader access
- Citation display in responses
- Document upload interface
- User profile management
- Enhanced chat interface with message history
- Real-time typing indicators
- Rich text formatting support

### Backend API

**Current:**
- FastAPI 0.104.1
- Global initialization (no DI)
- No authentication
- No rate limiting
- Generic error handling
- CORS wide open (all origins)
- No API versioning
- Direct SQLite access

**Target:**
- FastAPI (latest) with dependency injection
- JWT authentication middleware
- Rate limiting middleware
- Structured error responses
- Configured CORS for specific origins
- API versioning (v1, v2)
- SQLAlchemy ORM with connection pooling
- Request validation
- Response caching

### Database

**Current:**
- SQLite
- 5 tables: admissions, courses, facilities, contact_info, qa_dataset
- Schema mismatch between code and actual database
- No foreign keys
- No indexes
- No constraints beyond NOT NULL
- Direct sqlite3 access
- No migrations

**Target:**
- MySQL 8.0+
- Enhanced schema with proper relationships
- Foreign keys with cascading deletes
- Indexed columns for performance
- Constraints (UNIQUE, CHECK)
- SQLAlchemy ORM
- Alembic migrations
- Connection pooling
- Transaction management

### Authentication & Authorization

**Current:**
- None
- All endpoints public
- No user concept
- No roles

**Target:**
- JWT-based authentication
- User registration and login
- Password hashing (bcrypt)
- Role-based access control (Student, Admin)
- Protected endpoints
- Token refresh mechanism
- Session management

### NLP Pipeline

**Current:**
- spaCy en_core_web_sm model
- Rule-based intent recognition (keyword matching)
- Custom entity extraction (COURSE, DEPARTMENT)
- Basic text preprocessing
- Confidence scoring based on pattern matches
- No query rewriting
- No query expansion

**Target:**
- Enhanced spaCy model or custom ML model
- ML-based intent classification (scikit-learn or transformers)
- Improved entity extraction
- Advanced preprocessing (lemmatization, stopword removal)
- Better confidence scoring
- Query rewriting for better matching
- Query expansion with synonyms
- Ambiguity detection and clarification

### Search & Retrieval

**Current:**
- SQL LIKE queries
- Full-text search not implemented
- No ranking
- No relevance scoring
- Search across all tables sequentially

**Target:**
- Hybrid retrieval:
  - Structured search (MySQL full-text search)
  - Semantic search (vector similarity)
  - Document search (chunked documents)
- Re-ranking algorithm (BM25 + vector)
- Citation extraction
- Relevance scoring
- Query-time result fusion

### Vector Database

**Current:**
- None

**Target:**
- Qdrant or Weaviate
- Vector embeddings for documents
- Semantic similarity search
- Embedding management
- Vector index optimization

### RAG Engine

**Current:**
- None
- Template-based responses
- Hardcoded information for some intents

**Target:**
- LLM integration (OpenAI GPT-4 or local Llama)
- Context window management
- Prompt engineering
- Response generation with citations
- Confidence scoring
- Response validation
- Hallucination detection

### Conversation Memory

**Current:**
- Session-based only (Streamlit session state)
- Lost on page refresh
- Last 5 messages sent as context
- No persistent storage

**Target:**
- Persistent conversation storage in MySQL
- Multi-turn dialogue support
- Context retention across sessions
- Conversation history API
- Conversation summarization
- Context window optimization

### Document Processing

**Current:**
- None
- Static information only

**Target:**
- Document upload API (PDF, DOCX, TXT)
- Document parsing
- Document chunking
- Document indexing
- Embedding generation
- Citation extraction
- Document versioning

### Configuration

**Current:**
- Hardcoded values in code
- config/settings.py exists but not used
- No environment variables
- No .env file

**Target:**
- Environment-based configuration
- .env file for local development
- Pydantic Settings for validation
- Configuration per environment (dev, staging, prod)
- Secret management

### Logging

**Current:**
- None
- Print statements only
- No structured logs
- No log levels

**Target:**
- Python logging module
- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Error tracking
- Log aggregation (ELK stack or similar)

### Error Handling

**Current:**
- Generic try/catch
- HTTPException with basic message
- No error codes
- No structured error responses

**Target:**
- Custom exception classes
- Structured error responses
- Error codes and categories
- Error context (request ID, timestamp)
- Error tracking and monitoring
- User-friendly error messages

### Testing

**Current:**
- None
- No test suite
- No CI/CD

**Target:**
- Pytest test suite
- Unit tests for all components
- Integration tests for API
- E2E tests for critical flows
- Test coverage reporting
- CI/CD pipeline (GitHub Actions)

### Deployment

**Current:**
- Manual deployment
- No containerization
- No automated pipeline

**Target:**
- Docker containerization
- Docker Compose for local development
- Kubernetes for production (optional)
- CI/CD pipeline
- Automated testing
- Blue-green deployment
- Health checks
- Monitoring and alerting

## Migration Complexity Assessment

### Low Complexity (Easy)
- Frontend enhancements
- API versioning
- Documentation
- Docker containerization

### Medium Complexity (Moderate)
- NLP pipeline improvements
- Document processing
- Conversation memory
- Testing infrastructure
- Logging implementation

### High Complexity (Challenging)
- Database migration (SQLite → MySQL)
- Authentication implementation
- Vector database integration
- RAG implementation
- Configuration management refactoring

### Critical Complexity (Risk)
- Schema mismatch resolution
- Data migration and validation
- Breaking API changes
- Security hardening
- Production deployment

## Incremental Migration Path

### Phase 0: Foundation (Current)
- Audit existing system
- Document architecture
- Create baseline tests
- Identify technical debt
- Define migration roadmap

### Phase 1: Backend Refactoring
- Fix schema mismatches
- Implement configuration management
- Add structured logging
- Add proper error handling
- Implement repository pattern
- Add connection pooling

### Phase 2: Database Migration
- Design MySQL schema
- Create migration scripts
- Migrate data
- Validate integrity
- Update ORM layer

### Phase 3: Authentication
- Implement user registration
- Implement JWT authentication
- Add authorization middleware
- Protect endpoints

### Phase 4: NLP Enhancement
- Improve intent classification
- Enhance entity extraction
- Add query rewriting
- Add query expansion

### Phase 5: Semantic Search
- Set up vector database
- Create embeddings
- Implement semantic search
- Implement hybrid retrieval

### Phase 6: Document Processing
- Add document upload
- Implement parsing
- Add chunking
- Index documents

### Phase 7: RAG Implementation
- Integrate LLM
- Implement RAG pipeline
- Add citations
- Add confidence scoring

### Phase 8: Conversation Memory
- Add persistent storage
- Implement conversation history
- Add context management

### Phase 9: Admin & Analytics
- Build admin dashboard
- Add analytics
- Add user management

### Phase 10: Security & Deployment
- Security hardening
- Add rate limiting
- Implement CI/CD
- Docker containerization
- Production deployment

## Backward Compatibility Strategy

### API Compatibility
- Maintain v1 API during transition
- Introduce v2 API with new features
- Deprecate v1 after grace period
- Provide migration guide for API consumers

### Data Compatibility
- Preserve existing data during migration
- Provide data transformation scripts
- Validate data integrity post-migration
- Keep SQLite backup for rollback

### Frontend Compatibility
- Streamlit UI remains functional
- Progressive enhancement approach
- Optional migration to React
- Maintain user experience

## Success Metrics

### Technical Metrics
- Test coverage > 80%
- API response time < 500ms (p95)
- Database query time < 100ms (p95)
- Uptime > 99.5%
- Error rate < 1%

### User Metrics
- User satisfaction > 4/5
- Response relevance > 80%
- Citation accuracy > 90%
- Conversation completion rate > 70%

### Business Metrics
- Cost per query < $0.01
- Support ticket reduction > 30%
- User engagement increase > 50%

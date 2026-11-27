# MITRA

![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![spaCy](https://img.shields.io/badge/spaCy-3.x-09A3D5?style=flat-square&logo=spacy)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

An intelligent LLM for college helpdesk services built with Streamlit frontend and FastAPI backend. MITRA provides instant responses to student queries about admissions, courses, facilities, and more using NLP techniques with spaCy.

## Features

| Category | Feature | Scope & Access | Implementation |
| :--- | :--- | :--- | :--- |
| **Conversational AI** | Helpdesk Chat Engine | Authenticated & Guest users (`POST /chat`) | `NLPPipeline` + `ChatService` + PostgreSQL repositories |
| **Academic Discovery** | Admissions & Courses | Public browsing + Chat intent routing | `1_Admissions.py`, `2_Courses.py`, `admissions` & `courses` tables |
| **Campus & Student Life** | Facilities, Hostel & Library | Interactive tabs + Chart visualizations | `3_Facilities.py`, `facilities` table, curated library data |
| **Financial Planning** | Fees, Scholarships & Cost Calculator | Interactive UG/PG fee calculator & charts | `4_Fees_&_Scholarships.py`, `fee_inquiry` handler |
| **Career Outcomes** | Placements & Recruiter Analytics | KPI metrics, sector charts & multi-year trends | `5_Placements.py`, `placement_info` handler |
| **Campus Directory** | Department & Emergency Contacts | Office directory, campus address & contact form | `6_Contact_Information.py`, `contact_info` table |
| **Knowledge Base** | Dynamic Q&A Management | Authenticated users (`GET /qa`, `POST /qa`) | `QARepository` (`qa_dataset` table) |
| **Security & RBAC** | JWT Auth & Single-Admin Control | Bearer JWT (`HS256`), Bcrypt, DB trigger guard | `AuthService`, `security.py`, `/api/auth/*` & `/api/users/*` |

<details>
<summary><strong>Project Modernization Status & Technology Stack</strong></summary>

#### Modernization Milestones

| Phase | Milestone | Status | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Layered Architecture Refactoring | Complete | Separated API, Security, Service, Repository, Schema, and Core layers |
| **Phase 2** | Relational Database & Migrations | Complete | PostgreSQL 16 + SQLAlchemy 2.0 ORM + 4-step Alembic migration chain |
| **Phase 3** | Authentication & Access Control | Complete | JWT (`HS256`) tokens, Bcrypt hashing, Guest Mode, DB-enforced single-admin model |
| **UI Upgrade** | Multi-Page Analytics Frontend | Complete | Dark-themed Streamlit UI with Chat Hub + 6 multi-tab Plotly dashboards |
| **Quality** | Automated Test Suite | Complete | 97 Pytest test cases across unit (`52`) and integration (`45`) suites |

#### Technology Stack

| Layer | Technology | Role in MITRA | Source / Package |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | Streamlit (`>=1.28.0`) | Multi-page app, auth flow, guest mode, chat UI | `frontend/requirements.txt` |
| **Visualizations** | Plotly (`>=5.18.0`) & Pandas | 29 interactive charts & interactive data tables | `frontend/requirements.txt` |
| **Backend API** | FastAPI (`>=0.115.0`) & Uvicorn | Async REST endpoints, OpenAPI docs, middleware | `backend/requirements.txt` |
| **Validation** | Pydantic v2 & `pydantic-settings` | Request/response schemas & `.env` configuration | `backend/app/schemas/` |
| **NLP Engine** | Rule-Based Pipeline (`re`) | Text normalization, 8-intent scoring, entity matching | `backend/app/nlp_pipeline.py` |
| **Database & ORM** | PostgreSQL 16 & SQLAlchemy (`>=2.0.25`) | Connection pooling (`10 + 20`), ORM models, repositories | `backend/app/database/` |
| **Migrations** | Alembic (`>=1.12.0`) & `psycopg2-binary` | Versioned DDL migrations & PL/pgSQL admin trigger | `backend/alembic/` |
| **Security** | `python-jose` (JWT) & `passlib[bcrypt]` | Stateless Bearer auth, Bcrypt password hashing | `backend/app/core/security.py` |
| **Testing** | Pytest & `httpx` | Unit & FastAPI `TestClient` integration tests | `tests/`, `pytest.ini` |

</details>

---

## Architecture Overview

MITRA follows a strict **layered architecture** that isolates presentation, HTTP routing, authentication, NLP business logic, and relational persistence.

```mermaid
flowchart TB
    subgraph FE["Presentation Layer (Streamlit)"]
        AUTH_UI["Landing, Login, Register & Guest Flow\n(frontend/components/auth.py)"]
        CHAT_UI["Interactive Chat Interface & Sidebar\n(chat_interface.py, sidebar.py)"]
        PAGES["6 Multi-Page Dashboards\n(25 Tabs, 29 Plotly Charts)"]
    end

    subgraph API["API & Security Layer (FastAPI)"]
        MW["CORS & Request Timing Middleware\nGlobal Exception Handlers"]
        ROUTERS["API Routers\n(/health, /chat, /intents, /qa, /api/auth, /api/users)"]
        SEC["JWT Bearer & Admin Guards\n(app/core/security.py)"]
    end

    subgraph BIZ["Intelligence & Service Layer"]
        NLP["NLPPipeline\n(8 Intents, COURSE & DEPARTMENT Entities)"]
        CSVC["ChatService\n(Intent Routing & Cross-Table Search)"]
        ASVC["AuthService\n(Bcrypt Hashing & JWT Lifecycle)"]
    end

    subgraph DATA["Data Access & Persistence Layer"]
        REPOS["6 SQLAlchemy Repositories\n(Admission, Course, Facility, Contact, QA, User)"]
        DB[("PostgreSQL 16\nAlembic Schema + Single-Admin Trigger")]
    end

    AUTH_UI --> ROUTERS
    CHAT_UI --> ROUTERS
    PAGES -. "Interactive Data & Charts" .-> CHAT_UI
    MW --> ROUTERS
    ROUTERS --> SEC
    ROUTERS --> NLP
    NLP --> CSVC
    SEC --> ASVC
    CSVC --> REPOS
    ASVC --> REPOS
    REPOS --> DB
```

---

## NLP Pipeline & Intent Classification

User queries pass through `NLPPipeline` (`backend/app/nlp_pipeline.py`) for normalization, pattern-based intent scoring, college entity extraction, and confidence estimation before `ChatService` (`backend/app/services/chat_service.py`) queries the corresponding repository or institutional handler.

> [!NOTE]
> `NLPPipeline` currently operates as a zero-download rule-based matcher (`self.nlp = None`) with `SPACY_MODEL` and `CONFIDENCE_THRESHOLD` retained in `backend/app/core/config.py` for configuration compatibility and future NLP/LLM extensions.

```mermaid
flowchart LR
    Q["User Input"] --> C["1. Text Cleaning\n(Lowercase, strip, regex)"]
    C --> I["2. Intent Scoring\n(Exact match +2, substring +1)"]
    C --> E["3. Entity Extraction\n(COURSE & DEPARTMENT)"]
    I --> CONF["4. Confidence Heuristic\n(0.5 fallback, up to 0.9)"]
    E --> R["5. ChatService Routing\n(Intent + Entity Filter)"]
    CONF --> R
    R --> RES["6. ChatResponse\n(response, intent, confidence, entities)"]
```

### Intent Classification Matrix

| Intent ID | Matched Keywords / Patterns | Keywords | Data Source / Handler | Example Query |
| :--- | :--- | :---: | :--- | :--- |
| `admission_info` | `admission`, `apply`, `application`, `eligibility`, `entrance`, `how to apply`, `admission process`, `requirements` | 8 | `AdmissionRepository` (`admissions`) | *"What is the admission process and eligibility?"* |
| `course_info` | `course`, `program`, `syllabus`, `curriculum`, `degree`, `engineering`, `science`, `commerce`, `subjects` | 9 | `CourseRepository` (`courses`, filtered by `DEPARTMENT`) | *"Show computer science engineering courses"* |
| `fee_inquiry` | `fee`, `cost`, `tuition`, `payment`, `scholarship`, `how much`, `price`, `charges`, `financial` | 9 | `ChatService._handle_fee_query` | *"What is the tuition fee and scholarship info?"* |
| `hostel_info` | `hostel`, `accommodation`, `room`, `boarding`, `residence`, `stay`, `facilities`, `mess` | 8 | `FacilityRepository` (`category="Accommodation"`) | *"Tell me about hostel rooms and mess"* |
| `library_info` | `library`, `book`, `study`, `reading`, `resources`, `digital`, `journal`, `database` | 8 | `ChatService._handle_library_query` | *"What are the library timings and digital books?"* |
| `placement_info` | `placement`, `job`, `career`, `internship`, `recruitment`, `companies`, `salary`, `campus hiring` | 8 | `ChatService._handle_placement_query` | *"What is the average placement salary?"* |
| `contact_info` | `contact`, `phone`, `email`, `address`, `location`, `office`, `department`, `reach` | 8 | `ContactRepository` (`contact_info`) | *"How can I contact the admissions office?"* |
| `general_info` | `about`, `college`, `university`, `campus`, `facilities`, `history`, `achievements` | 7 | Cross-repo search (`admissions`, `courses`, `facilities`, `contact_info`, `qa_dataset`) | *"Tell me about college campus achievements"* |

### Entity Extraction & Keyword Distribution

| Entity Label | Description | Recognized Tokens | Count |
| :--- | :--- | :--- | :---: |
| `COURSE` | Academic course or program | `engineering`, `science`, `commerce`, `bba`, `mba`, `btech`, `mtech` | 7 |
| `DEPARTMENT` | Academic department (filters `CourseRepository`) | `computer science`, `electronics`, `mechanical`, `civil`, `physics`, `chemistry` | 6 |

```mermaid
xychart-beta
    title "NLP Intent Keyword Coverage by Domain"
    x-axis ["Admissions", "Courses", "Fees", "Hostel", "Library", "Placements", "Contacts", "General"]
    y-axis "Matched Patterns" 0 --> 12
    bar [8, 9, 9, 8, 8, 8, 8, 7]
```

<details>
<summary><strong>Interactive Sequence Diagram: Authenticated &amp; Guest Chat Request Lifecycle</strong></summary>

```mermaid
sequenceDiagram
    actor User as Student / Guest
    participant UI as Streamlit ChatInterface
    participant API as FastAPI POST /chat
    participant SEC as get_optional_current_user
    participant NLP as NLPPipeline
    participant SVC as ChatService
    participant DB as PostgreSQL 16

    User->>UI: Submits query in chat input
    UI->>API: POST /chat (optional Bearer JWT, last 5 messages)
    API->>SEC: Validate token if header present
    SEC-->>API: User dict or None (guest mode)
    API->>NLP: process(user_input)
    NLP-->>API: intent, entities, confidence
    API->>SVC: process_query(intent, entities, user_input, ...)
    SVC->>DB: Query domain repository / cross-table search
    DB-->>SVC: Structured records
    SVC-->>API: Formatted Markdown response
    API-->>UI: ChatResponse (200 OK)
    UI-->>User: Renders assistant message
```

</details>

---

## Frontend Multi-Page Dashboard

Beyond the conversational hub (`frontend/main.py`), MITRA includes **6 dedicated Streamlit pages** featuring **25 interactive tabs** and **29 Plotly visualizations** styled with a unified dark theme (`frontend/components/theme.py`).

| Module | File | Tabs | Plotly Charts | Interactive Highlights |
| :--- | :--- | :---: | :---: | :--- |
| **Chat Hub & Auth** | `frontend/main.py` | — | — | Landing/Login/Register/Guest gate, chat history export (`.txt`), role-based sidebar |
| **Admissions** | `frontend/pages/1_Admissions.py` | 4 | 3 | `Overview`, `Programs`, `Timeline`, `Documents` — bar/pie stats, Gantt timeline, checklist |
| **Courses** | `frontend/pages/2_Courses.py` | 4 | 3 | `Overview`, `Undergraduate`, `Postgraduate`, `Specializations` — seat & elective distribution |
| **Facilities** | `frontend/pages/3_Facilities.py` | 5 | 7 | `Overview`, `Library`, `Hostels`, `Sports`, `Labs` — capacity, campus area, lab & hostel charts |
| **Fees & Scholarships** | `frontend/pages/4_Fees_&_Scholarships.py` | 4 | 5 | `Fee Structure`, `Scholarships`, `Payment`, `Cost Calculator` — interactive total cost estimator |
| **Placements** | `frontend/pages/5_Placements.py` | 4 | 11 | `Statistics`, `Top Recruiters`, `Training`, `Year-wise Trends` — 4 KPI metrics & package charts |
| **Contact Directory** | `frontend/pages/6_Contact_Information.py` | 4 | 0 | `Administration`, `Departments`, `Student Services`, `Emergency` — directory & quick form |

```mermaid
xychart-beta
    title "Interactive Plotly Charts per Streamlit Page (29 Total)"
    x-axis ["Admissions", "Courses", "Facilities", "Fees", "Placements", "Contacts"]
    y-axis "Plotly Charts" 0 --> 12
    bar [3, 3, 7, 5, 11, 0]
```

---

## Database Schema & Migrations

MITRA uses **PostgreSQL 16** managed through **SQLAlchemy 2.0** (`backend/app/database/models.py`) and **Alembic** (`backend/alembic/versions/`).

> [!IMPORTANT]
> Migration `003_add_single_admin_constraint` installs PL/pgSQL triggers (`prevent_multiple_admins_insert` and `prevent_multiple_admins_update`) directly on the `users` table to enforce a **single-administrator invariant** at the database level.

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        string full_name
        boolean is_active
        boolean is_admin
        datetime created_at
        datetime updated_at
        datetime last_login_at
    }
    ADMISSIONS {
        int id PK
        string category
        string information
        text details
    }
    COURSES {
        int id PK
        string course_name
        string department
        string duration
        string eligibility
        text description
    }
    FACILITIES {
        int id PK
        string facility_name
        string category
        text description
        string location
        string timings
    }
    CONTACT_INFO {
        int id PK
        string department
        string contact_person
        string phone
        string email
        string office_location
    }
    QA_DATASET {
        int id PK
        string question
        text answer
    }
```

### Relational Tables & Indexes

| Table | ORM Model | Key Columns | Indexed Columns | Repository |
| :--- | :--- | :--- | :--- | :--- |
| `admissions` | `Admission` | `id`, `category`, `information`, `details` | `category` | `AdmissionRepository` |
| `courses` | `Course` | `id`, `course_name`, `department`, `duration`, `eligibility`, `description` | `course_name`, `department` | `CourseRepository` |
| `facilities` | `Facility` | `id`, `facility_name`, `category`, `description`, `location`, `timings` | `facility_name`, `category` | `FacilityRepository` |
| `contact_info` | `ContactInfo` | `id`, `department`, `contact_person`, `phone`, `email`, `office_location` | `department` | `ContactRepository` |
| `qa_dataset` | `QADataset` | `id`, `question` (`NOT NULL`), `answer` (`NOT NULL`) | `question` | `QARepository` |
| `users` | `User` | `id`, `username`, `email`, `password_hash`, `is_active`, `is_admin`, timestamps | `username` (`UNIQUE`), `email` (`UNIQUE`), `is_admin`, `is_active` | `UserRepository` |

### Alembic Migration Chain

```mermaid
flowchart LR
    R1["001_initial_schema\n(5 Knowledge Tables)"] --> R2["002_add_users_table\n(Users Table + Unique Indexes)"]
    R2 --> R3["003_add_single_admin_constraint\n(PL/pgSQL Admin Triggers)"]
    R3 --> R4["8bc28335b2c5 (head)\n(is_admin & is_active Indexes)"]
```

<details>
<summary><strong>Alembic CLI Commands Reference</strong></summary>

Run all migration commands from the `backend/` directory:

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Apply Migrations** | `alembic upgrade head` | Bring schema up to revision `8bc28335b2c5` |
| **Create Migration** | `alembic revision --autogenerate -m "description"` | Generate migration diff from SQLAlchemy models |
| **Check Current Rev** | `alembic current` | Print active database revision |
| **View History** | `alembic history` | Inspect full revision chain |
| **Rollback One Step** | `alembic downgrade -1` | Revert the latest migration |

For complete migration history and SQLite/MySQL transition notes, see [docs/DATABASE_MIGRATION.md](docs/DATABASE_MIGRATION.md).

</details>

---

## API Reference

Interactive Swagger UI and ReDoc specifications are served automatically when the backend is running at `http://localhost:8000/docs` and `http://localhost:8000/redoc`.

### Endpoint Classification

| Group | Method & Path | Access Level | Router | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Health** | `GET /` | Public | `health.py` | Root API status welcome message |
| **Health** | `GET /health` | Public | `health.py` | Service health check (`status`, `service`) |
| **Chat** | `POST /chat` | Public / Optional JWT | `chat.py` | Process student query; supports authenticated & guest users |
| **Intents** | `GET /intents` | Public | `intents.py` | Return list of all 8 supported NLP intent identifiers |
| **Knowledge** | `POST /qa` | Authenticated (Active User) | `knowledge.py` | Insert a new Q&A pair (`question`, `answer`) into `qa_dataset` |
| **Knowledge** | `GET /qa` | Authenticated (Active User) | `knowledge.py` | Retrieve all Q&A pairs or filter via `?question=` |
| **Auth** | `POST /api/auth/register` | Public | `auth.py` | Register a standard user account (`201 Created`) |
| **Auth** | `POST /api/auth/login` | Public | `auth.py` | Authenticate via username/email + password and issue Bearer JWT |
| **Auth** | `GET /api/auth/me` | Authenticated | `auth.py` | Return the authenticated user's profile |
| **Auth** | `GET /api/auth/debug/admin-check` | Public (Diagnostic) | `auth.py` | Inspect administrator existence, active status, and count |
| **Admin** | `GET /api/users` | Admin Only | `auth.py` | List all registered user accounts |
| **Admin** | `GET /api/users/{user_id}` | Admin Only | `auth.py` | Retrieve a specific user profile by ID |
| **Admin** | `PATCH /api/users/{user_id}/status` | Admin Only | `auth.py` | Activate or deactivate a user (blocks deactivating sole admin) |
| **Admin** | `DELETE /api/users/{user_id}` | Admin Only | `auth.py` | Delete a user account (blocks deleting sole admin) |

<details>
<summary><strong>Request &amp; Response Payload Schemas</strong></summary>

#### Chat (`POST /chat`)
```json
// Request (user_input: 1-1000 chars, conversation_history: max 20 entries)
{
  "user_input": "What BTech courses are in computer science?",
  "user_context": {},
  "conversation_history": []
}

// Response
{
  "response": "Here are the course details: ...",
  "intent": "course_info",
  "confidence": 0.52,
  "entities": [
    {"text": "btech", "label": "COURSE", "description": "Academic course or program"},
    {"text": "computer science", "label": "DEPARTMENT", "description": "Academic department"}
  ]
}
```

#### Authentication (`POST /api/auth/register` &amp; `POST /api/auth/login`)
```json
// POST /api/auth/register (username: 3-50 alphanumeric/underscore, password: 8-72 chars)
{
  "username": "student01",
  "email": "student01@college.edu",
  "password": "securepassword123",
  "full_name": "Student Name"
}

// POST /api/auth/login
{
  "username_or_email": "student01",
  "password": "securepassword123"
}

// Login Response
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

#### Knowledge Base (`POST /qa`) &amp; Admin Status (`PATCH /api/users/{user_id}/status`)
```json
// POST /qa (Bearer Token Required; question: 1-500 chars, answer: 1-2000 chars)
{
  "question": "When do semester exams begin?",
  "answer": "Semester examinations typically start in November and April."
}

// PATCH /api/users/{user_id}/status (Admin Bearer Token Required)
{
  "is_active": false
}
```

</details>

---

## Getting Started

### Prerequisites

| Requirement | Specification | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.8+ | Runtime for FastAPI backend and Streamlit frontend |
| **PostgreSQL** | Local or Managed (v16 recommended) | Primary relational database |
| **pip** | Latest recommended | Dependency installation (`requirements.txt` &amp; `frontend/requirements.txt`) |

### Installation & Setup

1. **Clone the repository and create a virtual environment:**

   ```bash
   git clone https://github.com/madhanmohanreddyperam06/MITRA.git
   cd MITRA
   python -m venv venv
   ```

   Activate the virtual environment:

   | Shell / OS | Activation Command |
   | :--- | :--- |
   | **Windows (PowerShell)** | `.\venv\Scripts\activate` |
   | **Windows (CMD)** | `venv\Scripts\activate.bat` |
   | **Linux / macOS** | `source venv/bin/activate` |

2. **Install backend and frontend dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r frontend/requirements.txt
   ```

3. **Create the PostgreSQL database and apply Alembic migrations:**

   ```sql
   CREATE DATABASE mitra_db;
   CREATE USER mitra_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE mitra_db TO mitra_user;
   ```

   Configure `backend/.env` (see Configuration Matrix below), then run migrations:

   ```bash
   cd backend
   alembic upgrade head
   cd ..
   ```

4. **Bootstrap the single administrator account (optional for admin endpoints):**

   ```bash
   cd backend
   python scripts/create_admin.py
   cd ..
   ```

### Configuration Matrix

Settings are loaded via Pydantic (`backend/app/core/config.py`) from `backend/.env` or environment variables:

| Category | Variable | Default | Description |
| :--- | :--- | :--- | :--- |
| **App** | `APP_NAME` | `"MITRA - College Helpdesk Assistant"` | FastAPI application title |
| **App** | `APP_ENV` | `"development"` | Environment mode (`development` / `production`) |
| **App** | `DEBUG` | `True` | Enables debug mode and Uvicorn auto-reload |
| **App** | `LOG_LEVEL` | `"INFO"` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| **API** | `API_HOST` | `"127.0.0.1"` | Backend bind address (`0.0.0.0` in containers/cloud) |
| **API** | `API_PORT` | `8000` | Backend HTTP port |
| **API** | `CORS_ALLOWED_ORIGINS` | `"http://localhost:8501"` | Comma-separated allowed frontend origins |
| **Database** | `DATABASE_URL` | `postgresql://mitra_user:password@localhost:5432/mitra_db` | PostgreSQL connection string (`psycopg2` applied automatically) |
| **Security** | `JWT_SECRET_KEY` | `"dev-secret-change-in-production"` | JWT signing secret (must be randomized when `APP_ENV=production`) |
| **Security** | `JWT_ALGORITHM` | `"HS256"` | JWT signing algorithm |
| **Security** | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime in minutes |
| **NLP & Chat** | `SPACY_MODEL` | `"en_core_web_sm"` | Configured spaCy model identifier |
| **NLP & Chat** | `CONFIDENCE_THRESHOLD` | `0.5` | Minimum confidence before logging low-confidence warnings |
| **NLP & Chat** | `MAX_CONVERSATION_HISTORY` | `10` | Chat history limit setting |
| **NLP & Chat** | `CHAT_TIMEOUT` | `30` | Chat request timeout in seconds |
| **Frontend** | `BACKEND_URL` | `"http://localhost:8000"` | Target FastAPI base URL read by Streamlit components |

<details>
<summary><strong>Example <code>backend/.env</code> &amp; Utility Scripts Reference (8 Scripts)</strong></summary>

#### Sample `backend/.env` for Local Development

```env
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

API_HOST=127.0.0.1
API_PORT=8000
CORS_ALLOWED_ORIGINS=http://localhost:8501

DATABASE_URL=postgresql://mitra_user:password@localhost:5432/mitra_db

# Generate production key: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET_KEY=dev-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SPACY_MODEL=en_core_web_sm
CONFIDENCE_THRESHOLD=0.5
MAX_CONVERSATION_HISTORY=10
CHAT_TIMEOUT=30
```

#### Backend Utility & Admin Scripts (`backend/scripts/`)

| Script | Purpose |
| :--- | :--- |
| `create_admin.py` | Interactive CLI to bootstrap the single initial administrator account |
| `create_admin_env.py` | Non-interactive admin creation via `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_FULL_NAME` |
| `check_admin.py` | Verify whether an administrator record exists in the database |
| `recreate_admin.py` | Remove and recreate the administrator account with updated credentials |
| `reset_admin_password.py` | Update the existing administrator's bcrypt password hash |
| `test_login.py` | Direct database & bcrypt authentication verification helper |
| `test_token.py` | Standalone JWT encoding/decoding sanity check |
| `validate_database.py` | Read-only validation of schema, constraints, indexes, and admin state |

</details>

### Running the Application

Run both services in separate terminals with your virtual environment activated:

| Service | Working Directory | Launch Command | Local Endpoint |
| :--- | :--- | :--- | :--- |
| **Backend API** | `backend/` | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload` | `http://localhost:8000` (`/docs`) |
| **Frontend UI** | `frontend/` | `python -m streamlit run main.py` | `http://localhost:8501` |

> [!TIP]
> If the backend is offline, Streamlit's `ChatInterface` automatically switches to an offline keyword fallback mode so the UI remains responsive while displaying a connection warning on authentication actions.

---

## Testing & Quality Assurance

The repository contains **97 automated tests** organized under `tests/` (`52` unit tests and `45` integration tests).

```mermaid
xychart-beta
    title "Automated Test Distribution by Module (97 Total)"
    x-axis ["Auth Int", "Auth Unit", "MySQL Int", "API Int", "DB Unit", "Repo", "RespGen", "UI Auth", "NLP", "Config"]
    y-axis "Test Functions" 0 --> 32
    bar [28, 23, 9, 8, 7, 5, 5, 5, 4, 3]
```

### Test Suite Classification

| Category | Test File | Tests | Scope Covered |
| :--- | :--- | :---: | :--- |
| **Integration** | `tests/integration/test_auth.py` | 28 | Registration, login, `/api/auth/me`, token expiry, admin user management |
| **Integration** | `tests/integration/test_mysql_integration.py` | 9 | Database compatibility & integration marker suite (`@pytest.mark.mysql`) |
| **Integration** | `tests/integration/test_api.py` | 8 | FastAPI `/health`, `/intents`, `/chat`, and `/qa` endpoint contracts |
| **Unit** | `tests/unit/test_auth.py` | 23 | `AuthService` password hashing, JWT creation/decoding, validation rules |
| **Unit** | `tests/unit/test_database.py` | 7 | Knowledge base operations & database unit verification |
| **Unit** | `tests/unit/test_repositories.py` | 5 | SQLAlchemy repository CRUD & query methods |
| **Unit** | `tests/unit/test_response_generator.py` | 5 | Intent-based template & fallback response formatting |
| **Unit** | `tests/unit/test_streamlit_auth.py` | 5 | Streamlit `AuthComponent` login/register/logout state handling |
| **Unit** | `tests/unit/test_nlp.py` | 4 | Intent detection, entity extraction, and confidence calculation |
| **Unit** | `tests/unit/test_config.py` | 3 | Pydantic `Settings` loading & configuration defaults |

### Running Tests

| Goal | `pytest` Command | Convenience Runner (`tests/run_all_tests.py`) |
| :--- | :--- | :--- |
| **Run All Tests** | `python -m pytest tests/ -v` | `python tests/run_all_tests.py` |
| **Unit Tests Only** | `python -m pytest tests/ -m unit -v` | `python tests/run_all_tests.py --unit` |
| **Integration Tests Only** | `python -m pytest tests/ -m integration -v` | `python tests/run_all_tests.py --integration` |
| **DB-Specific Tests** | `python -m pytest tests/ -m mysql -v` | `python tests/run_all_tests.py --mysql` |
| **Coverage Report** | `python -m pytest tests/ --cov=backend/app --cov-report=html` | `python tests/run_all_tests.py --cov` |

See [tests/README.md](tests/README.md) for fixture details and environment setup.

---

## Deployment & Project Structure

### Cloud Deployment (`render.yaml`)

MITRA ships with a ready-to-use Render Blueprint ([`render.yaml`](render.yaml)) defining 3 managed resources:

| Render Service | Type | Build Command | Start Command | Key Environment Variables |
| :--- | :--- | :--- | :--- | :--- |
| `mitra-backend` | Web Service | `pip install -r requirements.txt` | `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` | `DATABASE_URL`, `JWT_SECRET_KEY`, `APP_ENV=production`, `DEBUG=false`, `CORS_ALLOWED_ORIGINS` |
| `mitra-frontend` | Web Service | `cd frontend && pip install -r requirements.txt` | `cd frontend && streamlit run main.py --server.port=$PORT --server.address=0.0.0.0` | `BACKEND_URL` |
| `mitra-db` | PostgreSQL | Managed | Managed | `databaseName: mitra_db`, `user: mitra_user` |

<details>
<summary><strong>Render Post-Deploy Checklist &amp; Documentation Index</strong></summary>

1. Provision PostgreSQL (`mitra-db`), Backend (`mitra-backend`), and Frontend (`mitra-frontend`) via [`render.yaml`](render.yaml).
2. Open the backend **Render Shell** and apply migrations: `cd backend && alembic upgrade head`.
3. Bootstrap the single administrator using `backend/scripts/create_admin_env.py` with `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `ADMIN_FULL_NAME`.
4. Verify `/health` and `/api/auth/login`, and update `CORS_ALLOWED_ORIGINS` to match the live frontend origin.

#### Project Documentation Index

| Document | Topic |
| :--- | :--- |
| [docs/MITRA_BACKEND_ARCHITECTURE.md](docs/MITRA_BACKEND_ARCHITECTURE.md) | Layered architecture, middleware, error handling, and schemas |
| [docs/MITRA_AUTHENTICATION.md](docs/MITRA_AUTHENTICATION.md) | JWT specification, Bcrypt policy, and RBAC rules |
| [docs/DATABASE_MIGRATION.md](docs/DATABASE_MIGRATION.md) | Alembic schema migration & data validation guide |
| [docs/RENDER_POSTGRESQL_DEPLOYMENT.md](docs/RENDER_POSTGRESQL_DEPLOYMENT.md) | Full Render + PostgreSQL production deployment walkthrough |
| [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Detailed repository module map |
| [tests/README.md](tests/README.md) | Pytest markers, fixtures, and CI test execution |

</details>

### Repository Overview

| Directory / File | Purpose |
| :--- | :--- |
| `frontend/` | Streamlit multi-page UI, dark theme, auth/guest flow, and Plotly analytics |
| `backend/app/` | FastAPI routers, core config/security, SQLAlchemy models, repositories, services, and `nlp_pipeline.py` |
| `backend/alembic/` | Alembic migration environment and 4 versioned PostgreSQL migrations |
| `backend/scripts/` | 8 CLI utilities for admin lifecycle management, auth checks, and DB validation |
| `data/knowledge_base/` | JSON knowledge base reference files (`admission_data.json`, `course_catalog.json`) |
| `tests/` | Pytest configuration, fixtures, 52 unit tests, and 45 integration tests |
| `docs/` | Architecture, authentication, migration, code review, and cloud deployment guides |
| `render.yaml` | Multi-service Render infrastructure-as-code blueprint |

<details>
<summary><strong>Full Repository Directory Tree</strong></summary>

```text
MITRA/
├── frontend/
│   ├── main.py                              # Main Streamlit entry point & chat dashboard
│   ├── requirements.txt                     # Frontend dependencies (streamlit, plotly, pandas, requests)
│   ├── components/
│   │   ├── auth.py                          # Landing, login, register & guest flow
│   │   ├── chat_interface.py                # Chat UI & offline keyword fallback
│   │   ├── sidebar.py                       # Role-based navigation, settings & export
│   │   └── theme.py                         # Global dark theme CSS
│   └── pages/
│       ├── 1_Admissions.py                  # Admissions overview, seats, timeline & checklist
│       ├── 2_Courses.py                     # UG/PG programs, seats & specializations
│       ├── 3_Facilities.py                  # Library, hostels, sports & laboratory analytics
│       ├── 4_Fees_&_Scholarships.py         # Fee charts, scholarships & interactive cost calculator
│       ├── 5_Placements.py                  # Placement KPIs, recruiters, training & trends
│       └── 6_Contact_Information.py         # Offices, departments, emergency & contact form
├── backend/
│   ├── requirements.txt                     # Backend dependencies (FastAPI >=0.115.0)
│   ├── .env.example                         # Environment variable template
│   ├── alembic.ini                          # Alembic configuration
│   ├── alembic/
│   │   ├── env.py                           # Alembic runtime environment
│   │   └── versions/                        # 001 -> 002 -> 003 -> 8bc28335b2c5 migrations
│   ├── scripts/                             # Admin bootstrap, reset, token & DB validation CLIs
│   └── app/
│       ├── main.py                          # FastAPI app, middleware, exception handlers & routers
│       ├── nlp_pipeline.py                  # Rule-based intent scoring & entity extraction
│       ├── response_generator.py            # Template & fallback response generator
│       ├── api/                             # auth.py, chat.py, health.py, intents.py, knowledge.py
│       ├── core/                            # config.py, security.py, logging.py, exceptions.py, error_handlers.py
│       ├── database/
│       │   ├── connection.py                # PostgreSQL engine & pooling
│       │   ├── models.py                    # 6 SQLAlchemy ORM models
│       │   └── repositories/                # admissions, contacts, courses, facilities, qa, users
│       ├── schemas/                         # Pydantic v2 schemas (auth.py, chat.py, knowledge.py)
│       └── services/                        # auth_service.py, chat_service.py
├── data/knowledge_base/                     # admission_data.json, course_catalog.json
├── tests/
│   ├── conftest.py                          # Shared Pytest fixtures
│   ├── run_all_tests.py                     # Test suite CLI wrapper
│   ├── README.md                            # Testing documentation
│   ├── unit/                                # 7 unit test files (52 tests)
│   └── integration/                         # 3 integration test files (45 tests)
├── docs/                                    # Architecture, auth, migration & deployment docs
├── pytest.ini                               # Pytest markers & CLI defaults
├── render.yaml                              # Render Blueprint (backend, frontend, PostgreSQL)
├── requirements.txt                         # Root Python dependencies
├── LICENSE                                  # MIT License
└── README.md                                # Project documentation
```

</details>

---

## Contributing, License & Contact

### Contributing

1. Fork the repository and create a feature branch (`git checkout -b feature/your-feature`).
2. Follow **PEP 8** style conventions with type hints, concise docstrings, and focused functions.
3. Add unit or integration tests in `tests/` following [tests/README.md](tests/README.md).
4. Verify all checks pass before opening a pull request: `python -m pytest tests/ -v`.

### License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contact Information

### Madhan Mohan Reddy

- **Email**: <madhanmohanreddyperam06@gmail.com>
- **Mobile**: +91 9110395993

---
<div align="center">
© 2026 MITRA. All rights reserved.
</div>
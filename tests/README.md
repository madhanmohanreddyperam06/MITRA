# MITRA Test Suite

This directory contains the test suite for the MITRA project, organized into unit and integration tests.

## Test Strategy

The test suite uses pytest with fixtures to provide flexible database testing:

### Unit Tests (`tests/unit/`)
- **Database**: MySQL
- **Purpose**: Test individual components in isolation
- **Markers**: `@pytest.mark.unit`
- **Speed**: Fast

### Integration Tests (`tests/integration/`)
- **Database**: MySQL
- **Purpose**: Test component interactions and API endpoints
- **Markers**: `@pytest.mark.integration`
- **Speed**: Medium

### MySQL-Specific Tests (`tests/integration/test_mysql_integration.py`)
- **Database**: MySQL only
- **Purpose**: Verify MySQL compatibility and MySQL-specific features
- **Markers**: `@pytest.mark.mysql`
- **Speed**: Medium (requires MySQL database)
- **Note**: Skipped if MySQL is not configured

## Test Organization

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── run_all_tests.py              # Convenience script to run tests
├── README.md                     # This file
├── unit/                         # Unit tests
│   ├── test_config.py           # Configuration tests
│   ├── test_database.py         # Legacy database tests
│   ├── test_nlp.py              # NLP pipeline tests
│   ├── test_repositories.py     # Repository layer tests
│   └── test_response_generator.py # Response generator tests
└── integration/                  # Integration tests
    ├── test_api.py              # API endpoint tests
    └── test_mysql_integration.py # MySQL-specific tests
```

## Running Tests

### Run All Tests (Unit + Integration)
```bash
# Using pytest directly
pytest tests/ -v

# Using the convenience script
python tests/run_all_tests.py
```

### Run Only Unit Tests
```bash
# Using pytest
pytest tests/ -m unit -v

# Using the convenience script
python tests/run_all_tests.py --unit
```

### Run Only Integration Tests
```bash
# Using pytest
pytest tests/ -m integration -v

# Using the convenience script
python tests/run_all_tests.py --integration
```

### Run MySQL-Specific Tests
```bash
# Set DATABASE_URL to MySQL first
export DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mitra_test

# Run tests
pytest tests/ -m mysql -v

# Or using the convenience script
python tests/run_all_tests.py --mysql
```

### Run with Coverage Report
```bash
# Using pytest
pytest tests/ --cov=backend/app --cov-report=html --cov-report=term-missing

# Using the convenience script
python tests/run_all_tests.py --cov
```

### Run a Specific Test File
```bash
pytest tests/unit/test_repositories.py -v
```

### Run a Specific Test Function
```bash
pytest tests/unit/test_repositories.py::test_admission_repository -v
```

## Database Configuration

### MySQL Configuration
- Set `DATABASE_URL` in `backend/.env` or as environment variable:
  ```bash
  export DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mitra_test
  pytest tests/ -v
  ```

## Fixtures

The `conftest.py` file provides the following fixtures:

### `test_engine`
- Creates a test database engine using MySQL
- Automatically creates/drops tables

### `test_db`
- Creates a database session
- Each test gets a fresh session
- Automatically closes the session after the test

### `seed_test_data`
- Seeds the test database with sample data
- Automatically used by tests that need it
- Includes: admission, course, facility, contact, and QA data

### `mysql_engine` and `mysql_db`
- MySQL-specific fixtures
- Automatically skipped if MySQL is not available
- Used by `@pytest.mark.mysql` tests

### `cleanup_mysql_test_data`
- Automatically cleans up test data from MySQL
- Runs after each test when using MySQL
- Prevents test data pollution

## Test Markers

- `@pytest.mark.unit`: Unit tests (MySQL)
- `@pytest.mark.integration`: Integration tests (MySQL)
- `@pytest.mark.mysql`: MySQL-specific tests (requires MySQL database)
- `@pytest.mark.slow`: Slow running tests

## Writing New Tests

### Unit Test Example
```python
import pytest
from app.database.repositories.admissions import AdmissionRepository

@pytest.mark.unit
def test_admission_repository(test_db, seed_test_data):
    """Test AdmissionRepository with pytest fixtures."""
    repo = AdmissionRepository(test_db)

    # Test logic here
    admissions = repo.get_all()
    assert len(admissions) > 0
```

### Integration Test Example
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_api_endpoint(api_client):
    """Test API endpoint with pytest fixtures."""
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### MySQL-Specific Test Example
```python
import pytest
from app.database.repositories.admissions import AdmissionRepository

@pytest.mark.mysql
def test_mysql_repository(mysql_db):
    """Test repository with MySQL."""
    repo = AdmissionRepository(mysql_db)
    # Test logic here
```

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

1. **Default CI**: Run unit tests only (fast, no database required)
   ```bash
   pytest tests/ -m unit -v
   ```

2. **Full CI**: Run unit + integration tests with MySQL
   ```bash
   pytest tests/ -m "unit or integration" -v
   ```

3. **MySQL CI**: Run all tests including MySQL-specific tests
   ```bash
   export DATABASE_URL=mysql+pymysql://...
   pytest tests/ -v
   ```

## Troubleshooting

### Tests Fail with "Module not found"
- Ensure you're running from the project root directory
- Install dependencies: `pip install -r requirements.txt`

### MySQL Tests are Skipped
- Set `DATABASE_URL` to a MySQL connection string
- Ensure MySQL is running and accessible
- Create the test database: `CREATE DATABASE mitra_test;`

### Tests are Slow
- Run only unit tests: `pytest tests/ -m unit -v`

### Database Lock Errors
- Ensure each test uses its own session (provided by `test_db` fixture)
- Don't share sessions between tests
- Use `test_engine` fixture for table creation/dropping

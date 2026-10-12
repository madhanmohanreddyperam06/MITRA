"""Pytest configuration and fixtures for MITRA tests.

This module provides database fixtures and test configuration to support:
- Unit and integration tests with MySQL database
- Proper database setup/teardown between tests
- Test data seeding and cleanup
"""
import sys
import os
import tempfile
import pytest
from typing import Generator

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load .env.test or .env file for MySQL integration tests
test_env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env.test')
backend_env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
if os.path.exists(test_env_path):
    from dotenv import load_dotenv
    load_dotenv(test_env_path, override=True)
elif os.path.exists(backend_env_path):
    from dotenv import load_dotenv
    load_dotenv(backend_env_path)

# Set default JWT secret for tests if not set
if 'JWT_SECRET_KEY' not in os.environ:
    os.environ['JWT_SECRET_KEY'] = 'test-secret-for-integration-tests'

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base, Admission, Course, Facility, ContactInfo, QADataset, User
from app.core.config import settings


from functools import lru_cache


# Test database URL configuration
@lru_cache(maxsize=1)
def get_test_database_url() -> str:
    """Get test database URL based on environment configuration."""
    env_db_url = os.environ.get('DATABASE_URL', '')

    if env_db_url and 'mysql' in env_db_url.lower():
        return env_db_url

    # Default fallback to configured MySQL URL
    return settings.DATABASE_URL


# Database engine fixture
@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine using MySQL."""
    db_url = get_test_database_url()

    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10,
        connect_args={"connect_timeout": 3}
    )

    try:
        # Create tables using SQLAlchemy (acceptable for test environment)
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        pytest.skip(f"MySQL database not accessible: {e}")

    yield engine

    # Cleanup: drop tables after test
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass


# Database session fixture
@pytest.fixture(scope="function")
def test_db(test_engine) -> Generator[Session, None, None]:
    """Create a test database session.

    Each test gets a fresh session with transaction rollback.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Test data seeding fixture
@pytest.fixture(scope="function")
def seed_test_data(test_db: Session) -> None:
    """Seed test database with sample data.

    This fixture is automatically used by tests that need sample data.
    """
    # Add admission
    admission = Admission(
        category="undergraduate",
        information="Eligibility",
        details="12th standard with minimum 60% marks"
    )
    test_db.add(admission)

    # Add course
    course = Course(
        course_name="Computer Science Engineering",
        department="Engineering",
        duration="4 years",
        eligibility="12th with PCM",
        description="Comprehensive program"
    )
    test_db.add(course)

    # Add facility
    facility = Facility(
        facility_name="Central Library",
        category="Academic",
        description="Modern library",
        location="Main Campus",
        timings="8 AM to 8 PM"
    )
    test_db.add(facility)

    # Add contact
    contact = ContactInfo(
        department="Admissions",
        contact_person="Dr. Smith",
        phone="+91-123-456-7890",
        email="admissions@college.edu",
        office_location="Admin Block"
    )
    test_db.add(contact)

    # Add QA
    qa = QADataset(question="Test question", answer="Test answer")
    test_db.add(qa)

    test_db.commit()


# MySQL-specific fixture (optional, for MySQL integration tests)
@pytest.fixture(scope="function")
def mysql_engine():
    """Create MySQL engine for MySQL-specific integration tests.

    This fixture is skipped if MySQL is not available.
    """
    db_url = os.environ.get('DATABASE_URL', '')

    if not db_url or 'mysql' not in db_url.lower():
        pytest.skip("MySQL integration tests require DATABASE_URL set to MySQL")

    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10
        )

        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        # Create all tables for MySQL integration tests
        Base.metadata.create_all(bind=engine)

        yield engine

    except Exception as e:
        pytest.skip(f"MySQL not available: {e}")

    # Cleanup
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass


# MySQL session fixture
@pytest.fixture(scope="function")
def mysql_db(mysql_engine) -> Generator[Session, None, None]:
    """Create MySQL session for MySQL-specific tests."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=mysql_engine
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Cleanup fixture for MySQL test data
@pytest.fixture(scope="function")
def cleanup_mysql_test_data(mysql_db):
    """Clean up test data from MySQL after test.

    This fixture only runs when using MySQL and cleans up known test data.
    """
    yield

    try:
        mysql_db.execute(text("DELETE FROM qa_dataset WHERE question = 'Test question'"))
        mysql_db.execute(text("DELETE FROM qa_dataset WHERE question LIKE 'Integration test%'"))
        mysql_db.execute(text("DELETE FROM contact_info WHERE department = 'Admissions' AND contact_person = 'Dr. Smith'"))
        mysql_db.execute(text("DELETE FROM facilities WHERE facility_name = 'Central Library'"))
        mysql_db.execute(text("DELETE FROM courses WHERE course_name = 'Computer Science Engineering'"))
        mysql_db.execute(text("DELETE FROM admissions WHERE category = 'undergraduate' AND information = 'Eligibility'"))
        mysql_db.commit()
    except Exception:
        mysql_db.rollback()


# Pytest markers configuration
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (MySQL)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test (MySQL)"
    )
    config.addinivalue_line(
        "markers", "mysql: mark test as MySQL-specific (requires MySQL database)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

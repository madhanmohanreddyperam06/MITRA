"""Integration tests for API endpoints using pytest fixtures."""
import sys
import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import text

# Import after path setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from app.main import app
from app.database.models import Base, Admission, Course, Facility, ContactInfo, QADataset
from sqlalchemy.orm import sessionmaker
from app.database.connection import get_db


@pytest.fixture(scope="function")
def api_client(test_engine):
    """Create a FastAPI test client with test database."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Seed test data
    db = TestingSessionLocal()
    admission = Admission(
        category="undergraduate",
        information="Eligibility",
        details="12th standard with minimum 60% marks"
    )
    db.add(admission)
    course = Course(
        course_name="Computer Science Engineering",
        department="Engineering",
        duration="4 years",
        eligibility="12th with PCM",
        description="Comprehensive program"
    )
    db.add(course)
    facility = Facility(
        facility_name="Central Library",
        category="Academic",
        description="Modern library",
        location="Main Campus",
        timings="8 AM to 8 PM"
    )
    db.add(facility)
    contact = ContactInfo(
        department="Admissions",
        contact_person="Dr. Smith",
        phone="+91-123-456-7890",
        email="admissions@college.edu",
        office_location="Admin Block"
    )
    db.add(contact)
    qa = QADataset(question="Test question", answer="Test answer")
    db.add(qa)
    db.commit()
    db.close()

    # Create test client
    client = TestClient(app)
    yield client

    # Cleanup: clear overrides and drop tables
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.mark.integration
def test_root_endpoint(api_client):
    """Test root endpoint"""
    response = api_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.integration
def test_health_endpoint(api_client):
    """Test health check endpoint"""
    response = api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "MITRA"


@pytest.mark.integration
def test_intents_endpoint(api_client):
    """Test intents endpoint"""
    response = api_client.get("/intents")
    assert response.status_code == 200
    data = response.json()
    assert "intents" in data
    assert isinstance(data["intents"], list)
    assert len(data["intents"]) > 0


@pytest.mark.integration
def test_chat_endpoint(api_client):
    """Test chat endpoint"""
    response = api_client.post(
        "/chat",
        json={
            "user_input": "Tell me about admissions",
            "user_context": {},
            "conversation_history": []
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "intent" in data
    assert "confidence" in data
    assert "entities" in data


@pytest.mark.integration
def test_chat_validation(api_client):
    """Test chat endpoint validation"""
    # Test empty user_input
    response = api_client.post(
        "/chat",
        json={
            "user_input": "",
            "user_context": {},
            "conversation_history": []
        }
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_qa_get_endpoint(api_client):
    """Test get Q&A pairs endpoint"""
    api_client.post(
        "/api/auth/register",
        json={"username": "qauser", "email": "qa@example.com", "password": "TestPassword123!"}
    )
    login_res = api_client.post(
        "/api/auth/login",
        json={"username_or_email": "qauser", "password": "TestPassword123!"}
    )
    token = login_res.json()["access_token"]
    response = api_client.get("/qa", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
def test_qa_search_endpoint(api_client):
    """Test search Q&A pairs endpoint"""
    api_client.post(
        "/api/auth/register",
        json={"username": "qauser", "email": "qa@example.com", "password": "TestPassword123!"}
    )
    login_res = api_client.post(
        "/api/auth/login",
        json={"username_or_email": "qauser", "password": "TestPassword123!"}
    )
    token = login_res.json()["access_token"]
    response = api_client.get("/qa?question=Test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
def test_qa_add_endpoint(api_client):
    """Test add Q&A pair endpoint"""
    api_client.post(
        "/api/auth/register",
        json={"username": "qauser", "email": "qa@example.com", "password": "TestPassword123!"}
    )
    login_res = api_client.post(
        "/api/auth/login",
        json={"username_or_email": "qauser", "password": "TestPassword123!"}
    )
    token = login_res.json()["access_token"]
    response = api_client.post(
        "/qa",
        json={
            "question": "Integration test question",
            "answer": "Integration test answer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "id" in data

"""Tests for chat service (replaces legacy response generator)."""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app.services.chat_service import ChatService
from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository


@pytest.mark.unit
def test_chat_service_initialization(test_db, seed_test_data):
    """Test chat service initialization"""
    admission_repo = AdmissionRepository(test_db)
    course_repo = CourseRepository(test_db)
    facility_repo = FacilityRepository(test_db)
    contact_repo = ContactRepository(test_db)
    qa_repo = QARepository(test_db)

    chat_service = ChatService(
        admission_repo=admission_repo,
        course_repo=course_repo,
        facility_repo=facility_repo,
        contact_repo=contact_repo,
        qa_repo=qa_repo
    )

    assert chat_service is not None
    assert chat_service.admission_repo is not None
    assert chat_service.course_repo is not None


@pytest.mark.unit
def test_admission_response(test_db, seed_test_data):
    """Test admission query response"""
    admission_repo = AdmissionRepository(test_db)
    course_repo = CourseRepository(test_db)
    facility_repo = FacilityRepository(test_db)
    contact_repo = ContactRepository(test_db)
    qa_repo = QARepository(test_db)

    chat_service = ChatService(
        admission_repo=admission_repo,
        course_repo=course_repo,
        facility_repo=facility_repo,
        contact_repo=contact_repo,
        qa_repo=qa_repo
    )

    response = chat_service._handle_admission_query([], "Tell me about admissions")
    assert response is not None
    assert len(response) > 0


@pytest.mark.unit
def test_course_response(test_db, seed_test_data):
    """Test course query response"""
    admission_repo = AdmissionRepository(test_db)
    course_repo = CourseRepository(test_db)
    facility_repo = FacilityRepository(test_db)
    contact_repo = ContactRepository(test_db)
    qa_repo = QARepository(test_db)

    chat_service = ChatService(
        admission_repo=admission_repo,
        course_repo=course_repo,
        facility_repo=facility_repo,
        contact_repo=contact_repo,
        qa_repo=qa_repo
    )

    response = chat_service._handle_course_query([], "What courses are available?")
    assert response is not None
    assert len(response) > 0


@pytest.mark.unit
def test_fee_response(test_db, seed_test_data):
    """Test fee query response"""
    admission_repo = AdmissionRepository(test_db)
    course_repo = CourseRepository(test_db)
    facility_repo = FacilityRepository(test_db)
    contact_repo = ContactRepository(test_db)
    qa_repo = QARepository(test_db)

    chat_service = ChatService(
        admission_repo=admission_repo,
        course_repo=course_repo,
        facility_repo=facility_repo,
        contact_repo=contact_repo,
        qa_repo=qa_repo
    )

    response = chat_service._handle_fee_query([], "What is the fee structure?")
    assert response is not None
    assert "₹" in response or "fee" in response.lower()


@pytest.mark.unit
def test_general_response(test_db, seed_test_data):
    """Test general query response"""
    admission_repo = AdmissionRepository(test_db)
    course_repo = CourseRepository(test_db)
    facility_repo = FacilityRepository(test_db)
    contact_repo = ContactRepository(test_db)
    qa_repo = QARepository(test_db)

    chat_service = ChatService(
        admission_repo=admission_repo,
        course_repo=course_repo,
        facility_repo=facility_repo,
        contact_repo=contact_repo,
        qa_repo=qa_repo
    )

    response = chat_service._handle_general_query("Tell me about the college")
    assert response is not None
    assert len(response) > 0

"""Baseline tests for database layer using pytest fixtures."""
import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository


@pytest.mark.unit
def test_database_initialization(test_engine):
    """Test database initialization"""
    assert test_engine is not None


@pytest.mark.unit
def test_get_admission_info(test_db, seed_test_data):
    """Test getting admission information"""
    repo = AdmissionRepository(test_db)
    admissions = repo.get_all()
    assert isinstance(admissions, list)
    assert len(admissions) > 0


@pytest.mark.unit
def test_get_course_info(test_db, seed_test_data):
    """Test getting course information"""
    repo = CourseRepository(test_db)
    courses = repo.get_all()
    assert isinstance(courses, list)
    assert len(courses) > 0


@pytest.mark.unit
def test_get_facility_info(test_db, seed_test_data):
    """Test getting facility information"""
    repo = FacilityRepository(test_db)
    facilities = repo.get_all()
    assert isinstance(facilities, list)
    assert len(facilities) > 0


@pytest.mark.unit
def test_get_contact_info(test_db, seed_test_data):
    """Test getting contact information"""
    repo = ContactRepository(test_db)
    contacts = repo.get_all()
    assert isinstance(contacts, list)
    assert len(contacts) > 0


@pytest.mark.unit
def test_add_qa_pair(test_db, seed_test_data):
    """Test adding Q&A pair"""
    repo = QARepository(test_db)

    # Add a test Q&A pair
    qa_id = repo.add("Test question", "Test answer")
    assert qa_id is not None
    assert qa_id > 0

    # Verify it was added
    qa_pairs = repo.search_by_question("Test")
    assert len(qa_pairs) > 0


@pytest.mark.unit
def test_search_information(test_db, seed_test_data):
    """Test searching information"""
    repo = AdmissionRepository(test_db)
    results = repo.get_all()
    assert isinstance(results, list)

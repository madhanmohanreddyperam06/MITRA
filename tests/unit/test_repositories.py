"""Unit tests for repository layer using pytest fixtures."""
import pytest
from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository


@pytest.mark.unit
def test_admission_repository(test_db, seed_test_data):
    """Test AdmissionRepository with pytest fixtures."""
    repo = AdmissionRepository(test_db)

    # Test get_all
    admissions = repo.get_all()
    assert len(admissions) == 1
    assert admissions[0]['category'] == 'undergraduate'

    # Test get_by_category
    admissions = repo.get_by_category('undergraduate')
    assert len(admissions) == 1

    # Test get_by_id
    admission = repo.get_by_id(admissions[0]['id'])
    assert admission is not None
    assert admission['category'] == 'undergraduate'


@pytest.mark.unit
def test_course_repository(test_db, seed_test_data):
    """Test CourseRepository with pytest fixtures."""
    repo = CourseRepository(test_db)

    # Test get_all
    courses = repo.get_all()
    assert len(courses) == 1
    assert courses[0]['course_name'] == 'Computer Science Engineering'

    # Test get_by_department
    courses = repo.get_by_department('Engineering')
    assert len(courses) == 1

    # Test get_by_id
    course = repo.get_by_id(courses[0]['id'])
    assert course is not None
    assert course['course_name'] == 'Computer Science Engineering'


@pytest.mark.unit
def test_facility_repository(test_db, seed_test_data):
    """Test FacilityRepository with pytest fixtures."""
    repo = FacilityRepository(test_db)

    # Test get_all
    facilities = repo.get_all()
    assert len(facilities) == 1
    assert facilities[0]['facility_name'] == 'Central Library'

    # Test get_by_category
    facilities = repo.get_by_category('Academic')
    assert len(facilities) == 1

    # Test get_by_id
    facility = repo.get_by_id(facilities[0]['id'])
    assert facility is not None
    assert facility['facility_name'] == 'Central Library'


@pytest.mark.unit
def test_contact_repository(test_db, seed_test_data):
    """Test ContactRepository with pytest fixtures."""
    repo = ContactRepository(test_db)

    # Test get_all
    contacts = repo.get_all()
    assert len(contacts) == 1
    assert contacts[0]['department'] == 'Admissions'

    # Test get_by_department
    contacts = repo.get_by_department('Admissions')
    assert len(contacts) == 1

    # Test get_by_id
    contact = repo.get_by_id(contacts[0]['id'])
    assert contact is not None
    assert contact['department'] == 'Admissions'


@pytest.mark.unit
def test_qa_repository(test_db, seed_test_data):
    """Test QARepository with pytest fixtures."""
    repo = QARepository(test_db)

    # Test get_all
    qa_pairs = repo.get_all()
    assert len(qa_pairs) == 1
    assert qa_pairs[0]['question'] == 'Test question'

    # Test search_by_question
    qa_pairs = repo.search_by_question('Test')
    assert len(qa_pairs) == 1

    # Test get_by_id
    qa = repo.get_by_id(qa_pairs[0]['id'])
    assert qa is not None
    assert qa['question'] == 'Test question'

    # Test add
    qa_id = repo.add("New question", "New answer")
    assert qa_id is not None
    assert qa_id > 0

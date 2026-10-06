"""MySQL integration tests for MITRA database migration using pytest fixtures.

These tests require a running MySQL instance and are optional for Phase 2 validation.
They should be run after the migration is complete to verify MySQL compatibility.

To run these tests:
1. Set DATABASE_URL to a MySQL connection string
2. Ensure MySQL database is created and accessible
3. Run: pytest tests/integration/test_mysql_integration.py -v

Example:
    DATABASE_URL=mysql+pymysql://mitra_user:password@localhost:3306/mitra_test pytest tests/integration/test_mysql_integration.py -v
"""
import pytest
from sqlalchemy import text
from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository


@pytest.mark.mysql
def test_mysql_connection(mysql_engine):
    """Test MySQL database connection."""
    with mysql_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.mysql
def test_mysql_tables_exist(mysql_engine):
    """Test that all required tables exist in MySQL."""
    with mysql_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = DATABASE()
        """))
        tables = {row[0] for row in result.fetchall()}

        required_tables = {'admissions', 'courses', 'facilities', 'contact_info', 'qa_dataset'}
        assert required_tables.issubset(tables), f"Missing tables: {required_tables - tables}"


@pytest.mark.mysql
def test_mysql_admission_repository(mysql_db):
    """Test AdmissionRepository with MySQL."""
    repo = AdmissionRepository(mysql_db)

    # Test get_all
    admissions = repo.get_all()
    assert isinstance(admissions, list)

    # If data exists, test get_by_category
    if admissions:
        category = admissions[0]['category']
        if category:
            by_category = repo.get_by_category(category)
            assert isinstance(by_category, list)


@pytest.mark.mysql
def test_mysql_course_repository(mysql_db):
    """Test CourseRepository with MySQL."""
    repo = CourseRepository(mysql_db)

    # Test get_all
    courses = repo.get_all()
    assert isinstance(courses, list)

    # If data exists, test get_by_department
    if courses:
        department = courses[0]['department']
        if department:
            by_dept = repo.get_by_department(department)
            assert isinstance(by_dept, list)


@pytest.mark.mysql
def test_mysql_facility_repository(mysql_db):
    """Test FacilityRepository with MySQL."""
    repo = FacilityRepository(mysql_db)

    # Test get_all
    facilities = repo.get_all()
    assert isinstance(facilities, list)

    # If data exists, test get_by_category
    if facilities:
        category = facilities[0]['category']
        if category:
            by_category = repo.get_by_category(category)
            assert isinstance(by_category, list)


@pytest.mark.mysql
def test_mysql_contact_repository(mysql_db):
    """Test ContactRepository with MySQL."""
    repo = ContactRepository(mysql_db)

    # Test get_all
    contacts = repo.get_all()
    assert isinstance(contacts, list)

    # If data exists, test get_by_department
    if contacts:
        department = contacts[0]['department']
        if department:
            by_dept = repo.get_by_department(department)
            assert isinstance(by_dept, list)


@pytest.mark.mysql
def test_mysql_qa_repository(mysql_db):
    """Test QARepository with MySQL."""
    repo = QARepository(mysql_db)

    # Test get_all
    qa_pairs = repo.get_all()
    assert isinstance(qa_pairs, list)

    # Test search_by_question
    if qa_pairs:
        question = qa_pairs[0]['question']
        if question:
            # Search for first word
            search_term = question.split()[0] if question.split() else ""
            if search_term:
                results = repo.search_by_question(search_term)
                assert isinstance(results, list)


@pytest.mark.mysql
def test_mysql_unicode_handling(mysql_db):
    """Test Unicode data handling in MySQL."""
    repo = QARepository(mysql_db)
    test_question = "Test question with Unicode: ñ, é, 中文, हिन"
    test_answer = "Test answer with Unicode: ñ, é, 中文, हिन"

    qa_id = repo.add(test_question, test_answer)
    assert qa_id is not None

    # Retrieve and verify
    retrieved = repo.get_by_id(qa_id)
    assert retrieved is not None
    assert retrieved['question'] == test_question
    assert retrieved['answer'] == test_answer

    # Clean up
    mysql_db.execute(text(f"DELETE FROM qa_dataset WHERE id = {qa_id}"))
    mysql_db.commit()


@pytest.mark.mysql
def test_mysql_auto_increment(mysql_db):
    """Test auto-increment behavior in MySQL."""
    repo = QARepository(mysql_db)

    # Get current max ID
    result = mysql_db.execute(text("SELECT MAX(id) FROM qa_dataset"))
    max_id = result.scalar() or 0

    # Insert new record
    qa_id = repo.add("Auto-increment test", "Test answer")
    assert qa_id > max_id

    # Verify it auto-incremented
    assert qa_id == max_id + 1

    # Clean up
    mysql_db.execute(text(f"DELETE FROM qa_dataset WHERE id = {qa_id}"))
    mysql_db.commit()

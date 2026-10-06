"""SQLAlchemy models matching the actual database schema."""
from sqlalchemy import Column, Integer, String, Text, Index, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Admission(Base):
    """Admission information model."""
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=True)
    information = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)

    __table_args__ = (
        Index('ix_admissions_category', 'category'),
    )


class Course(Base):
    """Course information model."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    eligibility = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        Index('ix_courses_course_name', 'course_name'),
        Index('ix_courses_department', 'department'),
    )


class Facility(Base):
    """Facility information model."""
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    timings = Column(String(100), nullable=True)

    __table_args__ = (
        Index('ix_facilities_facility_name', 'facility_name'),
        Index('ix_facilities_category', 'category'),
    )


class ContactInfo(Base):
    """Contact information model."""
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String(100), nullable=True)
    contact_person = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    office_location = Column(String(255), nullable=True)

    __table_args__ = (
        Index('ix_contact_info_department', 'department'),
    )


class QADataset(Base):
    """Q&A dataset model."""
    __tablename__ = "qa_dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)

    __table_args__ = (
        Index('ix_qa_dataset_question', 'question'),
    )


class User(Base):
    """User model for regular users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_email', 'email'),
    )

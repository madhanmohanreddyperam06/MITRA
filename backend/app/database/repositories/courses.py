"""Repository for course data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Course
from app.core.exceptions import DatabaseError


class CourseRepository:
    """Repository for course-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all course information."""
        try:
            result = self.db.execute(select(Course))
            courses = result.scalars().all()
            return [
                {
                    "id": c.id,
                    "course_name": c.course_name,
                    "department": c.department,
                    "duration": c.duration,
                    "eligibility": c.eligibility,
                    "description": c.description
                }
                for c in courses
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch course info: {e}")

    def get_by_department(self, department: str) -> List[Dict[str, Any]]:
        """Get course information by department."""
        try:
            result = self.db.execute(
                select(Course).where(Course.department == department)
            )
            courses = result.scalars().all()
            return [
                {
                    "id": c.id,
                    "course_name": c.course_name,
                    "department": c.department,
                    "duration": c.duration,
                    "eligibility": c.eligibility,
                    "description": c.description
                }
                for c in courses
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch course info by department: {e}")

    def get_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        """Get course information by ID."""
        try:
            course = self.db.get(Course, course_id)
            if course:
                return {
                    "id": course.id,
                    "course_name": course.course_name,
                    "department": course.department,
                    "duration": course.duration,
                    "eligibility": course.eligibility,
                    "description": course.description
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch course info by ID: {e}")

"""Repository for admission data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Admission
from app.core.exceptions import DatabaseError


class AdmissionRepository:
    """Repository for admission-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all admission information."""
        try:
            result = self.db.execute(select(Admission))
            admissions = result.scalars().all()
            return [
                {
                    "id": a.id,
                    "category": a.category,
                    "information": a.information,
                    "details": a.details
                }
                for a in admissions
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch admission info: {e}")

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get admission information by category."""
        try:
            result = self.db.execute(
                select(Admission).where(Admission.category == category)
            )
            admissions = result.scalars().all()
            return [
                {
                    "id": a.id,
                    "category": a.category,
                    "information": a.information,
                    "details": a.details
                }
                for a in admissions
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch admission info by category: {e}")

    def get_by_id(self, admission_id: int) -> Optional[Dict[str, Any]]:
        """Get admission information by ID."""
        try:
            admission = self.db.get(Admission, admission_id)
            if admission:
                return {
                    "id": admission.id,
                    "category": admission.category,
                    "information": admission.information,
                    "details": admission.details
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch admission info by ID: {e}")

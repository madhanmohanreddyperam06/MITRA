"""Repository for facility data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Facility
from app.core.exceptions import DatabaseError


class FacilityRepository:
    """Repository for facility-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all facility information."""
        try:
            result = self.db.execute(select(Facility))
            facilities = result.scalars().all()
            return [
                {
                    "id": f.id,
                    "facility_name": f.facility_name,
                    "category": f.category,
                    "description": f.description,
                    "location": f.location,
                    "timings": f.timings
                }
                for f in facilities
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch facility info: {e}")

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get facility information by category."""
        try:
            result = self.db.execute(
                select(Facility).where(Facility.category == category)
            )
            facilities = result.scalars().all()
            return [
                {
                    "id": f.id,
                    "facility_name": f.facility_name,
                    "category": f.category,
                    "description": f.description,
                    "location": f.location,
                    "timings": f.timings
                }
                for f in facilities
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch facility info by category: {e}")

    def get_by_id(self, facility_id: int) -> Optional[Dict[str, Any]]:
        """Get facility information by ID."""
        try:
            facility = self.db.get(Facility, facility_id)
            if facility:
                return {
                    "id": facility.id,
                    "facility_name": facility.facility_name,
                    "category": facility.category,
                    "description": facility.description,
                    "location": facility.location,
                    "timings": facility.timings
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch facility info by ID: {e}")

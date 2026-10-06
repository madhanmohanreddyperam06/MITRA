"""Repository for contact data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import ContactInfo
from app.core.exceptions import DatabaseError


class ContactRepository:
    """Repository for contact-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all contact information."""
        try:
            result = self.db.execute(select(ContactInfo))
            contacts = result.scalars().all()
            return [
                {
                    "id": c.id,
                    "department": c.department,
                    "contact_person": c.contact_person,
                    "phone": c.phone,
                    "email": c.email,
                    "office_location": c.office_location
                }
                for c in contacts
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch contact info: {e}")

    def get_by_department(self, department: str) -> List[Dict[str, Any]]:
        """Get contact information by department."""
        try:
            result = self.db.execute(
                select(ContactInfo).where(ContactInfo.department == department)
            )
            contacts = result.scalars().all()
            return [
                {
                    "id": c.id,
                    "department": c.department,
                    "contact_person": c.contact_person,
                    "phone": c.phone,
                    "email": c.email,
                    "office_location": c.office_location
                }
                for c in contacts
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch contact info by department: {e}")

    def get_by_id(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """Get contact information by ID."""
        try:
            contact = self.db.get(ContactInfo, contact_id)
            if contact:
                return {
                    "id": contact.id,
                    "department": contact.department,
                    "contact_person": contact.contact_person,
                    "phone": contact.phone,
                    "email": contact.email,
                    "office_location": contact.office_location
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch contact info by ID: {e}")

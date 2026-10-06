"""Repository for user data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import User
from app.core.exceptions import DatabaseError


class UserRepository:
    """Repository for user-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        try:
            user = self.db.get(User, user_id)
            if user:
                return self._user_to_dict(user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user by ID: {e}")

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        try:
            result = self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            if user:
                return self._user_to_dict(user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user by email: {e}")

    def get_by_email_with_hash(self, email: str) -> Optional[User]:
        """Get user model by email (includes password_hash for authentication)."""
        try:
            result = self.db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user by email: {e}")

    def get_by_username_with_hash(self, username: str) -> Optional[User]:
        """Get user model by username (includes password_hash for authentication)."""
        try:
            result = self.db.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user by username: {e}")

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        try:
            result = self.db.execute(
                select(User).where(User.username == username)
            )
            user = result.scalar_one_or_none()
            if user:
                return self._user_to_dict(user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch user by username: {e}")

    def list_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        try:
            result = self.db.execute(select(User))
            users = result.scalars().all()
            return [self._user_to_dict(user) for user in users]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch users: {e}")

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        try:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                full_name=user_data.get('full_name'),
                is_active=user_data.get('is_active', True)
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return self._user_to_dict(user)
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create user: {e}")

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user information."""
        try:
            user = self.db.get(User, user_id)
            if not user:
                return None

            for key, value in user_data.items():
                if hasattr(user, key) and key != 'id':
                    setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)
            return self._user_to_dict(user)
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update user: {e}")

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        try:
            user = self.db.get(User, user_id)
            if not user:
                return False

            self.db.delete(user)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete user: {e}")

    def update_last_login(self, user_id: int) -> bool:
        """Update last login timestamp."""
        try:
            user = self.db.get(User, user_id)
            if not user:
                return False

            from datetime import datetime
            user.last_login_at = datetime.utcnow()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update last login: {e}")

    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert User model to dictionary (excluding sensitive fields)."""
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        }

"""Authentication and user management service."""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.database.repositories.users import UserRepository
from app.core.config import settings
from app.core.exceptions import MITRAError
from app.core.logging import logger


class AuthService:
    """Service for authentication and user management operations."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()

        if "sub" in to_encode and to_encode["sub"] is not None:
            to_encode["sub"] = str(to_encode["sub"])

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES', 30))

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.get_jwt_secret_key(),
            algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256')
        )
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and verify a JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.get_jwt_secret_key(),
                algorithms=[getattr(settings, 'JWT_ALGORITHM', 'HS256')]
            )
            return payload
        except JWTError as e:
            logger.warning(f"JWT decode error: {e}")
            return None

    def register_user(self, username: str, email: str, password: str, full_name: Optional[str] = None) -> Dict[str, Any]:
        """Register a new user."""
        # Normalize email
        email = email.lower().strip()

        # Check if email already exists
        if self.user_repo.get_by_email(email):
            raise MITRAError("Email already registered")

        # Check if username already exists
        if self.user_repo.get_by_username(username):
            raise MITRAError("Username already taken")

        # Validate password
        self._validate_password(password)

        # Hash password
        password_hash = self.hash_password(password)

        # Create user (always as normal user, never admin)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'is_active': True,
            'is_admin': False  # Public registration never creates admin
        }

        user = self.user_repo.create_user(user_data)
        logger.info(f"User registered: {username} ({email})")
        return user

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username/email and password."""
        # Try username first, then email
        user_model = self.user_repo.get_by_username_with_hash(username_or_email)
        if not user_model:
            user_model = self.user_repo.get_by_email_with_hash(username_or_email)

        if not user_model:
            logger.warning(f"Authentication failed: user not found - {username_or_email}")
            return None

        if not user_model.is_active:
            logger.warning(f"Authentication failed: inactive user - {username_or_email}")
            return None

        if not self.verify_password(password, user_model.password_hash):
            logger.warning(f"Authentication failed: invalid password - {username_or_email}")
            return None

        # Update last login
        self.user_repo.update_last_login(user_model.id)

        logger.info(f"User authenticated: {username_or_email}")
        return self.user_repo._user_to_dict(user_model)

    def activate_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Activate a user account."""
        return self.user_repo.update_user(user_id, {'is_active': True})

    def deactivate_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Deactivate a user account."""
        return self.user_repo.update_user(user_id, {'is_active': False})

    def _validate_password(self, password: str) -> None:
        """Validate password strength."""
        if not password:
            raise MITRAError("Password cannot be empty")

        if len(password) < 8:
            raise MITRAError("Password must be at least 8 characters long")

        if len(password) > 128:
            raise MITRAError("Password is too long (max 128 characters)")

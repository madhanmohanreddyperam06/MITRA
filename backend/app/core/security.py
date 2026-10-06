"""Security utilities for authentication and authorization."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories.users import UserRepository
from app.services.auth_service import AuthService
from app.core.exceptions import MITRAError
from app.core.logging import logger

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance."""
    user_repo = UserRepository(db)
    return AuthService(user_repo)


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[dict]:
    """
    Dependency to get current authenticated user if token is provided,
    or None if unauthenticated / guest request.
    """
    if not credentials or not credentials.credentials:
        return None

    try:
        token = credentials.credentials
        payload = auth_service.decode_token(token)
        if not payload:
            return None

        sub_val = payload.get("sub")
        if sub_val is None:
            return None

        user_id = int(sub_val)
        user = auth_service.user_repo.get_by_id(user_id)
        if user and user.get("is_active"):
            return user
    except Exception:
        pass
    return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    """
    Dependency to get the current authenticated user from JWT token.
    """
    token = credentials.credentials

    # Decode token
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID from token
    sub_val = payload.get("sub")
    if sub_val is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(sub_val)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = auth_service.user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user['is_active']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency to get the current active user.
    """
    return current_user

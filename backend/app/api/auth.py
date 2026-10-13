"""API router for authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories.users import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse, UserStatusUpdate
from app.core.security import get_current_user, get_auth_service
from app.core.logging import logger
from app.core.exceptions import MITRAError

router = APIRouter()

# Separate router for user management (admin functions)
user_management_router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user.
    Public endpoint.
    """
    try:
        user = auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return user
    except MITRAError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login with username/email and password.
    Returns a JWT access token.
    """
    try:
        logger.info(f"Login attempt for: {login_data.username_or_email}")
        user = auth_service.authenticate_user(
            username_or_email=login_data.username_or_email,
            password=login_data.password
        )

        if not user:
            logger.warning(f"Authentication failed for: {login_data.username_or_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": str(user['id'])}
        )

        logger.info(f"Login successful for: {login_data.username_or_email}")
        return TokenResponse(access_token=access_token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Get the current authenticated user's information.
    Requires authentication.
    """
    return current_user


@router.get("/debug/admin-check")
async def debug_admin_check(
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Debug endpoint to check admin user status.
    """
    try:
        admin_count = auth_service.user_repo.count_admins()
        admin_user = auth_service.user_repo.get_by_username_with_hash("admin")
        
        return {
            "admin_count": admin_count,
            "admin_exists": admin_user is not None,
            "admin_username": admin_user.username if admin_user else None,
            "admin_email": admin_user.email if admin_user else None,
            "admin_active": admin_user.is_active if admin_user else None,
            "admin_is_admin": admin_user.is_admin if admin_user else None,
            "password_hash_length": len(admin_user.password_hash) if admin_user else 0
        }
    except Exception as e:
        return {"error": str(e)}


# User management endpoints (admin functions) - moved to separate router
@user_management_router.get("/users", response_model=list[UserResponse])
async def list_users(
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    List all users (admin only).
    Requires authentication and admin privileges.
    """
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    users = auth_service.user_repo.list_users()
    return users


@user_management_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Get a specific user by ID (admin only).
    Requires authentication and admin privileges.
    """
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    user = auth_service.user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@user_management_router.patch("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    status_update: UserStatusUpdate,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update user active status (admin only).
    Requires authentication and admin privileges.
    """
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    user = auth_service.user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deactivating the only admin
    if user.get('is_admin') and not status_update.is_active:
        admin_count = auth_service.user_repo.count_admins()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate the only administrator"
            )
    
    updated_user = auth_service.user_repo.update_user(user_id, {'is_active': status_update.is_active})
    return updated_user


@user_management_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Delete a user (admin only).
    Requires authentication and admin privileges.
    """
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    user = auth_service.user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting the only admin
    if user.get('is_admin'):
        admin_count = auth_service.user_repo.count_admins()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the only administrator"
            )
    
    auth_service.user_repo.delete_user(user_id)
    return None

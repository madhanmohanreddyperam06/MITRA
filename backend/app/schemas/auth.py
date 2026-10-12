"""Pydantic schemas for authentication and user management."""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=255)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v

    @field_validator('username')
    @classmethod
    def username_lowercase(cls, v):
        return v.lower()


class UserLogin(BaseModel):
    """Schema for user login."""
    username_or_email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """Schema for user response (safe fields only)."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"


class UserStatusUpdate(BaseModel):
    """Schema for updating user status."""
    is_active: bool

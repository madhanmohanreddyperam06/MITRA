"""Configuration management for MITRA application."""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = Field(default="MITRA - College Helpdesk Assistant")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    # API
    API_HOST: str = Field(default="127.0.0.1")
    API_PORT: int = Field(default=8000)

    # Database
    DATABASE_URL: str = Field(default="mysql+pymysql://mitra_user:password@localhost:3306/mitra_db")

    # Authentication
    JWT_SECRET_KEY: str = Field(default="dev-secret-change-in-production")  # Development default, override in production
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # CORS
    CORS_ALLOWED_ORIGINS: str = Field(default="http://localhost:8501")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if isinstance(self.CORS_ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
        return self.CORS_ALLOWED_ORIGINS

    # NLP
    SPACY_MODEL: str = Field(default="en_core_web_sm")
    CONFIDENCE_THRESHOLD: float = Field(default=0.5)

    # Chat
    MAX_CONVERSATION_HISTORY: int = Field(default=10)
    CHAT_TIMEOUT: int = Field(default=30)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def get_absolute_db_path(self) -> str:
        """Get database URL from environment or config."""
        if 'DATABASE_URL' in os.environ:
            return os.environ['DATABASE_URL']
        else:
            return self.DATABASE_URL

    def get_jwt_secret_key(self) -> str:
        """Get JWT secret key from environment or config.

        In production, this will fail if no secret is configured.
        In development, a fallback is provided for convenience.
        """
        # Check environment variable first
        if 'JWT_SECRET_KEY' in os.environ:
            secret = os.environ['JWT_SECRET_KEY']
            # Warn if using weak secret in production
            if self.APP_ENV == 'production' and secret in ['CHANGE_ME_TO_A_SECURE_RANDOM_SECRET', 'your-secret-key', 'secret', '123456', 'dev-secret']:
                raise ValueError(
                    "CRITICAL: Insecure JWT secret key detected in production. "
                    "Please set a secure random JWT_SECRET_KEY environment variable."
                )
            return secret

        # Check if configured in settings
        if self.JWT_SECRET_KEY:
            # Warn if using weak secret in production
            if self.APP_ENV == 'production' and self.JWT_SECRET_KEY in ['CHANGE_ME_TO_A_SECURE_RANDOM_SECRET', 'your-secret-key', 'secret', '123456', 'dev-secret']:
                raise ValueError(
                    "CRITICAL: Insecure JWT secret key detected in production. "
                    "Please set a secure random JWT_SECRET_KEY environment variable."
                )
            return self.JWT_SECRET_KEY

        # Development-only fallback
        if self.APP_ENV == 'development':
            import warnings
            warnings.warn(
                "WARNING: Using development-only JWT secret. "
                "Set JWT_SECRET_KEY environment variable for production use."
            )
            return "dev-secret-change-in-production"

        # Production: fail securely
        raise ValueError(
            "CRITICAL: JWT_SECRET_KEY must be set in production environment. "
            "Please set a secure random JWT_SECRET_KEY environment variable."
        )


# Global settings instance
settings = Settings()

"""Database connection management using SQLAlchemy."""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import logger

# Get absolute database path
database_url = settings.get_absolute_db_path()


def create_app_engine(url: str):
    """Create SQLAlchemy engine for PostgreSQL database with production-ready settings."""
    logger.info("Using PostgreSQL database")

    # Ensure URL uses psycopg2 driver
    if "postgresql://" in url and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://")
        logger.info("Updated database URL to use psycopg2 driver")

    # Configure engine for PostgreSQL
    engine = create_engine(
        url,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_size=10,  # Increased pool size for production
        max_overflow=20,  # Allow overflow for peak loads
        echo=False,
        connect_args={
            "connect_timeout": 10,
        }
    )

    return engine


# Initialize global engine
engine = create_app_engine(database_url)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database connection and verify it's accessible."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully: PostgreSQL")
    except Exception as e:
        logger.warning(f"Database connection check warning: {e}")

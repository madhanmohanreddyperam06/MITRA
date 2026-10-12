"""Database connection management using SQLAlchemy."""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import logger

# Get absolute database path
database_url = settings.get_absolute_db_path()


def create_app_engine(url: str):
    """Create SQLAlchemy engine for MySQL database with production-ready settings."""
    logger.info("Using MySQL database")

    # Parse URL to determine if it's MySQL
    is_mysql = "mysql" in url.lower()

    # Configure engine based on database type
    if is_mysql:
        # Production MySQL settings for cloud databases
        engine = create_engine(
            url,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_size=10,  # Increased pool size for production
            max_overflow=20,  # Allow overflow for peak loads
            echo=False,
            connect_args={
                "connect_timeout": 10,
                # MySQL-specific settings for utf8mb4
                "charset": "utf8mb4",
            }
        )
    else:
        # Fallback for non-MySQL databases (development/testing)
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10,
            echo=False,
            connect_args={"connect_timeout": 10}
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
        logger.info("Database connection established successfully: MySQL")
    except Exception as e:
        logger.warning(f"Database connection check warning: {e}")

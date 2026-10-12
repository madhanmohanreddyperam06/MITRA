"""Script to create the initial administrator for MITRA using environment variables.

This script creates the first administrator account using environment variables.
It should only be run once during initial setup.

Usage:
    ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=securepass python scripts/create_admin_env.py

Environment Variables:
    ADMIN_USERNAME: Administrator username (required)
    ADMIN_EMAIL: Administrator email (required)
    ADMIN_PASSWORD: Administrator password (required)
    ADMIN_FULL_NAME: Administrator full name (optional)
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.database.connection import engine
from app.database.repositories.users import UserRepository
from app.services.auth_service import AuthService
from app.core.logging import logger


def create_admin():
    """Create the initial administrator account from environment variables."""
    print("=" * 60)
    print("MITRA Administrator Setup (Environment Variables)")
    print("=" * 60)
    print()

    # Get admin details from environment variables
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    full_name = os.getenv("ADMIN_FULL_NAME")

    # Validate required fields
    if not username:
        print("[ERROR] ADMIN_USERNAME environment variable is required")
        return False

    if not email:
        print("[ERROR] ADMIN_EMAIL environment variable is required")
        return False

    if not password:
        print("[ERROR] ADMIN_PASSWORD environment variable is required")
        return False

    # Validate email format (basic)
    if '@' not in email or '.' not in email:
        print("[ERROR] Invalid email format")
        return False

    # Create database session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)

        # Check if admin already exists
        print("Checking existing administrator...")
        admin_count = user_repo.count_admins()

        if admin_count > 0:
            print(f"\n[ERROR] Administrator already exists ({admin_count} admin(s) found).")
            print("No changes made.")
            print("If you need to reset the administrator, please contact support.")
            return False

        print("No administrator exists. Proceeding with creation.\n")

        # Begin transaction for atomic admin creation
        try:
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Full Name: {full_name or 'Not set'}")
            print()
            print("-" * 60)
            print("Creating administrator account...")

            # Double-check admin count before creation (within transaction)
            admin_count = user_repo.count_admins()
            if admin_count > 0:
                db.rollback()
                print(f"\n[ERROR] Administrator created by another process.")
                print("No changes made.")
                return False

            admin = auth_service.create_admin_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name
            )

            # Commit transaction
            db.commit()

            print()
            print("=" * 60)
            print("[SUCCESS] Administrator created successfully!")
            print("=" * 60)
            print(f"Username: {admin['username']}")
            print(f"Email: {admin['email']}")
            print(f"Full Name: {admin['full_name'] or 'Not set'}")
            print()
            print("IMPORTANT: Your password has been securely hashed.")
            print("Please remember your password. It cannot be recovered.")
            print()
            print("You can now login to the application using these credentials.")
            print("=" * 60)

            return True

        except Exception as e:
            db.rollback()
            print()
            print(f"[ERROR] Failed to create administrator: {e}")
            return False

    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = create_admin()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)

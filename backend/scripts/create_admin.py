"""Script to create the initial administrator for MITRA.

This script creates the first administrator account.
It should only be run once during initial setup.

Usage:
    python scripts/create_admin.py

The script will:
1. Check if an admin already exists
2. If admin exists, refuse to create another
3. If no admin exists, prompt for admin details
4. Create the admin account securely
"""
import sys
import os
import getpass

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.database.connection import engine
from app.database.repositories.users import UserRepository
from app.services.auth_service import AuthService
from app.core.logging import logger


def create_admin():
    """Create the initial administrator account."""
    print("=" * 60)
    print("MITRA Administrator Setup")
    print("=" * 60)
    print()

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
            # Prompt for admin details
            print("Please enter administrator details:")
            print("-" * 60)

            username = input("Admin username: ").strip()
            if not username:
                print("[ERROR] Username cannot be empty")
                return False

            email = input("Admin email: ").strip().lower()
            if not email:
                print("[ERROR] Email cannot be empty")
                return False

            # Validate email format (basic)
            if '@' not in email or '.' not in email:
                print("[ERROR] Invalid email format")
                return False

            password = getpass.getpass("Admin password: ")
            if not password:
                print("[ERROR] Password cannot be empty")
                return False

            password_confirm = getpass.getpass("Confirm password: ")
            if password != password_confirm:
                print("[ERROR] Passwords do not match")
                return False

            full_name = input("Admin full name (optional): ").strip() or None

            print()
            print("-" * 60)
            print("Creating administrator account...")

            # Double-check admin count before creation (within transaction)
            # This reduces race condition window, though proper fix requires DB constraint
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

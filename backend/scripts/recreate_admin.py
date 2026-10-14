"""Delete and recreate admin user with correct password."""
import os
import sys
from sqlalchemy import create_engine, text
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set in environment")
    sys.exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    with engine.connect() as conn:
        # Delete existing admin user
        print("\nDeleting existing admin user...")
        result = conn.execute(text("""
            DELETE FROM users WHERE username = 'admin';
        """))
        conn.commit()
        print(f"Deleted {result.rowcount} row(s)")
        
        # Recreate admin with new password
        new_password = "admin123"
        password_hash = pwd_context.hash(new_password)
        
        print(f"\nCreating new admin user...")
        print(f"Password: {new_password}")
        print(f"Hash: {password_hash[:30]}...")
        
        result = conn.execute(text("""
            INSERT INTO users (username, email, password_hash, full_name, is_active, is_admin, created_at, updated_at)
            VALUES ('admin', 'admin@mitra.com', :password_hash, 'MITRA ADMINISTRATOR', true, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """), {"password_hash": password_hash})
        
        conn.commit()
        print(f"\nSUCCESS: Admin user recreated!")
        print(f"Rows affected: {result.rowcount}")
        
        # Verify
        result = conn.execute(text("""
            SELECT id, username, email, is_active, is_admin
            FROM users
            WHERE username = 'admin';
        """))
        admin = result.fetchone()
        
        if admin:
            print(f"\nVerified admin user:")
            print(f"  ID: {admin[0]}")
            print(f"  Username: {admin[1]}")
            print(f"  Email: {admin[2]}")
            print(f"  Active: {admin[3]}")
            print(f"  Admin: {admin[4]}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAdmin recreation complete.")

"""Reset admin password in database."""
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
        # Get new password from environment or use default
        new_password = os.getenv("ADMIN_PASSWORD", "adminmitra@123")
        
        # Hash the new password
        password_hash = pwd_context.hash(new_password)
        
        print(f"\nResetting admin password...")
        print(f"New password: {new_password}")
        print(f"New hash: {password_hash[:30]}...")
        
        # Update the admin user's password
        result = conn.execute(text("""
            UPDATE users
            SET password_hash = :password_hash,
                updated_at = CURRENT_TIMESTAMP
            WHERE username = 'admin';
        """), {"password_hash": password_hash})
        
        conn.commit()
        
        print(f"\nSUCCESS: Admin password has been reset!")
        print(f"Rows affected: {result.rowcount}")
        
        # Verify the update
        result = conn.execute(text("""
            SELECT username, email, is_active, is_admin
            FROM users
            WHERE username = 'admin';
        """))
        admin = result.fetchone()
        
        if admin:
            print(f"\nVerified admin user:")
            print(f"  Username: {admin[0]}")
            print(f"  Email: {admin[1]}")
            print(f"  Active: {admin[2]}")
            print(f"  Admin: {admin[3]}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nPassword reset complete.")

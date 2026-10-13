"""Test login functionality directly."""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
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
SessionLocal = sessionmaker(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    session = SessionLocal()
    
    # Get admin user with password hash
    result = session.execute(text("""
        SELECT id, username, email, password_hash, is_active, is_admin
        FROM users
        WHERE username = 'admin' OR email = 'admin@mitra.com';
    """))
    admin_user = result.fetchone()
    
    if admin_user:
        print(f"\nAdmin user found:")
        print(f"  ID: {admin_user[0]}")
        print(f"  Username: {admin_user[1]}")
        print(f"  Email: {admin_user[2]}")
        print(f"  Password Hash: {admin_user[3][:20]}...")
        print(f"  Active: {admin_user[4]}")
        print(f"  Admin: {admin_user[5]}")
        
        # Test password verification
        test_password = "adminmitra@123"
        password_hash = admin_user[3]
        
        print(f"\nTesting password: '{test_password}'")
        is_valid = pwd_context.verify(test_password, password_hash)
        print(f"Password verification result: {is_valid}")
        
        if not is_valid:
            print("\nERROR: Password verification failed!")
            print("The admin user's password hash does not match 'adminmitra@123'")
            print("You may need to recreate the admin user with the correct password.")
        else:
            print("\nSUCCESS: Password verification passed!")
    else:
        print("\nERROR: Admin user not found!")
    
    session.close()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTest complete.")

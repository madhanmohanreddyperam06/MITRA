"""Check if admin user exists in database."""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set in environment")
    sys.exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check if users table exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'users'
            );
        """))
        table_exists = result.scalar()
        print(f"Users table exists: {table_exists}")

        if table_exists:
            # Check if admin user exists
            result = conn.execute(text("""
                SELECT id, username, email, is_active, is_admin
                FROM users
                WHERE username = 'admin' OR email = 'admin@mitra.com';
            """))
            admin_users = result.fetchall()

            if admin_users:
                print(f"\nFound {len(admin_users)} admin user(s):")
                for user in admin_users:
                    print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Active: {user[3]}, Admin: {user[4]}")
            else:
                print("\nNo admin user found in database!")
                print("All users in database:")
                result = conn.execute(text("SELECT id, username, email, is_active, is_admin FROM users;"))
                users = result.fetchall()
                if users:
                    for user in users:
                        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Active: {user[3]}, Admin: {user[4]}")
                else:
                    print("  No users found at all!")
        else:
            print("ERROR: Users table does not exist!")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

print("\nDatabase check complete.")

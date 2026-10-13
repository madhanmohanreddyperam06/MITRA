"""Test JWT token generation and validation."""
import os
import sys
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")
print(f"JWT_ALGORITHM: {JWT_ALGORITHM}")

# Create a test token
user_id = 1
to_encode = {"sub": str(user_id)}
expire = datetime.utcnow() + timedelta(minutes=30)
to_encode.update({"exp": expire})

try:
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print(f"\nGenerated token: {token[:50]}...")
    
    # Decode the token
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    print(f"Decoded token: {decoded}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

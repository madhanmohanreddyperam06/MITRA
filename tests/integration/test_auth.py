"""Integration tests for authentication API endpoints."""
import sys
import pytest
import os
from fastapi.testclient import TestClient

# Import after path setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from app.main import app
from app.database.models import Base, User
from sqlalchemy.orm import sessionmaker
from app.database.connection import get_db
from app.services.auth_service import AuthService
from app.database.repositories.users import UserRepository


@pytest.fixture(scope="function")
def auth_client(test_engine):
    """Create a FastAPI test client with test database for auth tests."""
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def auth_client_with_admin(test_engine):
    """Create a test client with an admin user already created."""
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    admin = auth_service.create_admin_user(
        username="admin",
        email="admin@example.com",
        password="AdminPassword123!",
        full_name="Administrator"
    )
    db.close()

    client = TestClient(app)
    yield client, admin

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def auth_client_with_user(test_engine):
    """Create a test client with a regular user already created."""
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    user = auth_service.register_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        full_name="Test User"
    )
    db.close()

    client = TestClient(app)
    yield client, user

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.mark.integration
def test_register_success(auth_client):
    """Test successful user registration."""
    response = auth_client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert data["is_active"] is True
    assert data["is_admin"] is False
    assert "password_hash" not in data


@pytest.mark.integration
def test_register_duplicate_email(auth_client):
    """Test registration with duplicate email fails."""
    # Register first user
    auth_client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Try to register with same email
    response = auth_client.post(
        "/api/auth/register",
        json={
            "username": "user2",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.integration
def test_register_duplicate_username(auth_client):
    """Test registration with duplicate username fails."""
    # Register first user
    auth_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "user1@example.com",
            "password": "TestPassword123!"
        }
    )

    # Try to register with same username
    response = auth_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "user2@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


@pytest.mark.integration
def test_register_weak_password(auth_client):
    """Test registration with weak password fails."""
    response = auth_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "short"
        }
    )
    assert response.status_code in (400, 422)


@pytest.mark.integration
def test_register_never_creates_admin(auth_client):
    """Test that public registration never creates admin."""
    response = auth_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["is_admin"] is False


@pytest.mark.integration
def test_login_success(auth_client_with_user):
    """Test successful login."""
    client, user = auth_client_with_user

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
def test_login_with_email(auth_client_with_user):
    """Test login with email instead of username."""
    client, user = auth_client_with_user

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.integration
def test_login_invalid_password(auth_client_with_user):
    """Test login with invalid password fails."""
    client, user = auth_client_with_user

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_login_unknown_user(auth_client):
    """Test login with unknown user fails."""
    response = auth_client.post(
        "/api/auth/login",
        json={
            "username_or_email": "unknown",
            "password": "password"
        }
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user(auth_client_with_user):
    """Test getting current user info with valid token."""
    client, user = auth_client_with_user

    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password_hash" not in data


@pytest.mark.integration
def test_get_current_user_no_token(auth_client):
    """Test getting current user without token fails."""
    response = auth_client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user_invalid_token(auth_client):
    """Test getting current user with invalid token fails."""
    response = auth_client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user_missing_bearer(auth_client):
    """Test getting current user with malformed auth header fails."""
    response = auth_client.get(
        "/api/auth/me",
        headers={"Authorization": "invalid_token"}
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_list_users_as_admin(auth_client_with_admin):
    """Test admin can list users."""
    client, admin = auth_client_with_admin

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # List users
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Only admin


@pytest.mark.integration
def test_list_users_as_normal_user(auth_client_with_user):
    """Test normal user cannot list users."""
    client, user = auth_client_with_user

    # Login as normal user
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Try to list users
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


@pytest.mark.integration
def test_list_users_unauthenticated(auth_client):
    """Test unauthenticated user cannot list users."""
    response = auth_client.get("/api/users")
    assert response.status_code == 401


@pytest.mark.integration
def test_get_user_as_admin(auth_client_with_admin):
    """Test admin can get specific user."""
    client, admin = auth_client_with_admin

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Get admin user
    response = client.get(
        f"/api/users/{admin['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin["id"]
    assert "password_hash" not in data


@pytest.mark.integration
def test_deactivate_user_as_admin(auth_client_with_admin):
    """Test admin can deactivate user."""
    client, admin = auth_client_with_admin

    # Create a regular user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Deactivate user (assuming user ID is 2)
    response = client.patch(
        "/api/users/2/status",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


@pytest.mark.integration
def test_deactivate_only_admin_prevented(auth_client_with_admin):
    """Test that deactivating the only admin is prevented."""
    client, admin = auth_client_with_admin

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Try to deactivate self (only admin)
    response = client.patch(
        f"/api/users/{admin['id']}/status",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "Cannot deactivate the only administrator" in response.json()["detail"]


@pytest.mark.integration
def test_delete_user_as_admin(auth_client_with_admin):
    """Test admin can delete user."""
    client, admin = auth_client_with_admin

    # Create a regular user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Delete user (assuming user ID is 2)
    response = client.delete(
        "/api/users/2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204


@pytest.mark.integration
def test_delete_only_admin_prevented(auth_client_with_admin):
    """Test that deleting the only admin is prevented."""
    client, admin = auth_client_with_admin

    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Try to delete self (only admin)
    response = client.delete(
        f"/api/users/{admin['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "Cannot delete the only administrator" in response.json()["detail"]


@pytest.mark.integration
def test_chat_endpoint_allows_guest(auth_client):
    """Test that chat endpoint works for guest (unauthenticated) users."""
    response = auth_client.post(
        "/chat",
        json={
            "user_input": "Tell me about admissions",
            "user_context": {},
            "conversation_history": []
        }
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_chat_endpoint_with_auth(auth_client_with_user):
    """Test that chat endpoint works with authentication."""
    client, user = auth_client_with_user

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Chat with auth
    response = client.post(
        "/chat",
        json={
            "user_input": "Tell me about admissions",
            "user_context": {},
            "conversation_history": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


@pytest.mark.integration
def test_qa_get_requires_auth(auth_client):
    """Test that QA get endpoint requires authentication."""
    response = auth_client.get("/qa")
    assert response.status_code == 401


@pytest.mark.integration
def test_qa_add_requires_auth(auth_client):
    """Test that QA add endpoint requires authentication."""
    response = auth_client.post(
        "/qa",
        json={
            "question": "Test question",
            "answer": "Test answer"
        }
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_qa_with_auth(auth_client_with_user):
    """Test that QA endpoints work with authentication."""
    client, user = auth_client_with_user

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    token = login_response.json()["access_token"]

    # Add QA with auth
    response = client.post(
        "/qa",
        json={
            "question": "Test question",
            "answer": "Test answer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Get QA with auth
    response = client.get(
        "/qa",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_inactive_user_cannot_authenticate(auth_client_with_user, test_engine):
    """Test that inactive user cannot authenticate."""
    client, user = auth_client_with_user

    # Deactivate user via direct DB manipulation
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    user_model = db.query(User).filter(User.id == user["id"]).first()
    user_model.is_active = False
    db.commit()
    db.close()

    # Try to login
    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 401


@pytest.mark.integration
def test_password_hash_never_in_response(auth_client_with_user, test_engine):
    """Security test: password hash should never appear in API responses."""
    client, user = auth_client_with_user

    # Register response
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "TestPassword123!"
        }
    )
    assert "password_hash" not in register_response.json()

    # Login response
    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }
    )
    assert "password_hash" not in login_response.json()

    # /me response
    token = login_response.json()["access_token"]
    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert "password_hash" not in me_response.json()

    # List users response (admin)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    admin = auth_service.create_admin_user(
        username="admin",
        email="admin@example.com",
        password="AdminPassword123!"
    )
    db.close()

    admin_login = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "AdminPassword123!"
        }
    )
    admin_token = admin_login.json()["access_token"]

    users_response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    for user_data in users_response.json():
        assert "password_hash" not in user_data

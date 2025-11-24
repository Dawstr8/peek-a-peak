from uuid import UUID

import pytest
from httpx import AsyncClient

BASE_URL = "/api/auth"
REGISTER_ENDPOINT = f"{BASE_URL}/register"
ME_ENDPOINT = f"{BASE_URL}/me"
LOGIN_ENDPOINT = f"{BASE_URL}/login"
LOGOUT_ENDPOINT = f"{BASE_URL}/logout"


@pytest.mark.asyncio
async def test_register_user_success(client_with_db: AsyncClient):
    """Test registering a new user successfully"""
    response = await client_with_db.post(
        REGISTER_ENDPOINT,
        json={"email": "user1@example.com", "username": "user1", "password": "pass123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(
    client_with_db: AsyncClient, registered_user
):
    """Test registering a user with a duplicate email"""
    response = await client_with_db.post(
        REGISTER_ENDPOINT,
        json={
            "email": registered_user["email"],
            "username": "user2_new",
            "password": "pass456",
        },
    )

    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_user_duplicate_username(
    client_with_db: AsyncClient, registered_user
):
    """Test registering a user with a duplicate username"""
    response = await client_with_db.post(
        REGISTER_ENDPOINT,
        json={
            "email": "other@example.com",
            "username": registered_user["username"],
            "password": "pass456",
        },
    )

    assert response.status_code == 400
    assert "Username is already taken" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_user_invalid_email(client_with_db: AsyncClient):
    """Test registering a user with invalid email format"""
    response = await client_with_db.post(
        REGISTER_ENDPOINT,
        json={"email": "invalid-email", "username": "user1", "password": "pass123"},
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("email" in str(error) for error in data["detail"])


@pytest.mark.asyncio
async def test_register_user_invalid_username(client_with_db: AsyncClient):
    """Test registering a user with invalid username format"""
    response = await client_with_db.post(
        REGISTER_ENDPOINT,
        json={
            "email": "valid@example.com",
            "username": "invalid@username",
            "password": "pass123",
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("username" in str(error) for error in data["detail"])


@pytest.mark.asyncio
async def test_read_me_success(client_with_db: AsyncClient, logged_in_user):
    """Test getting current user info with valid session"""
    response = await client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == logged_in_user["email"]
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_read_me_no_session(client_with_db: AsyncClient):
    """Test accessing me endpoint without session cookie"""
    response = await client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Not authenticated" in data["detail"]


@pytest.mark.asyncio
async def test_read_me_invalid_session(client_with_db: AsyncClient):
    """Test accessing me endpoint with invalid session"""
    client_with_db.cookies.set(
        "session_id", str(UUID("12345678-1234-5678-1234-567812345678"))
    )

    response = await client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Invalid or expired session" in data["detail"]


@pytest.mark.asyncio
async def test_login_with_session_success_with_email(
    client_with_db: AsyncClient, registered_user
):
    """Test successful login and session creation using email"""
    response = await client_with_db.post(
        LOGIN_ENDPOINT,
        data={
            "emailOrUsername": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    assert "session_id" in response.cookies
    assert response.cookies.get("session_id") is not None


@pytest.mark.asyncio
async def test_login_with_session_success_with_username(
    client_with_db: AsyncClient, registered_user
):
    """Test successful login and session creation using username"""
    response = await client_with_db.post(
        LOGIN_ENDPOINT,
        data={
            "emailOrUsername": registered_user["username"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    assert "session_id" in response.cookies
    assert response.cookies.get("session_id") is not None


@pytest.mark.asyncio
async def test_login_with_session_invalid_credentials(client_with_db: AsyncClient):
    """Test login with invalid credentials"""
    response = await client_with_db.post(
        LOGIN_ENDPOINT,
        data={"emailOrUsername": "nonexistent@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"]


@pytest.mark.asyncio
async def test_logout_success(client_with_db: AsyncClient, logged_in_user):
    """Test successful logout and session invalidation"""
    before_logout_me_response = await client_with_db.get(ME_ENDPOINT)

    response = await client_with_db.post(LOGOUT_ENDPOINT)

    after_logout_me_response = await client_with_db.get(ME_ENDPOINT)
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
    assert "session_id" not in response.cookies
    assert before_logout_me_response.status_code == 200
    assert after_logout_me_response.status_code == 401

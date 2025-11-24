from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def registered_users(client_with_db):
    """Creates and returns a list of registered users for testing"""
    users_data = [
        {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": f"password{i} ",
        }
        for i in range(1, 3)
    ]

    for user_data in users_data:
        await client_with_db.post("/api/auth/register", json=user_data)

    return users_data


@pytest.fixture
def registered_user(registered_users):
    """Creates and returns a registered user for testing"""
    return registered_users[0]


@pytest_asyncio.fixture
async def logged_in_user(client_with_db, registered_user):
    """Creates and returns a logged-in user with active session for testing"""
    email = registered_user["email"]
    username = registered_user["username"]
    password = registered_user["password"]

    await client_with_db.post(
        "/api/auth/login",
        data={"emailOrUsername": email, "password": password},
    )

    return {
        "email": email,
        "username": username,
        "password": password,
    }


@asynccontextmanager
async def temporary_login(client: AsyncClient, email_or_username: str, password: str):
    """
    Context manager that logs in a user, yields control, then logs out.

    Usage:
        async with temporary_login(client, registered_users[0]):
            # Your code here - user is logged in
            response = await client.post("/api/photos", ...)
        # User is automatically logged out after the block

    Args:
        client: The test client instance
        email_or_username: The email or username of the user to log in
        password: The password of the user to log in
    """
    await client.post(
        "/api/auth/login",
        data={
            "emailOrUsername": email_or_username,
            "password": password,
        },
    )

    try:
        yield client
    finally:
        await client.post("/api/auth/logout")

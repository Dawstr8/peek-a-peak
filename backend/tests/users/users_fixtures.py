"""
User fixtures for testing across different test types: unit, integration, and e2e
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.users.models import User
from src.users.repository import UsersRepository


@pytest.fixture
def mock_user() -> User:
    """
    Returns a mock User object for unit tests.
    This user is not persisted anywhere and is useful for pure unit tests
    that don't need database interaction.
    """
    return User(
        id=1,
        email="test@example.com",
        username="user",
        username_display="User",
        hashed_password="hashed_correct_password",
    )


@pytest.fixture
def mock_users_repository(mock_user: User):
    """
    Returns a mock UsersRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.

    Usage:
        # Repository will return mock_user only for "test@example.com"
        repo.get_by_email.side_effect = lambda email: mock_user if email == "test@example.com" else None

        # Repository will return mock_user only for ID 1
        repo.get_by_id.side_effect = lambda id: mock_user if id == 1 else None
    """
    repo = MagicMock(spec=UsersRepository)

    async def save(user):
        user.id = 1
        return user

    async def update(user_id, user_update):
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(mock_user, field, value)

        return mock_user

    async def get_by_email(email):
        return mock_user if email == mock_user.email else None

    async def get_by_id(user_id):
        return mock_user if user_id == mock_user.id else None

    async def get_by_username(username):
        return mock_user if username == mock_user.username else None

    repo.save = AsyncMock(side_effect=save)
    repo.update = AsyncMock(side_effect=update)
    repo.get_by_email = AsyncMock(side_effect=get_by_email)
    repo.get_by_id = AsyncMock(side_effect=get_by_id)
    repo.get_by_username = AsyncMock(side_effect=get_by_username)

    return repo


@pytest_asyncio.fixture
async def db_users(test_db) -> list[User]:
    """
    Creates and returns multiple real users in the test database.
    This fixture is useful for integration tests that need
    multiple real users in the database.
    """
    users_repo = UsersRepository(test_db)

    users = [
        User(
            email=f"user{i}@example.com",
            username=f"user{i}",
            username_display=f"User{i}",
            hashed_password=f"hashed_password{i}",
        )
        for i in range(1, 3)
    ]

    saved_users = []
    for user in users:
        saved_user = await users_repo.save(user)
        saved_users.append(saved_user)

    return saved_users


@pytest.fixture
def db_user(db_users) -> User:
    """
    Creates and returns a real user in the test database.
    This fixture is useful for integration tests that need
    a real user in the database.
    """
    return db_users[0]

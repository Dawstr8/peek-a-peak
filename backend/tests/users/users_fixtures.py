"""
User fixtures for testing across different test types: unit, integration, and e2e
"""

from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from src.users.models import User
from src.users.repository import UsersRepository
from tests.users.mock_repository import MockUsersRepository


@pytest.fixture
def users() -> list[User]:
    """Returns a list of User models for unit tests."""
    return [
        User(
            email=f"user{i}@example.com",
            username=f"user{i}",
            username_display=f"User{i}",
            hashed_password=f"hashed_correct_password{i}",
        )
        for i in range(1, 3)
    ]


@pytest.fixture
def mock_user(users) -> User:
    """
    Returns a mock User object for unit tests.
    This user is not persisted anywhere and is useful for pure unit tests
    that don't need database interaction.
    """
    users[0].id = uuid4()
    return users[0]


@pytest.fixture
def mock_users_repository(mock_user: User) -> UsersRepository:
    """
    Returns a mock UsersRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    return MockUsersRepository(items=[mock_user]).mock


@pytest_asyncio.fixture
async def db_user(test_db, users) -> User:
    """
    Creates and returns a real user in the test database.
    This fixture is useful for integration tests that need
    a real user in the database.
    """
    users_repo = UsersRepository(test_db)
    return await users_repo.save(users[0])

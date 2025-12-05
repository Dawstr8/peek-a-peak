"""
User fixtures for testing across different test types: unit, integration, and e2e
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.common.exceptions import NotFoundException
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
    """
    repo = MagicMock(spec=UsersRepository)

    async def save(user):
        user.id = 1
        return user

    async def update(user_id, user_update):
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(mock_user, field, value)

        return mock_user

    async def get_by_id(user_id):
        if user_id != mock_user.id:
            raise NotFoundException(f"User with id {user_id} not found.")

        return mock_user

    async def get_by_field(field, value):
        if value != getattr(mock_user, field):
            raise NotFoundException(f"User with {field}={value} not found.")

        return mock_user

    repo.save = AsyncMock(side_effect=save)
    repo.update = AsyncMock(side_effect=update)
    repo.get_by_id = AsyncMock(side_effect=get_by_id)
    repo.get_by_field = AsyncMock(side_effect=get_by_field)

    return repo


@pytest_asyncio.fixture
async def db_users(test_db) -> list[User]:
    """
    Creates and returns multiple real users in the test database.
    This fixture is useful for integration tests that need
    multiple real users in the database.
    """
    users_repo = UsersRepository(test_db)

    return await users_repo.save_all(
        [
            User(
                email=f"user{i}@example.com",
                username=f"user{i}",
                username_display=f"User{i}",
                hashed_password=f"hashed_password{i}",
            )
            for i in range(1, 3)
        ]
    )


@pytest.fixture
def db_user(db_users) -> User:
    """
    Creates and returns a real user in the test database.
    This fixture is useful for integration tests that need
    a real user in the database.
    """
    return db_users[0]

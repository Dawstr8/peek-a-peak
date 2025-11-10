"""
User fixtures for testing across different test types: unit, integration, and e2e
"""

from unittest.mock import MagicMock

import pytest

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

    def save(user):
        user.id = 1
        return user

    def get_by_email(email):
        return mock_user if email == mock_user.email else None

    def get_by_id(user_id):
        return mock_user if user_id == mock_user.id else None

    def get_by_username(username):
        return mock_user if username == mock_user.username else None

    repo.save.side_effect = save
    repo.get_by_email.side_effect = get_by_email
    repo.get_by_id.side_effect = get_by_id
    repo.get_by_username.side_effect = get_by_username

    return repo


@pytest.fixture
def db_users(test_db) -> list[User]:
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
            hashed_password=f"hashed_password{i}",
        )
        for i in range(1, 3)
    ]

    return [users_repo.save(user) for user in users]


@pytest.fixture
def db_user(db_users) -> User:
    """
    Creates and returns a real user in the test database.
    This fixture is useful for integration tests that need
    a real user in the database.
    """
    return db_users[0]

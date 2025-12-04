import copy

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.models import User, UserUpdate
from src.users.repository import UsersRepository
from tests.database.mixins import BaseRepositoryMixin


class TestUsersRepository(BaseRepositoryMixin):
    model_class = User
    sort_by = "username"

    @pytest.fixture
    def test_repository(self, test_db: AsyncSession) -> UsersRepository:
        return UsersRepository(test_db)

    @pytest.fixture()
    def db_items(self, db_users) -> list[User]:
        return db_users

    @pytest.fixture()
    def new_item(self) -> User:
        return User(
            email="new@example.com",
            username="newuser",
            username_display="New User",
            hashed_password="newhash",
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "field, error_message",
        [
            ("email", "Email is already in use."),
            ("username", "Username is already taken."),
        ],
    )
    async def test_save_unique_constraint_violation(
        self, test_repository, db_user, new_item, field, error_message
    ):
        setattr(new_item, field, getattr(db_user, field))

        with pytest.raises(ValueError, match=error_message):
            await test_repository.save(new_item)

    @pytest.mark.asyncio
    async def test_update_success(self, test_repository, db_user):
        """Test updating an existing user successfully and not overriding other fields."""
        original_user = copy.deepcopy(db_user)

        updated_user = await test_repository.update(
            db_user.id, UserUpdate(is_private=True)
        )

        assert updated_user.id == original_user.id
        assert updated_user.email == original_user.email
        assert updated_user.username == original_user.username
        assert updated_user.username_display == original_user.username_display

        assert original_user.is_private is False
        assert updated_user.is_private is True

    @pytest.mark.asyncio
    async def test_get_by_email_existing_user(self, test_repository, db_user):
        """Test getting an existing user by email."""
        retrieved_user = await test_repository.get_by_email(db_user.email)

        assert retrieved_user is not None
        assert retrieved_user.id == db_user.id
        assert retrieved_user.email == db_user.email

    @pytest.mark.asyncio
    async def test_get_by_email_non_existing_user(self, test_repository):
        """Test getting a non-existing user by email returns None."""
        retrieved_user = await test_repository.get_by_email("nonexistent@example.com")

        assert retrieved_user is None

    @pytest.mark.asyncio
    async def test_get_by_username_existing_user(self, test_repository, db_user):
        """Test getting an existing user by username."""
        retrieved_user = await test_repository.get_by_username(db_user.username)

        assert retrieved_user is not None
        assert retrieved_user.id == db_user.id
        assert retrieved_user.username == db_user.username

    @pytest.mark.asyncio
    async def test_get_by_username_non_existing_user(self, test_repository):
        """Test getting a non-existing user by username returns None."""
        retrieved_user = await test_repository.get_by_username("other_user")

        assert retrieved_user is None

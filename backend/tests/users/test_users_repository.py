import copy

import pytest

from src.users.models import User, UserUpdate
from src.users.repository import UsersRepository
from tests.database.mixins import BaseRepositoryMixin


class TestUsersRepository(BaseRepositoryMixin[User, UsersRepository]):
    repository_class = UsersRepository
    model_class = User
    sort_by = "username"

    items_fixture = "users"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "field, error_message",
        [
            ("email", "Email is already in use."),
            ("username", "Username is already taken."),
        ],
    )
    async def test_save_unique_constraint_violation(
        self, test_repository, items, field, error_message
    ):
        # Arrange
        db_user = await test_repository.save(items[0])
        new_user = items[1]
        setattr(new_user, field, getattr(db_user, field))

        # Act & Assert
        with pytest.raises(ValueError, match=error_message):
            await test_repository.save(new_user)

    @pytest.mark.asyncio
    async def test_update_success(self, test_repository, items):
        """Test updating an existing user successfully and not overriding other fields."""
        # Arrange
        db_user = await test_repository.save(items[0])
        original_user = copy.deepcopy(db_user)

        # Act
        updated_user = await test_repository.update(
            db_user.id, UserUpdate(is_private=True)
        )

        # Assert
        assert updated_user.id == original_user.id
        assert updated_user.email == original_user.email
        assert updated_user.username == original_user.username
        assert updated_user.username_display == original_user.username_display

        assert original_user.is_private is False
        assert updated_user.is_private is True

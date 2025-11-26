import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.models import User
from src.users.repository import UsersRepository


@pytest_asyncio.fixture
async def test_users_repository(test_db: AsyncSession) -> UsersRepository:
    """Create a UsersRepository instance for testing."""
    return UsersRepository(test_db)


@pytest.mark.asyncio
async def test_save_user_success(test_users_repository):
    """Test saving a new user successfully."""
    user = User(
        email="test@example.com",
        username="user",
        username_display="User",
        hashed_password="hash",
    )

    saved_user = await test_users_repository.save(user)

    assert saved_user.id is not None
    assert saved_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_save_user_duplicate_email(test_users_repository, db_user):
    """Test saving a user with a duplicate email raises ValueError."""
    username = "other_user"

    new_user = User(
        email=db_user.email,
        username=username,
        username_display=username,
        hashed_password="hash2",
    )

    with pytest.raises(ValueError) as exc:
        await test_users_repository.save(new_user)

    assert "Email is already in use" in str(exc.value)


@pytest.mark.asyncio
async def test_save_user_duplicate_username(test_users_repository, db_user):
    """Test saving a user with a duplicate username raises ValueError."""
    new_user = User(
        email="other@example.com",
        username=db_user.username,
        username_display=db_user.username_display,
        hashed_password="hash2",
    )

    with pytest.raises(ValueError) as exc:
        await test_users_repository.save(new_user)

    assert "Username is already taken" in str(exc.value)


@pytest.mark.asyncio
async def test_get_by_email_existing_user(test_users_repository, db_user):
    """Test getting an existing user by email."""
    retrieved_user = await test_users_repository.get_by_email(db_user.email)

    assert retrieved_user is not None
    assert retrieved_user.id == db_user.id
    assert retrieved_user.email == db_user.email


@pytest.mark.asyncio
async def test_get_by_email_non_existing_user(test_users_repository):
    """Test getting a non-existing user by email returns None."""
    retrieved_user = await test_users_repository.get_by_email("nonexistent@example.com")

    assert retrieved_user is None


@pytest.mark.asyncio
async def test_get_by_username_existing_user(test_users_repository, db_user):
    """Test getting an existing user by username."""
    retrieved_user = await test_users_repository.get_by_username(db_user.username)

    assert retrieved_user is not None
    assert retrieved_user.id == db_user.id
    assert retrieved_user.username == db_user.username


@pytest.mark.asyncio
async def test_get_by_username_non_existing_user(test_users_repository):
    """Test getting a non-existing user by username returns None."""
    retrieved_user = await test_users_repository.get_by_username("other_user")

    assert retrieved_user is None

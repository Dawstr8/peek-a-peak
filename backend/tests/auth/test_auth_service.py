from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.auth.exceptions import InvalidCredentialsException
from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.common.exceptions import NotFoundException
from src.sessions.repository import SessionsRepository
from src.users.models import UserCreate
from src.users.repository import UsersRepository


@pytest.fixture
def mock_sessions_repository():
    """Create a mock SessionsRepository"""
    return MagicMock(spec=SessionsRepository)


@pytest.fixture
def mock_password_service():
    """Create a mock PasswordService"""
    password_service = MagicMock()
    password_service.get_hash.side_effect = lambda pwd: f"hashed_{pwd}"
    password_service.verify.side_effect = (
        lambda plain, hashed: hashed == f"hashed_{plain}"
    )
    return password_service


@pytest.fixture
def service(
    mock_users_repository: UsersRepository,
    mock_sessions_repository: SessionsRepository,
    mock_password_service: PasswordService,
) -> AuthService:
    """Create an AuthService with mocked dependencies"""
    return AuthService(
        mock_users_repository,
        mock_sessions_repository,
        mock_password_service,
    )


@pytest.mark.asyncio
async def test_authenticate_user_not_found(service):
    """Test authentication when user is not found."""
    with pytest.raises(NotFoundException):
        await service.authenticate_user("nonexistent@example.com", "password")


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(service, mock_user):
    """Test authentication with wrong password."""
    with pytest.raises(InvalidCredentialsException):
        await service.authenticate_user(mock_user.email, "wrong_password")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email_or_username_fn,field_called_mock",
    [
        (lambda u: u.email, "email"),
        (lambda u: u.email.upper(), "email"),
        (lambda u: u.username, "username"),
        (lambda u: u.username.upper(), "username"),
    ],
)
async def test_authenticate_user_success(
    service,
    mock_user,
    mock_users_repository,
    email_or_username_fn,
    field_called_mock,
):
    """Test successful user authentication."""
    email_or_username = email_or_username_fn(mock_user)

    result = await service.authenticate_user(email_or_username, "correct_password")

    assert result == mock_user
    mock_users_repository.get_by_field.assert_called_once_with(
        field_called_mock, email_or_username.lower()
    )


@pytest.mark.asyncio
async def test_register_user(service):
    """Test registering a new user through the service"""
    user_create = UserCreate(
        email="Test@example.com", username="User", password="password123"
    )

    user = await service.register_user(user_create)

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.username == "user"
    assert user.username_display == "User"
    assert hasattr(user, "hashed_password")
    assert user.hashed_password != "password123"


@pytest.mark.asyncio
async def test_login_user_success(service, mock_sessions_repository, mock_user):
    """Test successful login and session creation."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    session = MagicMock()
    session.id = session_id
    mock_sessions_repository.create.return_value = session

    result = await service.login_user("test@example.com", "correct_password")

    assert result == session_id
    mock_sessions_repository.create.assert_called_once_with(
        mock_user.id, expires_in_days=30
    )


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(service):
    """Test login with invalid credentials raises ValueError."""

    with pytest.raises(InvalidCredentialsException) as exc:
        await service.login_user("nonexistent@example.com", "password")


@pytest.mark.asyncio
async def test_logout_user(service, mock_sessions_repository):
    """Test user logout invalidates the session."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")

    await service.logout_user(session_id)

    mock_sessions_repository.invalidate_by_id.assert_called_once_with(session_id)


@pytest.mark.asyncio
async def test_get_current_user_valid_session(
    service, mock_users_repository, mock_sessions_repository, mock_user
):
    """Test getting current user from valid session."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    user_id = mock_user.id

    session = MagicMock()
    session.user_id = user_id
    mock_sessions_repository.get_active_by_id.return_value = session

    result = await service.get_current_user(session_id)

    assert result == mock_user
    mock_sessions_repository.get_active_by_id.assert_called_once_with(session_id)
    mock_users_repository.get_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_current_user_invalid_session(service, mock_sessions_repository):
    """Test getting current user with invalid session raises ValueError."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    mock_sessions_repository.get_active_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc:
        await service.get_current_user(session_id)

    assert "Invalid or expired session" in str(exc.value)


@pytest.mark.asyncio
async def test_get_current_user_user_not_found(service, mock_sessions_repository):
    """Test getting current user when user is not found raises ValueError."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    user_id = 2

    session = MagicMock()
    session.user_id = user_id
    mock_sessions_repository.get_active_by_id.return_value = session

    with pytest.raises(NotFoundException) as exc:
        await service.get_current_user(session_id)

    assert "User not found" in str(exc.value)

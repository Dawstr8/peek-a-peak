import pytest

from src.authorization.exceptions import NotAuthorizedException
from src.authorization.service import AuthorizationService


@pytest.fixture
def mock_service() -> AuthorizationService:
    return AuthorizationService()


def test_ensure_user_is_owner_authorized(mock_service, mock_user):
    """Test ensure_user_is_owner when the user is authorized."""
    mock_service.ensure_user_is_owner(mock_user, mock_user.username)


def test_ensure_user_is_owner_not_authorized(mock_service, mock_user):
    """Test ensure_user_is_owner when the user is not authorized."""
    with pytest.raises(NotAuthorizedException):
        mock_service.ensure_user_is_owner(mock_user, "unauthorized_username")

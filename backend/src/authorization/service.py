from src.authorization.exceptions import NotAuthorizedException
from src.users.models import User


class AuthorizationService:
    @staticmethod
    def ensure_user_is_owner(current_user: User, username: str) -> None:
        if username != getattr(current_user, "username", None):
            raise NotAuthorizedException("Not authorized to access this resource")

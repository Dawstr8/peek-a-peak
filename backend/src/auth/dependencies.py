from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Path, status

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.database.core import db_dep
from src.sessions.repository import SessionsRepository
from src.users.dependencies import users_repository_dep
from src.users.models import User


def get_sessions_repository(db: db_dep) -> SessionsRepository:
    return SessionsRepository(db)


def get_password_service():
    return PasswordService()


def get_service(
    users_repository: users_repository_dep,
    sessions_repository: SessionsRepository = Depends(get_sessions_repository),
    password_service: PasswordService = Depends(get_password_service),
) -> AuthService:
    return AuthService(users_repository, sessions_repository, password_service)


auth_service_dep = Annotated[AuthService, Depends(get_service)]


async def get_current_user(
    auth_service: auth_service_dep,
    session_id: UUID = Cookie(None, alias="session_id"),
) -> User:
    """
    Provides the current authenticated user from session cookie.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        return await auth_service.get_current_user(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )


current_user_dep = Annotated[User, Depends(get_current_user)]


async def get_access_owner_id(
    current_user: current_user_dep,
    users_repository: users_repository_dep,
    username: str = Path(...),
) -> str:
    """
    Ensures the current user has access to the resource owned by the user with given username.

    Args:
        current_user: The current authenticated user
        username: The non-normalized username to check access for
        users_repository: The UsersRepository instance

    Returns:
        The user ID of the resource owner if access is granted.
    """
    username = username.lower()
    if username != current_user.username:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this resource"
        )

    resource_owner = await users_repository.get_by_username(username)
    if not resource_owner:
        raise HTTPException(status_code=404, detail="User not found")

    return resource_owner.id


get_access_owner_id_dep = Annotated[int, Depends(get_access_owner_id)]

__all__ = ["auth_service_dep", "current_user_dep", "get_access_owner_id_dep"]

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, status

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.common.exceptions import NotFoundException
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
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )


async def get_current_user_optional(
    auth_service: auth_service_dep,
    session_id: UUID = Cookie(None, alias="session_id"),
) -> User | None:
    """
    Provides the current authenticated user from session cookie, or None if not authenticated.
    """
    if not session_id:
        return None

    try:
        return await auth_service.get_current_user(session_id)
    except NotFoundException:
        return None


current_user_dep = Annotated[User, Depends(get_current_user)]
current_user_optional_dep = Annotated[User | None, Depends(get_current_user_optional)]


__all__ = ["auth_service_dep", "current_user_dep", "current_user_optional_dep"]

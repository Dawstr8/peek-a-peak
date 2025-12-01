from typing import Annotated

from fastapi import Depends, HTTPException, Path

from src.auth.dependencies import authenticated_user_dep
from src.authorization.exceptions import NotAuthorizedException
from src.authorization.service import AuthorizationService
from src.exceptions import NotFoundException
from src.users.dependencies import users_service_dep


def get_authorization_service() -> AuthorizationService:
    return AuthorizationService()


async def get_access_owner_id(
    current_user: authenticated_user_dep,
    users_service: users_service_dep,
    username: str = Path(...),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
) -> str:
    """Ensures the current user has access to the resource owned by the user with given username."""
    username = username.lower()

    try:
        authorization_service.ensure_user_is_owner(current_user, username)
        owner = await users_service.get_user_by_username(username)
        return owner.id
    except NotAuthorizedException or NotFoundException:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this resource"
        )


get_access_owner_id_dep = Annotated[int, Depends(get_access_owner_id)]

__all__ = ["get_access_owner_id_dep"]

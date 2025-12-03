from typing import Annotated

from fastapi import Depends, HTTPException, Path

from src.auth.dependencies import current_user_dep, current_user_optional_dep
from src.authorization.exceptions import NotAuthorizedException
from src.authorization.service import AuthorizationService
from src.common.exceptions import NotFoundException
from src.users.dependencies import users_service_dep


def get_authorization_service() -> AuthorizationService:
    return AuthorizationService()


async def authorize_owner_access(
    current_user: current_user_dep,
    users_service: users_service_dep,
    username: str = Path(...),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
) -> str:
    """Ensures the current user is the owner of the resource."""
    username = username.lower()

    try:
        owner = await users_service.get_user_by_username(username)
        authorization_service.ensure_user_is_owner(current_user, username)
        return owner.id
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotAuthorizedException:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this resource"
        )


async def authorize_private_access(
    users_service: users_service_dep,
    current_user: current_user_optional_dep,
    username: str = Path(...),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
) -> str:
    """Ensures the current user has access to potentially private resources (public access or owner access for private)."""
    username = username.lower()

    try:
        owner = await users_service.get_user_by_username(username)
        if not owner.is_private:
            return owner.id

        if current_user is None:
            raise HTTPException(
                status_code=403, detail="Not authorized to access this resource"
            )

        authorization_service.ensure_user_is_owner(current_user, username)
        return owner.id
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotAuthorizedException:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this resource"
        )


async def authorize_public_access(
    users_service: users_service_dep,
    username: str = Path(...),
) -> str:
    """Retrieves the user ID for public access (no authorization required)."""
    username = username.lower()

    try:
        owner = await users_service.get_user_by_username(username)
        return owner.id
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


authorize_owner_dep = Annotated[str, Depends(authorize_owner_access)]
authorize_private_dep = Annotated[str, Depends(authorize_private_access)]
authorize_public_dep = Annotated[str, Depends(authorize_public_access)]

__all__ = [
    "authorize_owner_dep",
    "authorize_private_dep",
    "authorize_public_dep",
]

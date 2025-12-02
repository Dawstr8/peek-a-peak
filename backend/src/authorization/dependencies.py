from typing import Annotated

from fastapi import Depends, HTTPException, Path

from src.auth.dependencies import current_user_dep, current_user_optional_dep
from src.authorization.exceptions import NotAuthorizedException
from src.authorization.service import AuthorizationService
from src.exceptions import NotFoundException
from src.users.dependencies import users_service_dep


def get_authorization_service() -> AuthorizationService:
    return AuthorizationService()


async def authorize_owner_access(
    current_user: current_user_dep,
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
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (NotAuthorizedException, NotFoundException):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this resource"
        )


async def authorize_read_access(
    users_service: users_service_dep,
    current_user: current_user_optional_dep,
    username: str = Path(...),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
) -> str:
    """Ensures the current user has read access to the resource owned by the user with given username."""
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


authorize_owner_access_dep = Annotated[int, Depends(authorize_owner_access)]
authorize_read_access_dep = Annotated[int, Depends(authorize_read_access)]

__all__ = ["authorize_owner_access_dep", "authorize_read_access_dep"]

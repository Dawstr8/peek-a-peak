from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.dependencies import peaks_repository_dep
from src.photos.dependencies import photos_repository_dep
from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_users_repository(db: db_dep) -> UsersRepository:
    return UsersRepository(db)


users_repository_dep = Annotated[UsersRepository, Depends(get_users_repository)]


def get_users_service(
    users_repository: users_repository_dep,
    photos_repository: photos_repository_dep,
    peaks_repository: peaks_repository_dep,
) -> UsersService:
    return UsersService(users_repository, photos_repository, peaks_repository)


users_service_dep = Annotated[UsersService, Depends(get_users_service)]

__all__ = ["users_repository_dep", "users_service_dep"]

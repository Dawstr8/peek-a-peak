from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.repository import PeaksRepository
from src.photos.repository import PhotosRepository
from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_users_repository(db: db_dep) -> UsersRepository:
    return UsersRepository(db)


def get_photos_repository(db: db_dep) -> PhotosRepository:
    return PhotosRepository(db)


def get_peaks_repository(db: db_dep) -> PeaksRepository:
    return PeaksRepository(db)


def get_users_service(
    users_repository: UsersRepository = Depends(get_users_repository),
    photos_repository: PhotosRepository = Depends(get_photos_repository),
    peaks_repository: PeaksRepository = Depends(get_peaks_repository),
) -> UsersService:
    return UsersService(users_repository, photos_repository, peaks_repository)


users_service_dep = Annotated[UsersService, Depends(get_users_service)]

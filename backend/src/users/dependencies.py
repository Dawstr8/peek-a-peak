from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.repository import PeaksRepository
from src.photos.repository import PhotosRepository
from src.users.service import UsersService


def get_photos_repository(db: db_dep) -> PhotosRepository:
    return PhotosRepository(db)


def get_peaks_repository(db: db_dep) -> PeaksRepository:
    return PeaksRepository(db)


def get_users_service(
    photos_repository: PhotosRepository = Depends(get_photos_repository),
    peaks_repository: PeaksRepository = Depends(get_peaks_repository),
) -> UsersService:
    return UsersService(photos_repository, peaks_repository)


users_service_dep = Annotated[UsersService, Depends(get_users_service)]

from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.photos.repository import PhotosRepository
from src.photos.service import PhotosService
from src.uploads.service import UploadsService
from src.uploads.services.local_storage import LocalFileStorage


def get_uploads_service() -> UploadsService:
    storage = LocalFileStorage()
    return UploadsService(storage)


def get_photos_repository(db: db_dep) -> PhotosRepository:
    return PhotosRepository(db)


photos_repository_dep = Annotated[PhotosRepository, Depends(get_photos_repository)]


def get_photos_service(
    photos_repository: photos_repository_dep,
    uploads_service: UploadsService = Depends(get_uploads_service),
) -> PhotosService:
    return PhotosService(uploads_service, photos_repository)


photos_service_dep = Annotated[PhotosService, Depends(get_photos_service)]

__all__ = ["photos_repository_dep", "photos_service_dep"]

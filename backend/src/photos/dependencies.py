from typing import Annotated

from fastapi import Depends

from config import settings
from src.database.core import db_dep
from src.photos.repository import PhotosRepository
from src.photos.service import PhotosService
from src.uploads.service import UploadsService
from src.uploads.services.local_storage import LocalFileStorage
from src.uploads.services.s3_storage import S3Storage
from src.weather.dependencies import weather_service_dep


def get_uploads_service() -> UploadsService:
    if settings.storage_type == "s3":
        storage = S3Storage(
            endpoint=settings.s3_endpoint,
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
            bucket_name=settings.s3_bucket_name,
            secure=settings.s3_secure,
        )
    else:
        storage = LocalFileStorage()

    return UploadsService(storage)


def get_photos_repository(db: db_dep) -> PhotosRepository:
    return PhotosRepository(db)


photos_repository_dep = Annotated[PhotosRepository, Depends(get_photos_repository)]


def get_photos_service(
    photos_repository: photos_repository_dep,
    weather_service: weather_service_dep,
    uploads_service: UploadsService = Depends(get_uploads_service),
) -> PhotosService:
    return PhotosService(uploads_service, photos_repository, weather_service)


photos_service_dep = Annotated[PhotosService, Depends(get_photos_service)]

__all__ = ["photos_repository_dep", "photos_service_dep"]

from typing import List, Optional

from fastapi import UploadFile

from src.photos.models import SummitPhoto, SummitPhotoCreate
from src.photos.repository import PhotosRepository
from src.uploads.service import UploadsService
from src.users.models import User
from src.users.repository import UsersRepository


class PhotosService:
    """
    Service for handling photo operations.
    """

    def __init__(
        self,
        uploads_service: UploadsService,
        photos_repository: PhotosRepository,
        users_repository: UsersRepository,
    ):
        """
        Initialize the PhotosService

        Args:
            uploads_service: Service for handling file uploads and storage
            photos_repository: Repository for database operations on photos
        """
        self.uploads_service = uploads_service
        self.photos_repository = photos_repository
        self.users_repository = users_repository

    async def upload_photo(
        self,
        file: UploadFile,
        summit_photo_create: SummitPhotoCreate,
        current_user: User,
    ) -> SummitPhoto:
        """
        Upload a photo file and store it in the database with the provided metadata.

        Args:
            file: The uploaded photo file
            summit_photo_create: Metadata for the photo (captured_at, lat, lng, alt, peak_id)

        Returns:
            SummitPhoto: The saved photo object with peak information
        """
        path = await self.uploads_service.save_file(file, content_type_prefix="image/")
        lat, lng = (
            summit_photo_create.lat,
            summit_photo_create.lng,
        )

        photo = SummitPhoto(
            file_name=path.split("/")[-1],
            owner_id=current_user.id,
            location=(
                f"POINT({lng} {lat})" if lat is not None and lng is not None else None
            ),
            **summit_photo_create.model_dump(),
        )

        saved_photo = await self.photos_repository.save(photo)

        return saved_photo

    async def get_photo_by_id(self, photo_id: int) -> Optional[SummitPhoto]:
        """
        Get a photo by its ID.

        Args:
            photo_id: ID of the photo to retrieve

        Returns:
            SummitPhoto with peak information if found, None otherwise
        """
        return await self.photos_repository.get_by_id(photo_id)

    async def get_all_photos(
        self, sort_by: Optional[str] = None, order: Optional[str] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos from the database, optionally sorted.

        Args:
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            List[SummitPhoto]: List of all photos with peak information
        """
        return await self.photos_repository.get_all(sort_by=sort_by, order=order)

    async def get_photos_by_user(
        self, username: str, sort_by: Optional[str] = None, order: Optional[str] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos uploaded by a specific user.

        Args:
            username: Username of the user whose photos to retrieve
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            List[SummitPhoto]: List of photos uploaded by the specified user with peak information
        """
        user = await self.users_repository.get_by_username(username)

        return await self.photos_repository.get_by_owner_id(
            user.id, sort_by=sort_by, order=order
        )

    async def delete_photo(self, photo_id: int) -> bool:
        """
        Delete a photo by ID (both file and database record)

        Args:
            photo_id: ID of the photo to delete

        Returns:
            bool: True if deletion was successful
        """
        photo = await self.photos_repository.get_by_id(photo_id)
        if not photo:
            return False

        file_deleted = await self.uploads_service.delete_file(photo.file_name)

        if file_deleted:
            db_deleted = await self.photos_repository.delete(photo_id)
            return db_deleted

        return False

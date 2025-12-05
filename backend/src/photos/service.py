from typing import List, Optional

from fastapi import UploadFile

from src.photos.models import SummitPhoto, SummitPhotoCreate
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from src.uploads.service import UploadsService
from src.users.models import User


class PhotosService:
    """
    Service for handling photo operations.
    """

    def __init__(
        self,
        uploads_service: UploadsService,
        photos_repository: PhotosRepository,
    ):
        self.uploads_service = uploads_service
        self.photos_repository = photos_repository

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

    async def get_photo_by_id(self, photo_id: int) -> SummitPhoto:
        """
        Retrieve a photo by its ID.

        Returns:
            SummitPhoto: The photo with the given ID

        Raises:
            NotFoundException: If no photo with the given ID exists
        """
        return await self.photos_repository.get_by_id(photo_id)

    async def get_all_photos(
        self, sort_params: Optional[SortParams] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos from the database, optionally sorted.

        Args:
            sort_params: Sorting parameters

        Returns:
            List[SummitPhoto]: List of all photos with peak information
        """
        return await self.photos_repository.get_all(sort_params=sort_params)

    async def delete_photo(self, photo_id: int) -> bool:
        """
        Delete a photo by ID (both file and database record)

        Args:
            photo_id: ID of the photo to delete

        Returns:
            bool: True if deletion was successful
        """
        photo = await self.get_photo_by_id(photo_id)
        file_deleted = await self.uploads_service.delete_file(photo.file_name)

        if file_deleted:
            await self.photos_repository.delete(photo)
            return True

        return False

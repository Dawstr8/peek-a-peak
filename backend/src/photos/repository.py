from typing import List, Optional

from sqlalchemy.orm import load_only
from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.pagination.models import PaginatedResponse, PaginationParams
from src.photos.models import SummitPhoto, SummitPhotoDate, SummitPhotoLocation
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting


class PhotosRepository(BaseRepository):
    """
    Repository for SummitPhoto data access operations.
    """

    async def save(self, photo: SummitPhoto) -> SummitPhoto:
        """
        Save a photo to the database.

        Args:
            photo: The SummitPhoto to save

        Returns:
            The saved SummitPhoto with database ID assigned
        """
        self.db.add(photo)
        await self.db.commit()
        await self.db.refresh(photo)
        return photo

    async def get_by_id(self, photo_id: int) -> Optional[SummitPhoto]:
        """
        Get a specific photo by ID.

        Args:
            photo_id: ID of the photo to retrieve

        Returns:
            SummitPhoto if found, None otherwise
        """
        return await self.db.get(SummitPhoto, photo_id)

    async def get_all(
        self, sort_params: Optional[SortParams] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos from the database, optionally sorted.

        Args:
            sort_params: Sorting parameters

        Returns:
            List of SummitPhoto objects
        """
        statement = select(SummitPhoto)
        statement = apply_sorting(statement, SummitPhoto, sort_params)
        result = await self.db.exec(statement)
        return result.all()

    async def get_by_owner_id(
        self,
        owner_id: int,
        sort_params: SortParams,
        pagination_params: PaginationParams,
    ) -> PaginatedResponse[SummitPhoto]:
        statement = select(SummitPhoto).where(SummitPhoto.owner_id == owner_id)
        statement = apply_sorting(statement, SummitPhoto, sort_params)
        return await self.paginator.paginate(statement, pagination_params)

    async def get_locations_by_owner_id(
        self, owner_id: int
    ) -> List[SummitPhotoLocation]:
        statement = (
            select(SummitPhoto)
            .where(SummitPhoto.owner_id == owner_id)
            .where(SummitPhoto.location != None)
            .options(load_only(SummitPhoto.id, SummitPhoto.location, SummitPhoto.alt))
        )
        result = await self.db.exec(statement)
        return result.all()

    async def get_dates_by_owner_id(self, owner_id: int) -> List[SummitPhotoDate]:
        statement = (
            select(SummitPhoto)
            .where(SummitPhoto.owner_id == owner_id)
            .options(load_only(SummitPhoto.id, SummitPhoto.captured_at))
        )
        result = await self.db.exec(statement)
        return result.all()

    async def delete(self, photo_id: int) -> bool:
        """
        Delete a photo by ID.

        Args:
            photo_id: ID of the photo to delete

        Returns:
            True if photo was deleted, False if not found
        """
        photo = await self.get_by_id(photo_id)
        if not photo:
            return False

        await self.db.delete(photo)
        await self.db.commit()
        return True

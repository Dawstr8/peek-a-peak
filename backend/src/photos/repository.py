from typing import List, Optional

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.photos.models import SummitPhoto


class PhotosRepository:
    """
    Repository for SummitPhoto data access operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the PhotosRepository.

        Args:
            db: Database session
        """
        self.db = db

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
        self, sort_by: Optional[str] = None, order: Optional[str] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos from the database, optionally sorted.

        Args:
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            List of SummitPhoto objects
        """
        statement = select(SummitPhoto)
        statement = self._apply_sorting(statement, sort_by, order)
        result = await self.db.exec(statement)
        return result.all()

    async def get_by_owner_id(
        self, owner_id: int, sort_by: Optional[str] = None, order: Optional[str] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos uploaded by a specific user.

        Args:
            user_id: ID of the user whose photos to retrieve
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            List of SummitPhoto objects uploaded by the specified user
        """
        statement = select(SummitPhoto).where(SummitPhoto.owner_id == owner_id)
        statement = self._apply_sorting(statement, sort_by, order)
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

    def _apply_sorting(
        self, statement, sort_by: Optional[str] = None, order: Optional[str] = None
    ):
        """
        Apply sorting to a query statement.

        Args:
            statement: The SQLModel select statement
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            Modified statement with sorting applied
        """
        if sort_by and hasattr(SummitPhoto, sort_by):
            column = getattr(SummitPhoto, sort_by)
            statement = (
                statement.order_by(desc(column))
                if order == "desc"
                else statement.order_by(column)
            )

        return statement

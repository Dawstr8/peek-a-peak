from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.peaks.models import Peak


class PeaksRepository:
    """
    Repository for Peak data access operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the PeaksRepository.

        Args:
            db: Database session
        """
        self.db = db

    async def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        query = select(Peak)
        result = await self.db.exec(query)
        return result.all()

    async def get_by_id(self, peak_id: int) -> Optional[Peak]:
        """
        Get a specific peak by ID.

        Args:
            peak_id: ID of the peak to retrieve

        Returns:
            Peak if found, None otherwise
        """
        return await self.db.get(Peak, peak_id)

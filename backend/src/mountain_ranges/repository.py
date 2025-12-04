from typing import Optional

from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.mountain_ranges.models import MountainRange


class MountainRangesRepository(BaseRepository[MountainRange]):
    model = MountainRange

    async def get_by_name(self, mountain_range_name: str) -> Optional[MountainRange]:
        statement = select(MountainRange).where(
            MountainRange.name == mountain_range_name
        )
        result = await self.db.exec(statement)
        return result.first()

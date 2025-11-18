from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange


class MountainRangesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, mountain_range: MountainRange) -> MountainRange:
        self.db.add(mountain_range)
        await self.db.commit()
        await self.db.refresh(mountain_range)
        return mountain_range

    async def get_by_name(self, mountain_range_name: str) -> Optional[MountainRange]:
        statement = select(MountainRange).where(
            MountainRange.name == mountain_range_name
        )
        result = await self.db.exec(statement)
        return result.first()

from typing import Generic, Optional, Type, TypeVar

from sqlmodel.ext.asyncio.session import AsyncSession

from src.pagination.paginator import Paginator

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.paginator = Paginator(db)

    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.db.get(self.model, id)

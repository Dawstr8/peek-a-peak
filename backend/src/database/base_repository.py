from typing import Generic, Optional, Type, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.pagination.paginator import Paginator
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.paginator = Paginator(db)

    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.db.get(self.model, id)

    async def get_all(self, sort_params: Optional[SortParams] = None) -> list[T]:
        statement = select(self.model)
        if sort_params is not None:
            statement = apply_sorting(statement, self.model, sort_params)

        result = await self.db.exec(statement)
        return result.all()

    async def save(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

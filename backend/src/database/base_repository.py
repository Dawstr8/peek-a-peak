from typing import Generic, Optional, Type, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.common.exceptions import NotFoundException
from src.pagination.paginator import Paginator
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.paginator = Paginator(db)

    async def get_by_id(self, id: int) -> T:
        obj = await self.db.get(self.model, id)
        if obj is None:
            raise NotFoundException(f"{self.model.__name__} with id {id} not found.")

        return obj

    async def get_by_field(self, field: str, value) -> T:
        statement = select(self.model).where(getattr(self.model, field) == value)
        result = await self.db.exec(statement)
        obj = result.first()
        if obj is None:
            raise NotFoundException(
                f"{self.model.__name__} with {field}={value} not found."
            )

        return obj

    async def get_by_fields(self, filters: dict) -> T:
        statement = select(self.model)

        for field, value in filters.items():
            statement = statement.where(getattr(self.model, field) == value)

        result = await self.db.exec(statement)
        obj = result.first()
        if obj is None:
            filter_desc = ", ".join(f"{k}={v}" for k, v in filters.items())
            raise NotFoundException(
                f"{self.model.__name__} with {filter_desc} not found."
            )

        return obj

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

    async def save_all(self, objs: list[T]) -> None:
        self.db.add_all(objs)
        await self.db.commit()
        for obj in objs:
            await self.db.refresh(obj)

        return objs

    async def delete(self, obj: T) -> None:
        await self.db.delete(obj)
        await self.db.commit()

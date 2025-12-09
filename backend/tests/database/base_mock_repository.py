from typing import Any, Generic, Optional, Type, TypeVar
from unittest.mock import AsyncMock, MagicMock

from src.common.exceptions import NotFoundException
from src.sorting.models import SortParams

T = TypeVar("T")


class BaseMockRepository(Generic[T]):
    repository_class: Type
    model: Type[T]

    def __init__(self, items: list[T]) -> None:
        self.mock = MagicMock(spec=self.repository_class)
        self.items = items.copy()
        self.next_id = 1

        self._setup_base_methods()
        self._setup_custom_methods()

    def _add_method(self, name: str, func: Any) -> None:
        setattr(self.mock, name, AsyncMock(side_effect=func))

    def _setup_base_methods(self) -> None:
        async def get_by_id(id: int) -> T:
            for item in self.items:
                if hasattr(item, "id") and item.id == id:
                    return item

            raise NotFoundException(f"{self.model.__name__} with id {id} not found.")

        async def get_by_field(field: str, value: Any) -> T:
            for item in self.items:
                if hasattr(item, field) and getattr(item, field) == value:
                    return item

            raise NotFoundException(
                f"{self.model.__name__} with {field}={value} not found."
            )

        async def get_all(sort_params: Optional[SortParams] = None) -> list[T]:
            results = self.items.copy()

            if sort_params:
                reverse = sort_params.order == "desc"
                if hasattr(self.items[0] if self.items else None, sort_params.sort_by):
                    results = sorted(
                        results,
                        key=lambda x: getattr(x, sort_params.sort_by),
                        reverse=reverse,
                    )

            return results

        async def save(item: T) -> T:
            if hasattr(item, "id") and item.id is None:
                item.id = self.next_id
                self.next_id += 1

            for i, existing_item in enumerate(self.items):
                if hasattr(existing_item, "id") and existing_item.id == item.id:
                    self.items[i] = item
                    return item

            self.items.append(item)
            return item

        async def save_all(items: list[T]) -> list[T]:
            for item in items:
                await self.mock.save(item)

            return items

        async def delete(item: T) -> None:
            if item in self.items:
                self.items.remove(item)

            elif hasattr(item, "id"):
                self.items = [i for i in self.items if i.id != item.id]

        self._add_method("get_by_id", get_by_id)
        self._add_method("get_by_field", get_by_field)
        self._add_method("get_all", get_all)
        self._add_method("save", save)
        self._add_method("save_all", save_all)
        self._add_method("delete", delete)

    def _setup_custom_methods(self) -> None:
        pass

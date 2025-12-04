from typing import Type

import pytest

from src.database.base_repository import BaseRepository
from src.sorting.models import SortParams


class BaseRepositoryMixin:
    model_class: Type = None
    sort_by = "id"

    @pytest.fixture()
    def test_repository(self) -> BaseRepository:
        """Create an instance of the repository for testing"""
        pass

    @pytest.fixture()
    def db_items(self):
        """Retrieve test items from fixtures based on model_class"""
        pass

    @pytest.mark.asyncio
    async def test_base_get_by_id_not_found(self, test_repository):
        result_item = await test_repository.get_by_id(-1)

        assert result_item is None

    @pytest.mark.asyncio
    async def test_base_get_by_id_found(self, test_repository, db_items):
        db_item = db_items[0]

        result_item = await test_repository.get_by_id(db_item.id)

        assert result_item is not None
        assert isinstance(result_item, self.model_class)
        assert result_item.id == db_item.id
        assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_all_empty(self, test_repository):
        result_items = await test_repository.get_all()

        assert result_items is not None
        assert len(result_items) == 0

    @pytest.mark.asyncio
    async def test_get_all(self, test_repository, db_items):
        result_items = await test_repository.get_all()

        assert result_items is not None
        assert len(result_items) == len(db_items)

        for result_item, db_item in zip(result_items, db_items):
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_all_with_sorting(self, test_repository, db_items):
        """Test retrieving all items with sorting parameters"""
        result_items_asc = await test_repository.get_all(
            sort_params=SortParams(sort_by=self.sort_by, order="asc")
        )

        result_items_desc = await test_repository.get_all(
            sort_params=SortParams(sort_by=self.sort_by, order="desc")
        )

        db_items_asc = sorted(db_items, key=lambda x: getattr(x, self.sort_by))
        for result_item, db_item in zip(result_items_asc, db_items_asc):
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

        db_items_desc = reversed(db_items_asc)
        for result_item, db_item in zip(result_items_desc, db_items_desc):
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

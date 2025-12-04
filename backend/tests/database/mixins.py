from typing import Type

import pytest

from src.database.base_repository import BaseRepository


class BaseRepositoryMixin:
    model_class: Type = None

    @pytest.fixture()
    def test_repository(self) -> BaseRepository:
        """Create an instance of the repository for testing"""
        pass

    @pytest.fixture()
    def db_items(self):
        """Retrieve test items from fixtures based on model_class"""
        pass

    @pytest.mark.asyncio
    async def test_base_get_by_id_found(self, test_repository, db_items):
        item = db_items[0]

        result_item = await test_repository.get_by_id(item.id)

        assert result_item is not None
        assert isinstance(result_item, self.model_class)
        assert result_item.id == item.id
        assert result_item == item

    @pytest.mark.asyncio
    async def test_base_get_by_id_not_found(self, test_repository):
        result_item = await test_repository.get_by_id(-1)

        assert result_item is None

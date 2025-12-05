from typing import Type

import pytest
from sqlalchemy.exc import IntegrityError

from src.database.base_repository import BaseRepository
from src.sorting.models import SortParams


class BaseRepositoryMixin:
    model_class: Type = None
    sort_by = "id"
    unique_fields = []
    unique_keys = []

    @pytest.fixture()
    def test_repository(self) -> BaseRepository:
        """Create an instance of the repository for testing"""
        pass

    @pytest.fixture()
    def db_items(self):
        """Retrieve test items from fixtures based on model_class"""
        pass

    @pytest.fixture()
    def new_item(self):
        """Create a new instance of the model_class for testing"""
        pass

    @pytest.fixture()
    def updated_item(self):
        """Create an updated instance of the model_class for testing"""
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
    async def test_get_by_field_not_found(self, test_repository):
        result_item = await test_repository.get_by_field("id", -1)

        assert result_item is None

    @pytest.mark.asyncio
    async def test_get_by_field_found(self, test_repository, db_items):
        for field in self.unique_fields:
            db_item = db_items[0]

            result_item = await test_repository.get_by_field(
                field, getattr(db_item, field)
            )

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

    @pytest.mark.asyncio
    async def test_save(self, test_repository, new_item):
        """Test saving a new item"""
        saved_item = await test_repository.save(new_item)

        assert saved_item is not None
        assert isinstance(saved_item, self.model_class)
        assert saved_item.id is not None
        assert saved_item == new_item

    @pytest.mark.asyncio
    async def test_save_unique_constraint_violation(
        self, test_repository, db_items, new_item
    ):
        for field in self.unique_fields:
            db_item = db_items[0]
            setattr(new_item, field, getattr(db_item, field))

            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save(new_item)

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_unique_constraint_violation_multiple_fields(
        self, test_repository, db_items, new_item
    ):
        for keys in self.unique_keys:
            db_item = db_items[0]
            for key in keys:
                setattr(new_item, key, getattr(db_item, key))

            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save(new_item)

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_all_empty(self, test_repository):
        saved_items = await test_repository.save_all([])

        assert saved_items == []

    @pytest.mark.asyncio
    async def test_save_all(self, test_repository, new_item, updated_item):
        items_to_save = [new_item, updated_item]

        saved_items = await test_repository.save_all(items_to_save)

        for saved_item, item_to_save in zip(saved_items, items_to_save):
            assert saved_item is not None
            assert isinstance(saved_item, self.model_class)
            assert saved_item.id is not None
            assert saved_item == item_to_save

    @pytest.mark.asyncio
    async def test_save_all_unique_constraint_violation(
        self, test_repository, new_item, updated_item
    ):

        for field in self.unique_fields:
            item_to_save = self.model_class(**new_item.model_dump())
            item_to_save_2 = self.model_class(**updated_item.model_dump())

            setattr(item_to_save_2, field, getattr(item_to_save, field))

            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save_all([item_to_save, item_to_save_2])

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_all_unique_constraint_violation_multiple_fields(
        self, test_repository, new_item, updated_item
    ):
        for keys in self.unique_keys:
            item_to_save = self.model_class(**new_item.model_dump())
            item_to_save_2 = self.model_class(**updated_item.model_dump())

            for key in keys:
                setattr(item_to_save_2, key, getattr(item_to_save, key))

            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save_all([item_to_save, item_to_save_2])

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_delete(self, test_repository, db_items):
        db_item = db_items[0]

        await test_repository.delete(db_item)

        result_item = await test_repository.get_by_id(db_item.id)
        assert result_item is None

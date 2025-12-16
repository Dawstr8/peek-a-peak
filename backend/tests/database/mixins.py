from typing import Generic, Type, TypeVar
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.common.exceptions import NotFoundException
from src.database.base_repository import BaseRepository
from src.sorting.models import SortParams

T = TypeVar("T", bound=SQLModel)
R = TypeVar("R", bound=BaseRepository)


class BaseRepositoryMixin(Generic[T, R]):
    repository_class: Type[R] = None
    model_class: Type[T] = None
    sort_by = "id"
    unique_fields = []
    unique_keys = []
    has_owner = False

    items_fixture = None

    @pytest.fixture()
    def test_repository(self, test_db: AsyncSession) -> R:
        if self.repository_class is None:
            raise NotImplementedError(
                "repository_class must be defined in the subclass."
            )

        if self.items_fixture is None:
            raise NotImplementedError("items_fixture must be defined in the subclass.")

        return self.repository_class(test_db)

    @pytest.fixture()
    def items(self, request) -> list[T]:
        """Retrieve test items from fixtures based on model_class"""
        return request.getfixturevalue(self.items_fixture)

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_repository):
        # Act & Assert
        with pytest.raises(NotFoundException):
            await test_repository.get_by_id(uuid4())

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, test_repository, items):
        # Arrange
        db_item = await test_repository.save(items[0])

        # Act
        result_item = await test_repository.get_by_id(db_item.id)

        # Assert
        assert result_item is not None
        assert isinstance(result_item, self.model_class)
        assert result_item.id == db_item.id
        assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_by_id_if_owned_not_found(self, test_repository, items):
        if not self.has_owner:
            pytest.skip("Model does not have an owner field")

        # Arrange
        db_item = await test_repository.save(items[0])

        # Act & Assert
        with pytest.raises(NotFoundException):
            await test_repository.get_by_id_if_owned(db_item.id, uuid4())

    @pytest.mark.asyncio
    async def test_get_by_id_if_owned_found(self, test_repository, items):
        if not self.has_owner:
            pytest.skip("Model does not have an owner field")

        # Arrange
        db_item = await test_repository.save(items[0])

        # Act
        result_item = await test_repository.get_by_id_if_owned(
            db_item.id, db_item.owner_id
        )

        # Assert
        assert result_item is not None
        assert isinstance(result_item, self.model_class)
        assert result_item.id == db_item.id
        assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_by_field_not_found(self, test_repository):
        if not self.unique_fields:
            pytest.skip("No unique fields defined for this model")

        # Act & Assert
        with pytest.raises(NotFoundException):
            await test_repository.get_by_field("id", uuid4())

    @pytest.mark.asyncio
    async def test_get_by_field_found(self, test_repository, items):
        if not self.unique_fields:
            pytest.skip("No unique fields defined for this model")

        # Arrange
        db_item = await test_repository.save(items[0])

        for field in self.unique_fields:
            # Act
            result_item = await test_repository.get_by_field(
                field, getattr(db_item, field)
            )

            # Assert
            assert result_item is not None
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_by_fields_not_found(self, test_repository):
        if not self.unique_keys:
            pytest.skip("No unique keys defined for this model")

        # Act & Assert
        with pytest.raises(NotFoundException):
            await test_repository.get_by_fields({"id": uuid4()})

    @pytest.mark.asyncio
    async def test_get_by_fields_found(self, test_repository, items):
        if not self.unique_keys:
            pytest.skip("No unique keys defined for this model")

        # Arrange
        db_item = await test_repository.save(items[0])

        for keys in self.unique_keys:
            filters = {key: getattr(db_item, key) for key in keys}

            # Act
            result_item = await test_repository.get_by_fields(filters)

            # Assert
            assert result_item is not None
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_all_empty(self, test_repository):
        # Act
        result_items = await test_repository.get_all()

        # Assert
        assert result_items is not None
        assert len(result_items) == 0

    @pytest.mark.asyncio
    async def test_get_all(self, test_repository, items):
        # Arrange
        db_items = await test_repository.save_all(items)

        # Act
        result_items = await test_repository.get_all()

        # Assert
        assert result_items is not None
        assert len(result_items) == len(db_items)

        for result_item, db_item in zip(result_items, db_items):
            assert isinstance(result_item, self.model_class)
            assert result_item.id == db_item.id
            assert result_item == db_item

    @pytest.mark.asyncio
    async def test_get_all_with_sorting(self, test_repository, items):
        """Test retrieving all items with sorting parameters"""
        # Arrange
        db_items = await test_repository.save_all(items)

        # Act
        result_items_asc = await test_repository.get_all(
            sort_params=SortParams(sort_by=self.sort_by, order="asc")
        )

        result_items_desc = await test_repository.get_all(
            sort_params=SortParams(sort_by=self.sort_by, order="desc")
        )

        # Assert
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
    async def test_save(self, test_repository, items):
        """Test saving a new item"""
        # Arrange
        new_item = items[0]

        # Act
        saved_item = await test_repository.save(new_item)

        # Assert
        assert saved_item is not None
        assert isinstance(saved_item, self.model_class)
        assert saved_item.id is not None
        assert saved_item == new_item

    @pytest.mark.asyncio
    async def test_save_unique_constraint_violation(self, test_repository, items):
        if not self.unique_fields:
            pytest.skip("No unique fields defined for this model")

        # Arrange
        db_item = await test_repository.save(items[0])
        for field in self.unique_fields:
            new_item = self.model_class(**items[1].model_dump())
            setattr(new_item, field, getattr(db_item, field))

            # Act and Assert
            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save(new_item)

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_unique_constraint_violation_multiple_fields(
        self, test_repository, items
    ):
        if not self.unique_keys:
            pytest.skip("No unique keys defined for this model")

        # Arrange
        db_item = await test_repository.save(items[0])
        for keys in self.unique_keys:
            new_item = self.model_class(**items[1].model_dump())
            for key in keys:
                setattr(new_item, key, getattr(db_item, key))

            # Act and Assert
            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save(new_item)

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_all_empty(self, test_repository):
        # Act
        saved_items = await test_repository.save_all([])

        # Assert
        assert saved_items == []

    @pytest.mark.asyncio
    async def test_save_all(self, test_repository, items):
        # Arrange
        items_to_save = items

        # Act
        saved_items = await test_repository.save_all(items_to_save)

        # Assert
        for saved_item, item_to_save in zip(saved_items, items_to_save):
            assert saved_item is not None
            assert isinstance(saved_item, self.model_class)
            assert saved_item.id is not None
            assert saved_item == item_to_save

    @pytest.mark.asyncio
    async def test_save_all_unique_constraint_violation(self, test_repository, items):
        if not self.unique_fields:
            pytest.skip("No unique fields defined for this model")

        # Arrange
        for field in self.unique_fields:
            item_to_save = self.model_class(**items[0].model_dump())
            item_to_save_2 = self.model_class(**items[1].model_dump())

            setattr(item_to_save_2, field, getattr(item_to_save, field))

            # Act and Assert
            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save_all([item_to_save, item_to_save_2])

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_save_all_unique_constraint_violation_multiple_fields(
        self, test_repository, items
    ):
        if not self.unique_keys:
            pytest.skip("No unique keys defined for this model")

        # Arrange
        for keys in self.unique_keys:
            item_to_save = self.model_class(**items[0].model_dump())
            item_to_save_2 = self.model_class(**items[1].model_dump())

            for key in keys:
                setattr(item_to_save_2, key, getattr(item_to_save, key))

            # Act and Assert
            with pytest.raises(IntegrityError) as exc_info:
                await test_repository.save_all([item_to_save, item_to_save_2])

            assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_delete(self, test_repository, items):
        # Arrange
        db_item = await test_repository.save(items[0])

        # Act
        await test_repository.delete(db_item)

        # Assert
        with pytest.raises(NotFoundException):
            await test_repository.get_by_id(db_item.id)

    @pytest.mark.asyncio
    async def test_count_no_items(self, test_repository):
        # Arrange
        count = await test_repository.count()

        # Assert
        assert count == 0

    @pytest.mark.asyncio
    async def test_count_with_items(self, test_repository, items):
        # Arrange
        db_items = await test_repository.save_all(items)

        # Act
        count = await test_repository.count()

        # Assert
        assert count == len(db_items)

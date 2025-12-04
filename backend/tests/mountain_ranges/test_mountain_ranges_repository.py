import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository
from tests.database.mixins import BaseRepositoryMixin


class TestMountainRangesRepository(BaseRepositoryMixin):
    model_class = MountainRange
    sort_by = "name"
    unique_fields = ["name"]

    @pytest.fixture
    def test_repository(self, test_db: AsyncSession) -> MountainRangesRepository:
        return MountainRangesRepository(test_db)

    @pytest.fixture
    def db_items(self, db_mountain_ranges) -> list[MountainRange]:
        return db_mountain_ranges

    @pytest.fixture
    def new_item(self) -> MountainRange:
        return MountainRange(name="New Mountain Range")

    @pytest.mark.asyncio
    async def test_get_by_name(self, test_repository, db_mountain_ranges):
        """Test retrieving an existing mountain range by name."""
        found_mountain_range = await test_repository.get_by_name("Tatry")

        assert found_mountain_range is not None
        assert found_mountain_range.name == "Tatry"
        assert found_mountain_range.id is not None

    @pytest.mark.asyncio
    async def test_get_by_name_non_existing_mountain_range(
        self, test_repository, db_mountain_ranges
    ):
        """Test retrieving a non-existing mountain range by name returns None."""
        found_mountain_range = await test_repository.get_by_name("NonExistentRange")

        assert found_mountain_range is None

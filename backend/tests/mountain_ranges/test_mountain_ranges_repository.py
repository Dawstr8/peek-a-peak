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

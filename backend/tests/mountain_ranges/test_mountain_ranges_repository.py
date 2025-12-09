import pytest

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository
from tests.database.mixins import BaseRepositoryMixin


class TestMountainRangesRepository(BaseRepositoryMixin):
    repository_class = MountainRangesRepository
    model_class = MountainRange
    sort_by = "name"
    unique_fields = ["name"]

    @pytest.fixture
    def db_items(self, db_mountain_ranges) -> list[MountainRange]:
        return db_mountain_ranges

    @pytest.fixture
    def new_item(self) -> MountainRange:
        return MountainRange(name="New Mountain Range")

    @pytest.fixture
    def updated_item(self) -> MountainRange:
        return MountainRange(name="Updated Mountain Range")

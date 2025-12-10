from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository
from tests.database.mixins import BaseRepositoryMixin


class TestMountainRangesRepository(
    BaseRepositoryMixin[MountainRange, MountainRangesRepository]
):
    repository_class = MountainRangesRepository
    model_class = MountainRange
    sort_by = "name"
    unique_fields = ["name"]

    items_fixture = "mountain_ranges"

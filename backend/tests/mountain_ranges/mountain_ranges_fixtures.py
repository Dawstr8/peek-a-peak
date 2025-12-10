import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository


@pytest.fixture
def mountain_ranges() -> list[MountainRange]:
    return [
        MountainRange(name="Tatry"),
        MountainRange(name="Karkonosze"),
        MountainRange(name="Beskidy"),
    ]


@pytest.fixture
def mock_mountain_ranges_map(mountain_ranges) -> dict[str, MountainRange]:
    """
    Returns a map of mock MountainRange objects for unit tests.
    """

    for i, range in enumerate(mountain_ranges, start=1):
        range.id = i

    return {
        "tatry": mountain_ranges[0],
        "karkonosze": mountain_ranges[1],
        "beskidy": mountain_ranges[2],
    }


@pytest_asyncio.fixture
async def db_mountain_ranges(
    test_db: AsyncSession, mountain_ranges
) -> dict[str, MountainRange]:
    """Fixture to seed mountain ranges into the test database."""
    repository = MountainRangesRepository(test_db)
    return await repository.save_all(mountain_ranges)

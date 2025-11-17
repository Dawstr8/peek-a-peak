import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange


@pytest.fixture
def mock_mountain_ranges_map() -> dict[str, MountainRange]:
    """
    Returns a map of mock MountainRange objects for unit tests.
    """
    return {
        "tatry": MountainRange(id=1, name="Tatry"),
        "beskidy": MountainRange(id=2, name="Beskidy"),
    }


@pytest_asyncio.fixture
async def db_mountain_ranges(test_db: AsyncSession) -> dict[str, MountainRange]:
    """Fixture to seed mountain ranges into the test database."""
    mountain_ranges = [
        MountainRange(name="Tatry"),
        MountainRange(name="Karkonosze"),
        MountainRange(name="Beskidy"),
    ]

    for mountain_range in mountain_ranges:
        test_db.add(mountain_range)

    await test_db.commit()

    for mountain_range in mountain_ranges:
        await test_db.refresh(mountain_range)

    return mountain_ranges

import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository


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
    repository = MountainRangesRepository(test_db)

    return await repository.save_all(
        [
            MountainRange(name="Tatry"),
            MountainRange(name="Karkonosze"),
            MountainRange(name="Beskidy"),
        ]
    )

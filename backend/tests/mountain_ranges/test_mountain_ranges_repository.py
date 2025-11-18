import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository


@pytest_asyncio.fixture
async def test_repository(test_db: AsyncSession) -> MountainRangesRepository:
    return MountainRangesRepository(test_db)


@pytest.mark.asyncio
async def test_save(test_repository: MountainRangesRepository):
    """Test saving a new mountain range to the database."""
    mountain_range = MountainRange(name="Test Mountain Range")

    saved_mountain_range = await test_repository.save(mountain_range)

    assert saved_mountain_range.id is not None
    assert saved_mountain_range.name == "Test Mountain Range"


@pytest.mark.asyncio
async def test_save_duplicate_name_raises_error(
    test_repository: MountainRangesRepository,
):
    """Test that saving duplicate mountain range names raises an error due to unique constraint."""
    mountain_range1 = MountainRange(name="Duplicate Range")
    mountain_range2 = MountainRange(name="Duplicate Range")

    await test_repository.save(mountain_range1)

    with pytest.raises(Exception):
        await test_repository.save(mountain_range2)


@pytest.mark.asyncio
async def test_get_by_name(
    test_repository: MountainRangesRepository, db_mountain_ranges
):
    """Test retrieving an existing mountain range by name."""
    found_mountain_range = await test_repository.get_by_name("Tatry")

    assert found_mountain_range is not None
    assert found_mountain_range.name == "Tatry"
    assert found_mountain_range.id is not None


@pytest.mark.asyncio
async def test_get_by_name_non_existing_mountain_range(
    test_repository: MountainRangesRepository, db_mountain_ranges
):
    """Test retrieving a non-existing mountain range by name returns None."""
    found_mountain_range = await test_repository.get_by_name("NonExistentRange")

    assert found_mountain_range is None

"""
Peak fixtures for testing across different test types: unit, integration, and e2e
"""

from uuid import uuid4

import pytest
import pytest_asyncio

from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository
from tests.peaks.mock_repository import MockPeaksRepository


@pytest.fixture
def peaks(mountain_ranges) -> list[Peak]:
    """Returns a list of Peak models for unit tests."""
    return [
        Peak(
            name="Rysy",
            elevation=2499,
            location="POINT(20.0881 49.1795)",
            mountain_range=mountain_ranges[0],
        ),
        Peak(
            name="Śnieżka",
            elevation=1602,
            location="POINT(15.7400 50.7361)",
            mountain_range=mountain_ranges[1],
        ),
        Peak(
            name="Babia Góra",
            elevation=1725,
            location="POINT(19.5292 49.5731)",
            mountain_range=mountain_ranges[2],
        ),
    ]


@pytest.fixture
def coords_map():
    """
    Returns a dictionary mapping location names to (lat, lng) tuples.
    This is useful for tests that need specific coordinates.
    """
    return {
        "near_rysy": (49.1794, 20.0880),
        "near_sniezka": (50.7360, 15.7401),
        "warsaw": (52.2297, 21.0122),
    }


@pytest.fixture
def mock_peaks_map(peaks) -> dict[str, Peak]:
    """
    Returns a dictionary mapping peak names to mock Peak objects for unit tests.
    These peaks are not persisted anywhere and are useful for pure unit tests
    that don't need database interaction.
    """
    for peak in peaks:
        peak.id = uuid4()

    return {"rysy": peaks[0], "śnieżka": peaks[1], "babia_gora": peaks[2]}


@pytest.fixture
def mock_peaks_repository(mock_peaks_map, coords_map) -> PeaksRepository:
    """
    Returns a mock PeaksRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    return MockPeaksRepository(
        items=list(mock_peaks_map.values()), coords_map=coords_map
    ).mock


@pytest_asyncio.fixture
async def db_peaks(test_db, peaks) -> list[Peak]:
    """
    Creates and returns a list of Peak models in the test database.
    This fixture is useful for integration and e2e tests that require
    actual database records.
    """
    repository = PeaksRepository(test_db)
    return await repository.save_all(peaks)

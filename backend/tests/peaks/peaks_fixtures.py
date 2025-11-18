"""
Peak fixtures for testing across different test types: unit, integration, and e2e
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.peaks.models import Peak, PeakWithDistance
from src.peaks.repository import PeaksRepository


@pytest.fixture
def coords_map():
    """
    Returns a dictionary mapping location names to (latitude, longitude) tuples.
    This is useful for tests that need specific coordinates.
    """
    return {
        "near_rysy": (49.1794, 20.0880),
        "near_sniezka": (50.7360, 15.7401),
        "warsaw": (52.2297, 21.0122),
    }


@pytest.fixture
def mock_peaks_map(mock_mountain_ranges_map) -> dict[str, Peak]:
    """
    Returns a dictionary mapping peak names to mock Peak objects for unit tests.
    These peaks are not persisted anywhere and are useful for pure unit tests
    that don't need database interaction.
    """
    return {
        "rysy": Peak(
            id=1,
            name="Rysy",
            elevation=2499,
            location="POINT(20.0881 49.1795)",
            range_id=mock_mountain_ranges_map["tatry"].id,
        ),
        "giewont": Peak(
            id=2,
            name="Giewont",
            elevation=1894,
            location="POINT(19.9344 49.2522)",
            range_id=mock_mountain_ranges_map["tatry"].id,
        ),
        "babia_gora": Peak(
            id=3,
            name="Babia Góra",
            elevation=1725,
            location="POINT(19.5292 49.5731)",
            range_id=mock_mountain_ranges_map["beskidy"].id,
        ),
    }


@pytest.fixture
def mock_peaks_repository(mock_peaks_map, coords_map) -> PeaksRepository:
    """
    Returns a mock PeaksRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    repo = MagicMock(spec=PeaksRepository)

    async def get_all():
        return [peak for peak in mock_peaks_map.values()]

    async def get_by_id(peak_id):
        for peak in mock_peaks_map.values():
            if peak.id == peak_id:
                return peak

        return None

    async def get_nearest(
        latitude: float, longitude: float, max_distance=None, name_filter=None, limit=5
    ):
        if (latitude, longitude) == coords_map["near_rysy"]:
            results = [
                PeakWithDistance(peak=mock_peaks_map["rysy"], distance=50.0),
                PeakWithDistance(peak=mock_peaks_map["giewont"], distance=30000.0),
                PeakWithDistance(peak=mock_peaks_map["babia_gora"], distance=80000.0),
            ]
        elif (latitude, longitude) == coords_map["near_sniezka"]:
            results = [
                PeakWithDistance(peak=mock_peaks_map["giewont"], distance=150000.0),
                PeakWithDistance(peak=mock_peaks_map["babia_gora"], distance=250000.0),
                PeakWithDistance(peak=mock_peaks_map["rysy"], distance=400000.0),
            ]
        elif (latitude, longitude) == coords_map["warsaw"]:
            results = [
                PeakWithDistance(peak=mock_peaks_map["babia_gora"], distance=250000.0),
                PeakWithDistance(peak=mock_peaks_map["giewont"], distance=300000.0),
                PeakWithDistance(peak=mock_peaks_map["rysy"], distance=400000.0),
            ]

        results_within_distance = [
            result
            for result in results
            if max_distance is None or result.distance <= max_distance
        ]

        if name_filter:
            results_within_distance = [
                result
                for result in results_within_distance
                if name_filter.lower() in result.peak.name.lower()
            ]

        return results_within_distance[:limit]

    repo.get_all = AsyncMock(side_effect=get_all)
    repo.get_by_id = AsyncMock(side_effect=get_by_id)
    repo.get_nearest = AsyncMock(side_effect=get_nearest)

    return repo


@pytest_asyncio.fixture
async def db_peaks(test_db, db_mountain_ranges) -> list[Peak]:
    """
    Creates and returns a list of Peak models in the test database.
    This fixture is useful for integration and e2e tests that require
    actual database records.
    """
    repository = PeaksRepository(test_db)

    peaks = [
        Peak(
            name="Rysy",
            elevation=2499,
            location="POINT(20.0881 49.1795)",
            mountain_range_id=db_mountain_ranges[0].id,
        ),
        Peak(
            name="Śnieżka",
            elevation=1602,
            location="POINT(15.7400 50.7361)",
            mountain_range_id=db_mountain_ranges[1].id,
        ),
        Peak(
            name="Babia Góra",
            elevation=1725,
            location="POINT(19.5292 49.5731)",
            mountain_range_id=db_mountain_ranges[2].id,
        ),
    ]

    for peak in peaks:
        await repository.save(peak)

    return peaks

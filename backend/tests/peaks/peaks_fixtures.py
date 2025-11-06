"""
Peak fixtures for testing across different test types: unit, integration, and e2e
"""

from unittest.mock import MagicMock

import pytest

from src.peaks.models import Peak
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
def mock_peaks_map() -> dict[str, Peak]:
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
            latitude=49.1795,
            longitude=20.0881,
            range="Tatry",
        ),
        "giewont": Peak(
            id=2,
            name="Giewont",
            elevation=1894,
            latitude=49.2522,
            longitude=19.9344,
            range="Tatry",
        ),
        "babia_gora": Peak(
            id=3,
            name="Babia Góra",
            elevation=1725,
            latitude=49.5731,
            longitude=19.5292,
            range="Beskidy",
        ),
    }


@pytest.fixture
def mock_peaks_repository(mock_peaks_map) -> PeaksRepository:
    """
    Returns a mock PeaksRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    repo = MagicMock(spec=PeaksRepository)

    def get_all():
        return [peak for peak in mock_peaks_map.values()]

    def get_by_id(peak_id):
        for peak in mock_peaks_map.values():
            if peak.id == peak_id:
                return peak

        return None

    repo.get_all.side_effect = get_all
    repo.get_by_id.side_effect = get_by_id

    return repo


@pytest.fixture
def db_peaks(test_db) -> list[Peak]:
    """
    Creates and returns a list of Peak models in the test database.
    This fixture is useful for integration and e2e tests that require
    actual database records.
    """
    peaks = [
        Peak(
            name="Rysy",
            elevation=2499,
            latitude=49.1795,
            longitude=20.0881,
            range="Tatry",
        ),
        Peak(
            name="Śnieżka",
            elevation=1602,
            latitude=50.7361,
            longitude=15.7400,
            range="Karkonosze",
        ),
        Peak(
            name="Babia Góra",
            elevation=1725,
            latitude=49.5731,
            longitude=19.5297,
            range="Beskidy",
        ),
    ]

    for peak in peaks:
        test_db.add(peak)

    test_db.commit()

    for peak in peaks:
        test_db.refresh(peak)

    return peaks

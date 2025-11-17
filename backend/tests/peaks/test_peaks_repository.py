"""
Tests for the PeaksRepository
"""

import pytest

from src.mountain_ranges.models import MountainRange
from src.peaks.repository import PeaksRepository


@pytest.fixture()
def test_repository(test_db):
    """Create a PeaksRepository instance for testing"""
    return PeaksRepository(test_db)


@pytest.mark.asyncio
async def test_get_all(test_repository, db_peaks):
    """Test retrieving all peaks"""
    peaks = await test_repository.get_all()

    assert len(peaks) == 3
    assert any(peak.name == "Rysy" for peak in peaks)
    assert any(peak.name == "Śnieżka" for peak in peaks)
    assert any(peak.name == "Babia Góra" for peak in peaks)


@pytest.mark.asyncio
async def test_get_by_id(test_repository, db_peaks):
    """Test retrieving a peak by ID"""
    peak_id = db_peaks[0].id

    peak = await test_repository.get_by_id(peak_id)

    assert peak is not None
    assert peak.name == "Rysy"
    assert peak.elevation == 2499

    peak = await test_repository.get_by_id(999999)
    assert peak is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "coords_key,params,expected_results",
    [
        (
            "near_rysy",
            {},
            [
                {"name": "Rysy", "distance": 100.0},
                {"name": "Babia Góra", "distance": 80000.0},
                {"name": "Śnieżka", "distance": 400000.0},
            ],
        ),
        (
            "near_rysy",
            {"limit": 2},
            [
                {"name": "Rysy", "distance": 100.0},
                {"name": "Babia Góra", "distance": 80000.0},
            ],
        ),
        (
            "near_rysy",
            {"max_distance": 100000},
            [
                {"name": "Rysy", "distance": 100.0},
                {"name": "Babia Góra", "distance": 80000.0},
            ],
        ),
        (
            "near_sniezka",
            {},
            [
                {"name": "Śnieżka", "distance": 100.0},
                {"name": "Babia Góra", "distance": 350000.0},
                {"name": "Rysy", "distance": 400000.0},
            ],
        ),
    ],
)
async def test_get_nearest_parametrized(
    test_repository, db_peaks, coords_map, coords_key, params, expected_results
):
    """Test finding nearest peaks with various parameters"""
    latitude, longitude = coords_map[coords_key]

    results = await test_repository.get_nearest(
        latitude=latitude, longitude=longitude, **params
    )

    assert len(results) == len(expected_results)

    for peak_with_distance, expected in zip(results, expected_results):
        peak, distance = peak_with_distance.peak, peak_with_distance.distance
        assert peak.id is not None
        assert peak.name == expected["name"]
        assert peak.elevation is not None
        assert peak.latitude is not None
        assert peak.longitude is not None
        assert peak.mountain_range_id is not None
        assert isinstance(peak.mountain_range, MountainRange)

        assert isinstance(distance, float)
        assert 0 <= distance <= expected["distance"]

    distances = [item.distance for item in results]
    assert distances == sorted(distances)


@pytest.mark.asyncio
async def test_get_nearest_empty_database(test_repository, coords_map):
    """Test finding nearest peaks when database is empty"""
    latitude, longitude = coords_map["near_rysy"]

    results = await test_repository.get_nearest(latitude=latitude, longitude=longitude)

    assert results == []

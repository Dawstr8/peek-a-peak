"""
Tests for the PeaksRepository
"""

import pytest

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
async def test_get_nearest_default(test_repository, db_peaks, coords_map):
    """Test finding nearest peaks (default limit)"""
    latitude, longitude = coords_map["near_rysy"]

    results = await test_repository.get_nearest(latitude=latitude, longitude=longitude)

    assert len(results) == 3

    for peak_with_distance in results:
        peak, distance = peak_with_distance.peak, peak_with_distance.distance
        assert peak.id is not None
        assert peak.name is not None
        assert peak.elevation is not None
        assert peak.latitude is not None
        assert peak.longitude is not None
        assert peak.range is not None

        assert isinstance(distance, float)
        assert distance >= 0

    distances = [item.distance for item in results]
    assert distances == sorted(distances)
    assert results[0].peak.name == "Rysy"
    assert results[0].distance < 100


@pytest.mark.asyncio
async def test_get_nearest_with_limit(test_repository, db_peaks, coords_map):
    """Test finding nearest peaks with a custom limit"""
    latitude, longitude = coords_map["near_rysy"]

    results = await test_repository.get_nearest(
        latitude=latitude, longitude=longitude, limit=2
    )

    assert len(results) == 2
    assert results[0].distance < results[1].distance
    assert results[0].peak.name == "Rysy"


@pytest.mark.asyncio
async def test_get_nearest_with_max_distance(test_repository, db_peaks, coords_map):
    """Test finding nearest peaks with max_distance filter"""
    latitude, longitude = coords_map["near_rysy"]

    results = await test_repository.get_nearest(
        latitude=latitude, longitude=longitude, max_distance=100
    )

    assert len(results) == 1
    assert results[0].peak.name == "Rysy"
    assert results[0].distance < 100


@pytest.mark.asyncio
async def test_get_nearest_from_sniezka(test_repository, db_peaks, coords_map):
    """Test finding nearest peaks from coordinates near Śnieżka"""
    latitude, longitude = coords_map["near_sniezka"]

    results = await test_repository.get_nearest(latitude=latitude, longitude=longitude)

    assert len(results) == 3
    assert results[0].peak.name == "Śnieżka"
    assert results[0].distance < 100


@pytest.mark.asyncio
async def test_get_nearest_empty_database(test_repository, coords_map):
    """Test finding nearest peaks when database is empty"""
    latitude, longitude = coords_map["near_rysy"]

    results = await test_repository.get_nearest(latitude=latitude, longitude=longitude)

    assert results == []

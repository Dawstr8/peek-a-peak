"""
Tests for the PeaksService
"""

import pytest

from src.peaks.service import PeaksService


@pytest.fixture
def mock_peaks_service(mock_peaks_repository) -> PeaksService:
    """Create a PeaksService with mocked dependencies"""
    return PeaksService(mock_peaks_repository)


@pytest.mark.asyncio
async def test_get_all(mock_peaks_service, mock_peaks_repository):
    """Test getting all peaks through the service"""
    peaks = await mock_peaks_service.get_all()

    assert len(peaks) == 3
    assert peaks[0].name == "Rysy"
    assert peaks[1].name == "Giewont"
    assert peaks[2].name == "Babia Góra"

    mock_peaks_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(mock_peaks_map, mock_peaks_service, mock_peaks_repository):
    """Test getting a specific peak by ID through the service"""
    peak = await mock_peaks_service.get_by_id(mock_peaks_map["rysy"].id)

    assert peak is not None
    assert peak.id == mock_peaks_map["rysy"].id
    assert peak.name == mock_peaks_map["rysy"].name

    mock_peaks_repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_not_found(mock_peaks_service, mock_peaks_repository):
    """Test getting a peak by ID when it doesn't exist"""
    peak = await mock_peaks_service.get_by_id(999)

    assert peak is None

    mock_peaks_repository.get_by_id.assert_called_once_with(999)


@pytest.mark.asyncio
async def test_find_nearest_peaks(
    coords_map, mock_peaks_service, mock_peaks_repository
):
    """Test finding the nearest peaks"""
    results = await mock_peaks_service.find_nearest_peaks(
        latitude=coords_map["near_rysy"][0],
        longitude=coords_map["near_rysy"][1],
        limit=5,
    )

    assert len(results) == 3
    assert results[0]["peak"].id == 1
    assert results[0]["peak"].name == "Rysy"
    assert results[0]["distance"] < 100
    assert results[1]["peak"].name == "Giewont"
    assert results[1]["distance"] < 50000
    assert results[2]["peak"].name == "Babia Góra"
    assert results[2]["distance"] < 100000

    mock_peaks_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_find_nearest_peaks_respects_limit(
    coords_map, mock_peaks_service, mock_peaks_repository
):
    """Test that the limit parameter correctly limits the number of results"""
    results = await mock_peaks_service.find_nearest_peaks(
        latitude=coords_map["near_rysy"][0],
        longitude=coords_map["near_rysy"][1],
        limit=2,
    )

    assert len(results) == 2
    assert results[0]["distance"] < results[1]["distance"]

    mock_peaks_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_find_nearest_peaks_with_max_distance(
    coords_map, mock_peaks_service, mock_peaks_repository
):
    """Test that max_distance parameter filters peaks correctly"""

    results = await mock_peaks_service.find_nearest_peaks(
        latitude=coords_map["near_rysy"][0],
        longitude=coords_map["near_rysy"][1],
        max_distance=100,
    )

    assert len(results) == 1
    assert results[0]["peak"].name == "Rysy"
    assert results[0]["distance"] < 100

    mock_peaks_repository.get_all.assert_called()


@pytest.mark.asyncio
async def test_find_nearest_peaks_max_distance_none(
    coords_map, mock_peaks_service, mock_peaks_repository
):
    """Test that max_distance=None includes all peaks"""
    results = await mock_peaks_service.find_nearest_peaks(
        latitude=coords_map["near_rysy"][0],
        longitude=coords_map["near_rysy"][1],
        max_distance=None,
    )

    assert len(results) == 3
    assert results[0]["peak"].name == "Rysy"
    assert results[1]["peak"].name == "Giewont"
    assert results[2]["peak"].name == "Babia Góra"

    mock_peaks_repository.get_all.assert_called_once()

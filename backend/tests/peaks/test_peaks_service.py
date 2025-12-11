"""
Tests for the PeaksService
"""

import pytest

from src.common.exceptions import NotFoundException
from src.peaks.service import PeaksService
from src.sorting.models import SortParams


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
    assert peaks[1].name == "Śnieżka"
    assert peaks[2].name == "Babia Góra"

    mock_peaks_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_count(mock_peaks_service, mock_peaks_repository):
    count = await mock_peaks_service.get_count()

    assert count == 3

    mock_peaks_repository.count.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(mock_peaks_map, mock_peaks_service, mock_peaks_repository):
    """Test getting a specific peak by ID through the service"""
    peak_id = mock_peaks_map["rysy"].id

    peak = await mock_peaks_service.get_by_id(peak_id)

    assert peak is not None
    assert peak.id == peak_id
    assert peak.name == mock_peaks_map["rysy"].name

    mock_peaks_repository.get_by_id.assert_called_once_with(peak_id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(mock_peaks_service, mock_peaks_repository):
    """Test getting a peak by ID when it doesn't exist"""
    id = 999

    with pytest.raises(NotFoundException):
        await mock_peaks_service.get_by_id(id)

    mock_peaks_repository.get_by_id.assert_called_once_with(id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,expected_length",
    [
        ({}, 3),
        ({"sort_params": None}, 3),
        ({"sort_params": SortParams(sort_by="elevation", order="desc")}, 3),
        ({"limit": None}, 3),
        ({"limit": 2}, 2),
        ({"name_filter": None}, 3),
        ({"name_filter": "rysy"}, 1),
        ({"name_filter": "nonexistent"}, 0),
    ],
)
async def test_search_peaks_parametrized(
    mock_peaks_service,
    params: dict,
    expected_length: int,
):
    """Test passing multiple parameter combinations to search"""
    results = await mock_peaks_service.search_peaks(**params)

    assert len(results) == expected_length


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,expected_length",
    [
        ({}, 3),
        ({"limit": 2}, 2),
        ({"limit": None}, 3),
        ({"max_distance": 100}, 1),
        ({"max_distance": None}, 3),
        ({"name_filter": "rysy"}, 1),
        ({"name_filter": "nonexistent"}, 0),
        ({"name_filter": None}, 3),
    ],
)
async def test_find_nearby_peaks_parametrized(
    coords_map,
    mock_peaks_service,
    params: dict,
    expected_length: int,
):
    """Test passing multiple coordinate sets to find nearby peaks"""
    lat, lng = coords_map["near_rysy"]

    results = await mock_peaks_service.find_nearby_peaks(
        lat=lat,
        lng=lng,
        **params,
    )

    assert len(results) == expected_length

    distances = [item.distance for item in results]
    assert distances == sorted(distances)

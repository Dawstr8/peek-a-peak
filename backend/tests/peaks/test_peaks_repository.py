"""
Tests for the PeaksRepository
"""

import pytest

from src.mountain_ranges.models import MountainRange
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository


@pytest.fixture()
def test_repository(test_db):
    """Create a PeaksRepository instance for testing"""
    return PeaksRepository(test_db)


@pytest.mark.asyncio
async def test_save(test_repository, db_mountain_ranges):
    """Test saving a single peak"""
    peak = Peak(
        name="Test Peak",
        elevation=2000,
        mountain_range_id=db_mountain_ranges[0].id,
    )

    saved_peak = await test_repository.save(peak)

    assert saved_peak.id is not None
    assert saved_peak.name == "Test Peak"
    assert saved_peak.elevation == 2000
    assert saved_peak.mountain_range_id == db_mountain_ranges[0].id


@pytest.mark.asyncio
async def test_save_duplicate_name_elevation_and_mountain_range_raises_error(
    test_repository, db_mountain_ranges
):
    """Test unique constraint when saving a single peak"""
    name = "Unique Peak"
    elevation = 3000
    mountain_range_id = db_mountain_ranges[0].id

    peak1 = Peak(
        name=name,
        elevation=elevation,
        mountain_range_id=mountain_range_id,
    )

    peak2 = Peak(
        name=name,
        elevation=elevation,
        mountain_range_id=mountain_range_id,
    )

    await test_repository.save(peak1)

    with pytest.raises(Exception) as exc_info:
        await test_repository.save(peak2)

    assert "uq_peak_name_elevation_mountain_range" in str(exc_info.value)


@pytest.mark.asyncio
async def test_save_multiple(test_repository, db_mountain_ranges):
    """Test saving multiple peaks"""
    peaks = [
        Peak(
            name="Test Peak 1",
            elevation=1000,
            mountain_range_id=db_mountain_ranges[0].id,
        ),
        Peak(
            name="Test Peak 2",
            elevation=1000,
            mountain_range_id=db_mountain_ranges[0].id,
        ),
        Peak(
            name="Test Peak 1",
            elevation=1500,
            mountain_range_id=db_mountain_ranges[0].id,
        ),
        Peak(
            name="Test Peak 1",
            elevation=1000,
            mountain_range_id=db_mountain_ranges[1].id,
        ),
    ]

    await test_repository.save_multiple(peaks)

    all_peaks = await test_repository.get_all()
    names = [peak.name for peak in all_peaks]

    assert len(all_peaks) == 4
    assert "Test Peak 1" in names
    assert "Test Peak 2" in names


@pytest.mark.asyncio
async def test_save_multiple_duplicate_name_elevation_and_mountain_range_raises_error(
    test_repository, db_mountain_ranges
):
    """Test unique constraint when saving multiple peaks"""
    name = "Unique Peak"
    elevation = 3000
    mountain_range_id = db_mountain_ranges[0].id

    peaks = [
        Peak(
            name=name,
            elevation=elevation,
            mountain_range_id=mountain_range_id,
        ),
        Peak(
            name=name,
            elevation=elevation,
            mountain_range_id=mountain_range_id,
        ),
    ]

    with pytest.raises(Exception) as exc_info:
        await test_repository.save_multiple(peaks)

    assert "uq_peak_name_elevation_mountain_range" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_all(test_repository, db_peaks):
    """Test retrieving all peaks"""
    peaks = await test_repository.get_all()

    assert len(peaks) == 3
    assert any(peak.name == "Rysy" for peak in peaks)
    assert any(peak.name == "Śnieżka" for peak in peaks)
    assert any(peak.name == "Babia Góra" for peak in peaks)


@pytest.mark.asyncio
async def test_get_all_without_location(test_repository, db_peaks):
    """Test retrieving peaks without location"""
    peak_without_location = Peak(
        name="No Location Peak",
        elevation=1200,
        mountain_range_id=db_peaks[0].mountain_range_id,
        location=None,
    )
    await test_repository.save(peak_without_location)

    peaks = await test_repository.get_all_without_location()

    assert len(peaks) == 1
    assert any(peak.name == "No Location Peak" for peak in peaks)


@pytest.mark.asyncio
async def test_get_count_no_peaks(test_repository):
    count = await test_repository.get_count()

    assert count == 0


@pytest.mark.asyncio
async def test_get_count(test_repository, db_peaks):
    count = await test_repository.get_count()

    assert count == 3


@pytest.mark.asyncio
async def test_get_summited_by_user_count_no_peaks(test_repository, db_user):
    count = await test_repository.get_summited_by_user_count(db_user.id)

    assert count == 0


@pytest.mark.asyncio
async def test_get_summited_by_user_count_no_photos(test_repository, db_user, db_peaks):
    count = await test_repository.get_summited_by_user_count(db_user.id)

    assert count == 0


@pytest.mark.asyncio
async def test_get_summited_by_user_count(
    test_repository, db_user, db_peaks, db_photos
):
    count = await test_repository.get_summited_by_user_count(db_user.id)

    assert count == 2


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
async def test_get_by_name_elevation_and_mountain_range(test_repository, db_peaks):
    """Test retrieving a peak by name, elevation, and mountain range ID"""
    peak = await test_repository.get_by_name_elevation_and_mountain_range(
        peak_name=db_peaks[0].name,
        elevation=db_peaks[0].elevation,
        mountain_range_id=db_peaks[0].mountain_range_id,
    )

    assert peak is not None
    assert peak.name == db_peaks[0].name
    assert peak.elevation == db_peaks[0].elevation
    assert peak.mountain_range_id == db_peaks[0].mountain_range_id

    peak = await test_repository.get_by_name_elevation_and_mountain_range(
        peak_name="Nonexistent Peak",
        elevation=db_peaks[0].elevation,
        mountain_range_id=db_peaks[0].mountain_range_id,
    )

    assert peak is None

    peak = await test_repository.get_by_name_elevation_and_mountain_range(
        peak_name=db_peaks[0].name,
        elevation=9999,
        mountain_range_id=db_peaks[0].mountain_range_id,
    )

    assert peak is None

    peak = await test_repository.get_by_name_elevation_and_mountain_range(
        peak_name=db_peaks[0].name,
        elevation=db_peaks[0].elevation,
        mountain_range_id=9999,
    )

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
        (
            "near_rysy",
            {"name_filter": "rysy"},
            [
                {"name": "Rysy", "distance": 100.0},
            ],
        ),
        (
            "near_rysy",
            {"name_filter": "RYSY"},
            [
                {"name": "Rysy", "distance": 100.0},
            ],
        ),
        (
            "near_rysy",
            {"name_filter": "babia"},
            [
                {"name": "Babia Góra", "distance": 80000.0},
            ],
        ),
        (
            "near_rysy",
            {"name_filter": "śnieżka"},
            [
                {"name": "Śnieżka", "distance": 400000.0},
            ],
        ),
        (
            "near_rysy",
            {"name_filter": "nonexistent"},
            [],
        ),
        (
            "near_rysy",
            {
                "max_distance": 1000,
                "name_filter": "babia",
            },
            [],
        ),
        (
            "near_rysy",
            {
                "max_distance": 100000,
                "name_filter": "babia",
            },
            [
                {"name": "Babia Góra", "distance": 80000.0},
            ],
        ),
    ],
)
async def test_get_nearest_parametrized(
    test_repository, db_peaks, coords_map, coords_key, params, expected_results
):
    """Test finding nearest peaks with various parameters"""
    lat, lng = coords_map[coords_key]

    results = await test_repository.get_nearest(lat=lat, lng=lng, **params)

    assert len(results) == len(expected_results)

    for peak_with_distance, expected in zip(results, expected_results):
        peak, distance = peak_with_distance.peak, peak_with_distance.distance
        assert peak.id is not None
        assert peak.name == expected["name"]
        assert peak.elevation is not None
        assert peak.lat is not None
        assert peak.lng is not None
        assert peak.mountain_range_id is not None
        assert isinstance(peak.mountain_range, MountainRange)

        assert isinstance(distance, float)
        assert 0 <= distance <= expected["distance"]

    distances = [item.distance for item in results]
    assert distances == sorted(distances)


@pytest.mark.asyncio
async def test_get_nearest_empty_database(test_repository, coords_map):
    """Test finding nearest peaks when database is empty"""
    lat, lng = coords_map["near_rysy"]

    results = await test_repository.get_nearest(lat=lat, lng=lng)

    assert results == []

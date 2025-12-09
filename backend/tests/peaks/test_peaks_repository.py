"""
Tests for the PeaksRepository
"""

import pytest

from src.mountain_ranges.models import MountainRange
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository
from src.sorting.models import SortParams
from tests.database.mixins import BaseRepositoryMixin


class TestPeaksRepository(BaseRepositoryMixin):
    repository_class = PeaksRepository
    model_class = Peak
    unique_keys = [("name", "elevation", "mountain_range_id")]

    @pytest.fixture()
    def db_items(self, db_peaks) -> list[Peak]:
        return db_peaks

    @pytest.fixture()
    def new_item(self, db_mountain_ranges) -> Peak:
        return Peak(
            name="New Peak",
            elevation=2500,
            mountain_range_id=db_mountain_ranges[0].id,
        )

    @pytest.fixture()
    def updated_item(self, db_mountain_ranges) -> Peak:
        return Peak(
            name="Updated Peak",
            elevation=2600,
            mountain_range_id=db_mountain_ranges[1].id,
        )

    @pytest.mark.asyncio
    async def test_get_all_without_location(self, test_repository, db_peaks):
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
    async def test_get_count_no_peaks(self, test_repository):
        count = await test_repository.get_count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_get_count(self, test_repository, db_peaks):
        count = await test_repository.get_count()

        assert count == 3

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count_no_peaks(self, test_repository, db_user):
        count = await test_repository.get_summited_by_user_count(db_user.id)

        assert count == 0

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count_no_photos(
        self, test_repository, db_user, db_peaks
    ):
        count = await test_repository.get_summited_by_user_count(db_user.id)

        assert count == 0

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count(
        self, test_repository, db_user, db_peaks, db_photos
    ):
        count = await test_repository.get_summited_by_user_count(db_user.id)

        assert count == 2

    @pytest.mark.asyncio
    async def test_search_no_peaks(self, test_repository, coords_map):
        """Test searching nearest peaks when database is empty"""
        sort_params = SortParams()

        results = await test_repository.search(sort_params=sort_params)

        assert results == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "params,expected_results",
        [
            ({}, ["Rysy", "Śnieżka", "Babia Góra"]),
            ({"limit": 2}, ["Rysy", "Śnieżka"]),
            (
                {"sort_params": SortParams(sort_by="elevation", order="desc")},
                ["Rysy", "Babia Góra", "Śnieżka"],
            ),
            ({"name_filter": "rysy"}, ["Rysy"]),
            ({"name_filter": "BABIA"}, ["Babia Góra"]),
            ({"name_filter": "śnieżka"}, ["Śnieżka"]),
            ({"name_filter": "nonexistent"}, []),
        ],
    )
    async def test_search_parametrized(
        self, test_repository, db_peaks, params, expected_results
    ):
        """Test searching peaks with various parameters"""
        results = await test_repository.search(**params)

        assert len(results) == len(expected_results)

        for peak, expected_name in zip(results, expected_results):
            assert peak.id is not None
            assert peak.name == expected_name
            assert isinstance(peak.mountain_range, MountainRange)

        result_names = [peak.name for peak in results]
        assert result_names == expected_results

    @pytest.mark.asyncio
    async def test_find_nearby_no_peaks(self, test_repository, coords_map):
        """Test finding nearest peaks when database is empty"""
        lat, lng = coords_map["near_rysy"]

        results = await test_repository.find_nearby(lat=lat, lng=lng)

        assert results == []

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
    async def test_find_nearby_parametrized(
        self,
        test_repository,
        db_peaks,
        coords_map,
        coords_key,
        params,
        expected_results,
    ):
        """Test finding nearest peaks with various parameters"""
        lat, lng = coords_map[coords_key]

        results = await test_repository.find_nearby(lat=lat, lng=lng, **params)

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

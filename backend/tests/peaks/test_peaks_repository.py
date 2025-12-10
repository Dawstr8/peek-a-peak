"""
Tests for the PeaksRepository
"""

import pytest
from sqlalchemy.exc import IntegrityError

from src.mountain_ranges.models import MountainRange
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from src.users.repository import UsersRepository
from tests.database.mixins import BaseRepositoryMixin


class TestPeaksRepository(BaseRepositoryMixin[Peak, PeaksRepository]):
    repository_class = PeaksRepository
    model_class = Peak
    unique_keys = [("name", "elevation", "mountain_range_id")]

    items_fixture = "peaks"

    @pytest.fixture()
    def test_users_repository(self, test_db) -> UsersRepository:
        return UsersRepository(test_db)

    @pytest.fixture()
    def test_photos_repository(self, test_db) -> PhotosRepository:
        return PhotosRepository(test_db)

    @pytest.mark.asyncio
    async def test_save_all_unique_constraint_violation_multiple_fields(
        self, test_repository, items
    ):
        # Arrange
        [keys] = self.unique_keys
        db_item = await test_repository.save(items[0])

        item_to_save = self.model_class(
            **items[1].model_dump(), mountain_range_id=db_item.mountain_range.id
        )
        item_to_save_2 = self.model_class(**items[2].model_dump())

        for key in keys:
            setattr(item_to_save_2, key, getattr(item_to_save, key))

        # Act and Assert
        with pytest.raises(IntegrityError) as exc_info:
            await test_repository.save_all([item_to_save, item_to_save_2])

        assert getattr(exc_info.value.orig, "sqlstate") == "23505"

    @pytest.mark.asyncio
    async def test_get_all_without_location(self, test_repository, items):
        """Test retrieving peaks without location"""
        # Arrange
        db_peaks = await test_repository.save_all(items)
        mountain_range = db_peaks[0].mountain_range
        peak_without_location = Peak(
            name="No Location Peak",
            elevation=1200,
            mountain_range=mountain_range,
            location=None,
        )

        await test_repository.save(peak_without_location)

        # Act
        peaks = await test_repository.get_all_without_location()

        # Assert
        assert len(peaks) == 1
        assert any(peak.name == "No Location Peak" for peak in peaks)

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count_no_peaks(
        self, test_repository, users, test_users_repository
    ):
        # Arrange
        await test_users_repository.save(users[0])

        # Act
        count = await test_repository.get_summited_by_user_count(users[0].id)

        # Assert
        assert count == 0

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count_no_photos(
        self, test_repository, users, peaks, test_users_repository
    ):
        # Arrange
        user = users[0]
        await test_users_repository.save(user)
        await test_repository.save_all(peaks)

        # Act
        count = await test_repository.get_summited_by_user_count(user.id)

        # Assert
        assert count == 0

    @pytest.mark.asyncio
    async def test_get_summited_by_user_count(
        self, test_repository, photos, test_photos_repository
    ):
        # Arrange
        await test_photos_repository.save_all(photos)

        # Act
        count = await test_repository.get_summited_by_user_count(photos[0].owner_id)

        # Assert
        assert count == 2

    @pytest.mark.asyncio
    async def test_search_no_peaks(self, test_repository):
        # Arrange
        sort_params = SortParams()

        # Act
        results = await test_repository.search(sort_params=sort_params)

        # Assert
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
        self, test_repository, items, params, expected_results
    ):
        # Arrange
        await test_repository.save_all(items)

        # Act
        results = await test_repository.search(**params)

        # Assert
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
        # Arrange
        lat, lng = coords_map["near_rysy"]

        # Act
        results = await test_repository.find_nearby(lat=lat, lng=lng)

        # Assert
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
        items,
        coords_map,
        coords_key,
        params,
        expected_results,
    ):
        """Test finding nearest peaks with various parameters"""
        # Arrange
        await test_repository.save_all(items)
        lat, lng = coords_map[coords_key]

        # Act
        results = await test_repository.find_nearby(lat=lat, lng=lng, **params)

        # Assert
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

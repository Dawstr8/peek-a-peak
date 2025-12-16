"""
Tests for the PhotosRepository
"""

import pytest

from src.pagination.models import PaginationParams
from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from tests.database.mixins import BaseRepositoryMixin


class TestPhotosRepository(BaseRepositoryMixin[SummitPhoto, PhotosRepository]):
    repository_class = PhotosRepository
    model_class = SummitPhoto
    sort_by = "captured_at"
    has_owner = True

    items_fixture = "photos"

    @pytest.mark.asyncio
    async def test_get_by_owner_id(self, test_repository, items):
        """Test retrieving all summit photos"""
        # Arrange
        db_photos = await test_repository.save_all(items)
        owner = db_photos[0].owner

        # Act
        photos_paginated = await test_repository.get_by_owner_id(
            owner.id,
            sort_params=SortParams(sort_by=None, order=None),
            pagination_params=PaginationParams(page=1, per_page=10),
        )

        # Assert
        assert photos_paginated.total == 3
        assert photos_paginated.page == 1
        assert photos_paginated.per_page == 10

        photos = photos_paginated.items
        assert len(photos) == 3

        photo_ids = [photo.id for photo in photos]
        assert db_photos[0].id in photo_ids
        assert db_photos[1].id in photo_ids

        first_photo = next(photo for photo in photos if photo.id == db_photos[0].id)
        assert first_photo.file_name == db_photos[0].file_name
        assert first_photo.peak_id == db_photos[0].peak_id
        assert first_photo.peak is not None
        assert first_photo.peak.id == db_photos[0].peak_id

    @pytest.mark.asyncio
    async def test_get_by_owner_id_with_sorting(self, test_repository, items):
        # Arrange
        db_photos = await test_repository.save_all(items)
        owner = db_photos[0].owner
        pagination_params = PaginationParams(page=1, per_page=10)

        sort_params1 = SortParams(sort_by="captured_at", order="asc")
        sort_params2 = SortParams(sort_by="captured_at", order="desc")

        # Act
        photos_asc_paginated = await test_repository.get_by_owner_id(
            owner_id=owner.id,
            sort_params=sort_params1,
            pagination_params=pagination_params,
        )
        photos_desc_paginated = await test_repository.get_by_owner_id(
            owner_id=owner.id,
            sort_params=sort_params2,
            pagination_params=pagination_params,
        )

        # Assert
        photos_asc = photos_asc_paginated.items
        photos_desc = photos_desc_paginated.items

        assert len(photos_asc) == 3
        assert len(photos_desc) == 3
        assert photos_asc[0].id != photos_desc[0].id

    @pytest.mark.asyncio
    async def test_get_locations_by_owner_id(self, test_repository, items):
        """Test retrieving summit photo locations by owner ID"""
        # Arrange
        db_photos = await test_repository.save_all(items)
        owner = db_photos[0].owner

        # Act
        photos_locations = await test_repository.get_locations_by_owner_id(owner.id)

        # Assert
        assert len(photos_locations) == 2

        for location in photos_locations:
            assert location.id is not None
            assert location.lat is not None
            assert location.lng is not None
            assert location.alt is not None

    @pytest.mark.asyncio
    async def test_get_dates_by_owner_id(self, test_repository, items):
        """Test retrieving summit photo dates by owner ID"""
        # Arrange
        db_photos = await test_repository.save_all(items)
        owner = db_photos[0].owner

        # Act
        photos_dates = await test_repository.get_dates_by_owner_id(owner.id)

        # Assert
        assert len(photos_dates) == 3

        for date in photos_dates:
            assert date.id is not None
            assert date.captured_at is not None

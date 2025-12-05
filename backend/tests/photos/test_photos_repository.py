"""
Tests for the PhotosRepository
"""

from datetime import datetime, timezone

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.pagination.models import PaginationParams
from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from tests.database.mixins import BaseRepositoryMixin


class TestPhotosRepository(BaseRepositoryMixin):
    model_class = SummitPhoto
    sort_by = "captured_at"

    @pytest.fixture()
    def test_repository(self, test_db: AsyncSession) -> PhotosRepository:
        return PhotosRepository(test_db)

    @pytest.fixture()
    def db_items(self, db_photos) -> list[SummitPhoto]:
        return db_photos

    @pytest.fixture()
    def new_item(self, db_user, db_peaks) -> SummitPhoto:
        return SummitPhoto(
            owner_id=db_user.id,
            file_name="new_photo.jpg",
            captured_at=datetime(2025, 10, 5, 9, 0, tzinfo=timezone.utc),
            location="POINT(19.5295 49.5730)",
            alt=1720,
            peak_id=db_peaks[0].id,
        )

    @pytest.mark.asyncio
    async def test_get_by_owner_id(self, test_repository, db_photos, db_user):
        """Test retrieving all summit photos"""
        photos_paginated = await test_repository.get_by_owner_id(
            db_user.id,
            sort_params=SortParams(sort_by=None, order=None),
            pagination_params=PaginationParams(page=1, per_page=10),
        )

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
    async def test_get_by_owner_id_with_sorting(
        self, test_repository, db_photos, db_user
    ):
        owner_id = db_user.id
        pagination_params = PaginationParams(page=1, per_page=10)

        sort_params1 = SortParams(sort_by="captured_at", order="asc")
        sort_params2 = SortParams(sort_by="captured_at", order="desc")

        """Test retrieving all summit photos with sorting parameters"""
        photos_asc_paginated = await test_repository.get_by_owner_id(
            owner_id=owner_id,
            sort_params=sort_params1,
            pagination_params=pagination_params,
        )
        photos_desc_paginated = await test_repository.get_by_owner_id(
            owner_id=owner_id,
            sort_params=sort_params2,
            pagination_params=pagination_params,
        )

        photos_asc = photos_asc_paginated.items
        photos_desc = photos_desc_paginated.items

        assert len(photos_asc) == 3
        assert len(photos_desc) == 3
        assert photos_asc[0].id != photos_desc[0].id

    @pytest.mark.asyncio
    async def test_get_locations_by_owner_id(self, test_repository, db_photos, db_user):
        """Test retrieving summit photo locations by owner ID"""
        photos_locations = await test_repository.get_locations_by_owner_id(db_user.id)

        assert len(photos_locations) == 2

        for location in photos_locations:
            assert location.id is not None
            assert location.lat is not None
            assert location.lng is not None
            assert location.alt is not None

    @pytest.mark.asyncio
    async def test_get_dates_by_owner_id(self, test_repository, db_photos, db_user):
        """Test retrieving summit photo dates by owner ID"""
        photos_dates = await test_repository.get_dates_by_owner_id(db_user.id)

        assert len(photos_dates) == 3

        for date in photos_dates:
            assert date.id is not None
            assert date.captured_at is not None

    @pytest.mark.asyncio
    async def test_delete(self, test_repository, db_photos):
        """Test deleting a summit photo"""
        photo_id = db_photos[0].id
        photo = await test_repository.get_by_id(photo_id)
        assert photo is not None

        result = await test_repository.delete(photo_id)
        assert result is True

        photo = await test_repository.get_by_id(photo_id)
        assert photo is None

    @pytest.mark.asyncio
    async def test_delete_non_existent(self, test_repository):
        """Test deleting a non-existent summit photo"""
        result = await test_repository.delete(999999)

        assert result is False

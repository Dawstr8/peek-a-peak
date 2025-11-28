"""
Tests for the PhotosRepository
"""

from datetime import datetime, timezone

import pytest
from sqlmodel import select

from src.models import SortParams
from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository


@pytest.fixture()
def test_photos_repository(test_db):
    """Create a PhotosRepository instance for testing"""
    return PhotosRepository(test_db)


@pytest.mark.asyncio
async def test_save(test_photos_repository, db_peaks, db_user):
    """Test saving a new summit photo"""
    new_photo = SummitPhoto(
        owner_id=db_user.id,
        file_name="new_photo.jpg",
        captured_at=datetime(2025, 10, 5, 9, 0, tzinfo=timezone.utc),
        location="POINT(19.5295 49.5730)",
        alt=1720,
        peak_id=db_peaks[0].id,
    )

    saved_photo = await test_photos_repository.save(new_photo)

    assert saved_photo.id is not None
    assert saved_photo.file_name == "new_photo.jpg"
    assert saved_photo.captured_at == datetime(2025, 10, 5, 9, 0, tzinfo=timezone.utc)
    assert saved_photo.alt == 1720
    assert saved_photo.peak == db_peaks[0]
    assert saved_photo.peak.id == db_peaks[0].id


@pytest.mark.asyncio
async def test_get_by_id(test_photos_repository, db_photos):
    """Test retrieving a summit photo by ID"""
    photo_id = db_photos[0].id

    photo = await test_photos_repository.get_by_id(photo_id)

    assert photo is not None
    assert photo.file_name == db_photos[0].file_name
    assert photo.peak_id == db_photos[0].peak_id
    assert photo.peak is not None
    assert photo.peak.id == db_photos[0].peak_id


@pytest.mark.asyncio
async def test_get_by_id_non_existent(test_photos_repository):
    """Test retrieving a non-existent summit photo by ID"""
    non_existent_photo = await test_photos_repository.get_by_id(999999)

    assert non_existent_photo is None


@pytest.mark.asyncio
async def test_get_all(test_photos_repository, db_photos):
    """Test retrieving all summit photos"""
    photos = await test_photos_repository.get_all()

    assert photos is not None
    assert len(photos) == len(db_photos)

    photo_ids = [photo.id for photo in photos]
    assert db_photos[0].id in photo_ids
    assert db_photos[1].id in photo_ids
    assert db_photos[2].id in photo_ids

    first_photo = next(photo for photo in photos if photo.id == db_photos[0].id)
    assert first_photo.file_name == db_photos[0].file_name
    assert first_photo.peak_id == db_photos[0].peak_id
    assert first_photo.peak is not None
    assert first_photo.peak.id == db_photos[0].peak_id


@pytest.mark.asyncio
async def test_get_all_with_sorting(test_photos_repository, db_photos):
    """Test retrieving all summit photos with sorting parameters"""
    photos_asc = await test_photos_repository.get_all(
        sort_params=SortParams(sort_by="captured_at", order="asc")
    )
    photos_desc = await test_photos_repository.get_all(
        sort_params=SortParams(sort_by="captured_at", order="desc")
    )

    assert len(photos_asc) == len(db_photos)
    assert len(photos_desc) == len(db_photos)
    assert photos_asc[0].id != photos_desc[0].id


@pytest.mark.asyncio
async def test_get_by_owner_id(test_photos_repository, db_photos, db_user):
    """Test retrieving all summit photos"""
    photos = await test_photos_repository.get_by_owner_id(db_user.id)

    assert photos is not None
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
async def test_get_by_owner_id_with_sorting(test_photos_repository, db_photos, db_user):
    """Test retrieving all summit photos with sorting parameters"""
    photos_asc = await test_photos_repository.get_by_owner_id(
        owner_id=db_user.id, sort_params=SortParams(sort_by="captured_at", order="asc")
    )
    photos_desc = await test_photos_repository.get_by_owner_id(
        owner_id=db_user.id, sort_params=SortParams(sort_by="captured_at", order="desc")
    )

    assert len(photos_asc) == 3
    assert len(photos_desc) == 3
    assert photos_asc[0].id != photos_desc[0].id


@pytest.mark.asyncio
async def test_get_locations_by_owner_id(test_photos_repository, db_photos, db_user):
    """Test retrieving summit photo locations by owner ID"""
    photos_locations = await test_photos_repository.get_locations_by_owner_id(
        db_user.id
    )

    assert len(photos_locations) == 2

    for location in photos_locations:
        assert location.id is not None
        assert location.lat is not None
        assert location.lng is not None
        assert location.alt is not None


@pytest.mark.asyncio
async def test_get_dates_by_owner_id(test_photos_repository, db_photos, db_user):
    """Test retrieving summit photo dates by owner ID"""
    photos_dates = await test_photos_repository.get_dates_by_owner_id(db_user.id)

    assert len(photos_dates) == 3

    for date in photos_dates:
        assert date.id is not None
        assert date.captured_at is not None


@pytest.mark.asyncio
async def test_delete(test_photos_repository, db_photos):
    """Test deleting a summit photo"""
    photo_id = db_photos[0].id
    photo = await test_photos_repository.get_by_id(photo_id)
    assert photo is not None

    result = await test_photos_repository.delete(photo_id)
    assert result is True

    photo = await test_photos_repository.get_by_id(photo_id)
    assert photo is None


@pytest.mark.asyncio
async def test_delete_non_existent(test_photos_repository):
    """Test deleting a non-existent summit photo"""
    result = await test_photos_repository.delete(999999)

    assert result is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_params",
    [
        (None),
        (SortParams(sort_by="invalid_column", order="asc")),
    ],
)
async def test_apply_sorting_with_invalid_or_missing_params(
    test_photos_repository, db_photos, sort_params: SortParams
):
    statement = select(SummitPhoto)

    result_statement = test_photos_repository._apply_sorting(
        statement, sort_params=sort_params
    )

    photos = (await test_photos_repository.db.exec(result_statement)).all()
    assert len(photos) == len(db_photos)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_params, expected_reversed",
    [
        (SortParams(sort_by="captured_at", order=None), False),
        (SortParams(sort_by="captured_at", order="asc"), False),
        (SortParams(sort_by="captured_at", order="desc"), True),
        (SortParams(sort_by="uploaded_at", order=None), False),
    ],
)
async def test_apply_sorting_with_valid_params(
    test_photos_repository, db_photos, sort_params: SortParams, expected_reversed: bool
):
    statement = select(SummitPhoto)

    result_statement = test_photos_repository._apply_sorting(
        statement, sort_params=sort_params
    )

    photos = (await test_photos_repository.db.exec(result_statement)).all()
    fields = [
        getattr(p, sort_params.sort_by)
        for p in photos
        if getattr(p, sort_params.sort_by) is not None
    ]

    assert fields == sorted(fields, reverse=expected_reversed)

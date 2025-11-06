"""
Tests for the PhotosRepository
"""

from datetime import datetime

import pytest

from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository


@pytest.fixture()
def test_photos_repository(test_db):
    """Create a PhotosRepository instance for testing"""
    return PhotosRepository(test_db)


def test_save(test_photos_repository, test_peaks, db_user):
    """Test saving a new summit photo"""
    new_photo = SummitPhoto(
        owner_id=db_user.id,
        file_name="new_photo.jpg",
        captured_at=datetime(2025, 10, 5, 9, 0),
        latitude=49.5730,
        longitude=19.5295,
        altitude=1720,
        distance_to_peak=3.8,
        peak_id=test_peaks[0].id,
    )

    saved_photo = test_photos_repository.save(new_photo)

    assert saved_photo.id is not None
    assert saved_photo.file_name == "new_photo.jpg"
    assert saved_photo.captured_at == datetime(2025, 10, 5, 9, 0)
    assert saved_photo.latitude == 49.5730
    assert saved_photo.longitude == 19.5295
    assert saved_photo.altitude == 1720
    assert saved_photo.distance_to_peak == 3.8
    assert saved_photo.peak == test_peaks[0]
    assert saved_photo.peak.id == test_peaks[0].id


def test_get_by_id(test_photos_repository, db_photos):
    """Test retrieving a summit photo by ID"""
    photo_id = db_photos[0].id

    photo = test_photos_repository.get_by_id(photo_id)

    assert photo is not None
    assert photo.file_name == db_photos[0].file_name
    assert photo.distance_to_peak == db_photos[0].distance_to_peak
    assert photo.peak_id == db_photos[0].peak_id
    assert photo.peak is not None
    assert photo.peak.id == db_photos[0].peak_id


def test_get_by_id_non_existent(test_photos_repository):
    """Test retrieving a non-existent summit photo by ID"""
    non_existent_photo = test_photos_repository.get_by_id(999999)

    assert non_existent_photo is None


def test_get_all(test_photos_repository, db_photos):
    """Test retrieving all summit photos"""
    photos = test_photos_repository.get_all()

    assert photos is not None
    assert len(photos) == 2

    photo_ids = [photo.id for photo in photos]
    assert db_photos[0].id in photo_ids
    assert db_photos[1].id in photo_ids

    first_photo = next(photo for photo in photos if photo.id == db_photos[0].id)
    assert first_photo.file_name == db_photos[0].file_name
    assert first_photo.distance_to_peak == db_photos[0].distance_to_peak
    assert first_photo.peak_id == db_photos[0].peak_id
    assert first_photo.peak is not None
    assert first_photo.peak.id == db_photos[0].peak_id


def test_get_all_sorted_by_captured_at_asc(test_photos_repository, db_photos):
    """Test retrieving all summit photos sorted by captured_at ascending"""
    photos = test_photos_repository.get_all(sort_by="captured_at", order="asc")

    assert photos is not None
    assert len(photos) == 2

    captured_times = [
        photo.captured_at for photo in photos if photo.captured_at is not None
    ]
    assert captured_times == sorted(captured_times)


def test_get_all_sorted_by_captured_at_desc(test_photos_repository, db_photos):
    """Test retrieving all summit photos sorted by captured_at descending"""
    photos = test_photos_repository.get_all(sort_by="captured_at", order="desc")

    assert photos is not None
    assert len(photos) == 2

    captured_times = [
        photo.captured_at for photo in photos if photo.captured_at is not None
    ]
    assert captured_times == sorted(captured_times, reverse=True)


def test_delete(test_photos_repository, db_photos):
    """Test deleting a summit photo"""
    photo_id = db_photos[0].id
    photo = test_photos_repository.get_by_id(photo_id)
    assert photo is not None

    result = test_photos_repository.delete(photo_id)
    assert result is True

    photo = test_photos_repository.get_by_id(photo_id)
    assert photo is None


def test_delete_non_existent(test_photos_repository):
    """Test deleting a non-existent summit photo"""
    result = test_photos_repository.delete(999999)
    assert result is False

"""
Tests for the PhotosService
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile

from src.photos.models import SummitPhotoCreate
from src.photos.service import PhotosService
from src.uploads.service import UploadsService


@pytest.fixture
def mock_uploads_service():
    """Create a mock upload service"""
    service = AsyncMock(spec=UploadsService)
    service.save_file.return_value = "/uploads/test-photo.jpg"
    service.delete_file.return_value = True
    return service


@pytest.fixture
def photos_service(
    mock_uploads_service,
    mock_photos_repository,
    mock_users_repository,
):
    """Create a PhotosService with mocked dependencies"""
    return PhotosService(
        mock_uploads_service,
        mock_photos_repository,
        mock_users_repository,
    )


@pytest.fixture
def mock_file():
    """Create a mock file upload"""
    file = AsyncMock(spec=UploadFile)
    file.filename = "test-photo.jpg"
    file.content_type = "image/jpeg"
    return file


@pytest.mark.asyncio
async def test_upload_photo_with_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
    coords_map,
    mock_user,
):
    """Test uploading a photo with provided metadata"""
    summit_photo_create = SummitPhotoCreate(
        captured_at=datetime(2025, 10, 6, 14, 30, 0, tzinfo=timezone.utc),
        lat=coords_map["near_rysy"][0],
        lng=coords_map["near_rysy"][1],
        alt=2450.0,
        peak_id=1,
    )

    result = await photos_service.upload_photo(
        mock_file, summit_photo_create, mock_user
    )

    assert result.id == 1
    assert result.owner_id == mock_user.id
    assert result.file_name == mock_file.filename
    assert result.peak_id == 1
    assert result.captured_at == datetime(2025, 10, 6, 14, 30, 0, tzinfo=timezone.utc)
    assert result.alt == 2450.0

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_photo_without_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
    mock_user,
):
    """Test uploading a photo without any metadata"""
    summit_photo_create = SummitPhotoCreate()

    result = await photos_service.upload_photo(
        mock_file, summit_photo_create, mock_user
    )

    assert result.id == 1
    assert result.owner_id == mock_user.id
    assert result.file_name == mock_file.filename
    assert result.peak_id is None
    assert result.captured_at is None
    assert result.alt is None
    assert result.lat is None
    assert result.lng is None

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_photo_with_partial_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
    mock_user,
):
    """Test uploading a photo with only some metadata fields"""
    summit_photo_create = SummitPhotoCreate(
        captured_at=datetime(2025, 10, 6, 16, 45, 20, tzinfo=timezone.utc),
        alt=1500.0,
    )

    result = await photos_service.upload_photo(
        mock_file, summit_photo_create, mock_user
    )

    assert result.id == 1
    assert result.owner_id == mock_user.id
    assert result.file_name == mock_file.filename
    assert result.peak_id is None
    assert result.captured_at == datetime(2025, 10, 6, 16, 45, 20, tzinfo=timezone.utc)
    assert result.alt == 1500.0
    assert result.lat is None
    assert result.lng is None

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_photo_by_id(photos_service, mock_photos_repository, mock_photo):
    """Test getting a photo by ID"""
    photo_id = mock_photo.id

    result = await photos_service.get_photo_by_id(photo_id)

    assert result == mock_photo
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_photo_by_id_not_found(photos_service, mock_photos_repository):
    """Test getting a photo by ID when it doesn't exist"""
    photo_id = 999

    result = await photos_service.get_photo_by_id(photo_id)

    assert result is None
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_all_photos(photos_service, mock_photos_repository, mock_photos):
    """Test getting all photos"""
    result = await photos_service.get_all_photos()

    assert result == mock_photos
    mock_photos_repository.get_all.assert_called_once_with(sort_params=None)


@pytest.mark.asyncio
async def test_get_photos_by_user(
    photos_service,
    mock_users_repository,
    mock_photos_repository,
    mock_photos,
    mock_user,
):
    """Test getting photos by user"""
    user_id = mock_user.id
    username = mock_user.username

    result = await photos_service.get_photos_by_user(username)

    expected_photos = [photo for photo in mock_photos if photo.owner_id == user_id]
    assert result == expected_photos
    mock_users_repository.get_by_username.assert_called_once_with(username)
    mock_photos_repository.get_by_owner_id.assert_called_once_with(
        user_id, sort_params=None
    )


@pytest.mark.asyncio
async def test_delete_photo_success(
    photos_service, mock_uploads_service, mock_photos_repository, mock_photo
):
    """Test deleting a photo successfully"""
    photo_id = mock_photo.id
    result = await photos_service.delete_photo(photo_id)

    assert result is True
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_uploads_service.delete_file.assert_called_once_with(mock_photo.file_name)
    mock_photos_repository.delete.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_delete_photo_failure_no_file(
    photos_service, mock_uploads_service, mock_photos_repository, mock_photo
):
    """Test deleting a photo when the file deletion fails"""
    photo_id = mock_photo.id
    mock_uploads_service.delete_file.return_value = False

    result = await photos_service.delete_photo(photo_id)

    assert result is False
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_uploads_service.delete_file.assert_called_once_with(mock_photo.file_name)
    mock_photos_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_photo_failure_not_found(photos_service, mock_photos_repository):
    """Test deleting a photo that doesn't exist"""
    photo_id = 999

    result = await photos_service.delete_photo(photo_id)

    assert result is False
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_photos_repository.delete.assert_not_called()

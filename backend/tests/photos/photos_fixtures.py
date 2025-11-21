"""
Photo fixtures for testing across different test types: unit, integration, and e2e
"""

import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository
from tests.auth.auth_fixtures import temporary_login


@pytest.fixture
def mock_photos() -> list[SummitPhoto]:
    """
    Returns a list of mock Photo objects for unit tests.
    This photos are not persisted anywhere and are useful for pure unit tests
    that don't need database interaction.
    """
    return [
        SummitPhoto(
            id=1,
            file_name="test-photo-1.jpg",
            location="POINT(20.0880 49.1794)",
        ),
        SummitPhoto(
            id=2,
            file_name="test-photo-2.jpg",
            location="POINT(20.0880 49.1794)",
        ),
    ]


@pytest.fixture
def mock_photo(mock_photos) -> SummitPhoto:
    """
    Returns a mock Photo object for unit tests.
    This photo is not persisted anywhere and is useful for pure unit tests
    that don't need database interaction.
    """
    return mock_photos[0]


@pytest.fixture
def mock_photos_repository(
    mock_photo: SummitPhoto, mock_photos: list[SummitPhoto]
) -> PhotosRepository:
    """
    Returns a mock PhotosRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    repo = MagicMock(spec=PhotosRepository)

    async def save(photo):
        photo.id = 1
        return photo

    async def get_by_id(photo_id):
        return mock_photo if photo_id in [photo.id for photo in mock_photos] else None

    async def get_all(sort_by=None, order=None):
        return mock_photos

    async def get_by_owner_id(owner_id, sort_by=None, order=None):
        return [photo for photo in mock_photos if photo.owner_id == owner_id]

    repo.save = AsyncMock(side_effect=save)
    repo.get_by_id = AsyncMock(side_effect=get_by_id)
    repo.get_by_owner_id = AsyncMock(side_effect=get_by_owner_id)
    repo.get_all = AsyncMock(side_effect=get_all)
    repo.delete = AsyncMock(return_value=True)

    return repo


@pytest_asyncio.fixture
async def db_photos(test_db, db_users, db_peaks, coords_map) -> list[SummitPhoto]:
    """
    Creates and returns a list of real photos in the test database.
    This fixture is useful for integration tests that need
    real photos in the database.
    """
    photos_repo = PhotosRepository(test_db)

    photos = [
        SummitPhoto(
            owner_id=db_users[0].id,
            file_name="test1.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 9, 30, 10, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_rysy'][1]} {coords_map['near_rysy'][0]})",
            alt=2495,
            peak_id=db_peaks[0].id,
        ),
        SummitPhoto(
            owner_id=db_users[0].id,
            file_name="test2.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 10, 1, 11, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_sniezka'][1]} {coords_map['near_sniezka'][0]})",
            alt=1600,
            peak_id=db_peaks[1].id,
        ),
        SummitPhoto(
            owner_id=db_users[1].id,
            file_name="test3.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 11, 1, 11, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_sniezka'][1]} {coords_map['near_sniezka'][0]})",
            alt=1600,
            peak_id=db_peaks[1].id,
        ),
    ]

    saved_photos = []
    for photo in photos:
        saved_photo = await photos_repo.save(photo)
        saved_photos.append(saved_photo)

    return saved_photos


@pytest_asyncio.fixture
async def e2e_photos(
    client_with_db, registered_users, db_peaks, coords_map
) -> list[dict]:
    """
    Creates and returns a list of photos through the API endpoints.
    This fixture is useful for end-to-end tests that need real photos
    created through the full application stack.

    Returns a list of photo responses from the API.
    """
    photos_data = [
        [
            {
                "summit_photo_create": {
                    "captured_at": "2025-09-30T10:00:00Z",
                    "lat": coords_map["near_rysy"][0],
                    "lng": coords_map["near_rysy"][1],
                    "alt": 2495.0,
                    "peak_id": db_peaks[0].id,
                },
                "file": ("photo1.jpg", b"imagedata1", "image/jpeg"),
            },
            {
                "summit_photo_create": {
                    "captured_at": "2025-10-01T11:00:00Z",
                    "lat": coords_map["near_sniezka"][0],
                    "lng": coords_map["near_sniezka"][1],
                    "alt": 1602.0,
                },
                "file": ("photo2.jpg", b"imagedata2", "image/jpeg"),
            },
        ],
        [
            {
                "summit_photo_create": {
                    "captured_at": "2025-11-01T11:00:00Z",
                    "lat": coords_map["near_sniezka"][0],
                    "lng": coords_map["near_sniezka"][1],
                    "alt": 1602.0,
                },
                "file": ("photo3.jpg", b"imagedata3", "image/jpeg"),
            },
        ],
    ]

    created_photos = []
    for i in range(2):
        user = registered_users[i]
        photos = photos_data[i]
        async with temporary_login(client_with_db, user["username"], user["password"]):
            for photo in photos:
                response = await client_with_db.post(
                    "/api/photos",
                    files={"file": photo["file"]},
                    data={
                        "summit_photo_create": json.dumps(photo["summit_photo_create"])
                    },
                )

                created_photos.append(response.json())

    return created_photos


@pytest.fixture
def e2e_photo(e2e_photos) -> dict:
    """
    Returns a single photo created through the API endpoints.
    This fixture is useful for end-to-end tests that need a real photo
    created through the full application stack.

    Returns the first photo response from the API.
    """
    return e2e_photos[0]

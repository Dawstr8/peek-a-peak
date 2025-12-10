"""
Photo fixtures for testing across different test types: unit, integration, and e2e
"""

import json
from datetime import datetime, timezone

import pytest
import pytest_asyncio

from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository
from tests.auth.auth_fixtures import temporary_login
from tests.photos.mock_repository import MockPhotosRepository


@pytest.fixture
def photos(users, peaks, coords_map) -> list[SummitPhoto]:
    """
    Returns a list of Photo objects for unit tests.
    This photos are not persisted anywhere and are useful for pure unit tests
    that don't need database interaction.
    """
    return [
        SummitPhoto(
            owner=users[0],
            peak=peaks[0],
            file_name="test1.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 9, 30, 10, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_rysy'][1]} {coords_map['near_rysy'][0]})",
            alt=2495,
        ),
        SummitPhoto(
            owner=users[0],
            peak=peaks[1],
            file_name="test2.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 10, 1, 11, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_sniezka'][1]} {coords_map['near_sniezka'][0]})",
            alt=1600,
        ),
        SummitPhoto(
            owner=users[1],
            peak=peaks[1],
            file_name="test3.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 11, 1, 11, 0, tzinfo=timezone.utc),
            location=f"POINT({coords_map['near_sniezka'][1]} {coords_map['near_sniezka'][0]})",
            alt=1600,
        ),
        SummitPhoto(
            owner=users[0],
            peak=None,
            file_name="test4.jpg",
            uploaded_at=datetime.now(),
            captured_at=datetime(2025, 10, 1, 11, 0, tzinfo=timezone.utc),
            location=None,
            alt=None,
        ),
    ]


@pytest.fixture
def mock_photos(photos) -> list[SummitPhoto]:
    """
    Returns a list of mock Photo objects for unit tests.
    This photos are not persisted anywhere and are useful for pure unit tests
    that don't need database interaction.
    """
    for photo in photos:
        photo.id = 1

    return photos


@pytest.fixture
def mock_photo(mock_photos) -> SummitPhoto:
    """
    Returns a mock Photo object for unit tests.
    This photo is not persisted anywhere and is useful for pure unit tests
    that don't need database interaction.
    """
    return mock_photos[0]


@pytest.fixture
def mock_photos_repository(mock_photos: list[SummitPhoto]) -> PhotosRepository:
    """
    Returns a mock PhotosRepository for unit tests.
    This mock does not interact with a real database and is useful for pure unit tests
    that don't need database interaction.
    """
    return MockPhotosRepository(items=mock_photos).mock


@pytest_asyncio.fixture
async def db_photos(test_db, photos) -> list[SummitPhoto]:
    """
    Creates and returns a list of real photos in the test database.
    This fixture is useful for integration tests that need
    real photos in the database.
    """
    photos_repo = PhotosRepository(test_db)
    return await photos_repo.save_all(photos)


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
                "summitPhotoCreate": {
                    "capturedAt": "2025-09-30T10:00:00Z",
                    "lat": coords_map["near_rysy"][0],
                    "lng": coords_map["near_rysy"][1],
                    "alt": 2495.0,
                    "peak_id": db_peaks[0].id,
                },
                "file": ("photo1.jpg", b"imagedata1", "image/jpeg"),
            },
            {
                "summitPhotoCreate": {
                    "capturedAt": "2025-10-01T11:00:00Z",
                    "lat": coords_map["near_sniezka"][0],
                    "lng": coords_map["near_sniezka"][1],
                    "alt": 1602.0,
                },
                "file": ("photo2.jpg", b"imagedata2", "image/jpeg"),
            },
            {
                "summitPhotoCreate": {"capturedAt": "2025-10-01T11:00:00Z"},
                "file": ("photo4.jpg", b"imagedata4", "image/jpeg"),
            },
        ],
        [
            {
                "summitPhotoCreate": {
                    "capturedAt": "2025-11-01T11:00:00Z",
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
                    data={"summitPhotoCreate": json.dumps(photo["summitPhotoCreate"])},
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

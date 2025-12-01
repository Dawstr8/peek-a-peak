import json
import os
import re
from pathlib import Path

import pytest

from main import app
from src.models import SortParams
from src.photos import dependencies
from src.uploads.service import UploadsService
from src.uploads.services.local_storage import LocalFileStorage


@pytest.fixture(autouse=True)
def override_uploads_service(test_upload_dir):
    """Override the upload service dependency to isolate filesystem writes."""

    def _get_uploads_service():
        return UploadsService(LocalFileStorage(upload_dir=str(test_upload_dir)))

    app.dependency_overrides[dependencies.get_uploads_service] = _get_uploads_service
    yield
    app.dependency_overrides.pop(dependencies.get_uploads_service, None)


@pytest.mark.asyncio
async def test_get_all_photos_empty(client_with_db):
    """Test getting all photos when none exist"""
    resp = await client_with_db.get("/api/photos")

    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_all_photos(client_with_db, e2e_photos):
    """Test getting all photos"""
    resp = await client_with_db.get("/api/photos")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == len(e2e_photos)

    for photo in photos:
        assert "id" in photo
        assert "fileName" in photo


@pytest.mark.asyncio
async def test_get_all_photos_with_peaks(client_with_db, db_peaks, e2e_photos):
    """Test getting all photos includes peak information when assigned"""
    resp = await client_with_db.get("/api/photos")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == len(e2e_photos)

    photos_without_peak = [p for p in photos if p["peakId"] is None]
    photos_with_peak = [p for p in photos if p["peakId"] is not None]

    for photo_without_peak in photos_without_peak:
        assert photo_without_peak is not None
        assert photo_without_peak["peak"] is None

    for photo_with_peak in photos_with_peak:
        assert photo_with_peak is not None
        assert photo_with_peak["peak"] is not None
        assert photo_with_peak["peak"]["id"] == db_peaks[0].id
        assert photo_with_peak["peak"]["name"] == db_peaks[0].name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_params,expected_reversed",
    [
        (SortParams(sort_by="capturedAt", order=None), False),
        (SortParams(sort_by="capturedAt", order="asc"), False),
        (SortParams(sort_by="capturedAt", order="desc"), True),
        (SortParams(sort_by="uploadedAt", order=None), False),
    ],
)
async def test_get_all_photos_with_sorting_parameters(
    client_with_db, e2e_photos, sort_params: SortParams, expected_reversed: bool
):
    """Test getting all photos sorted by various parameters"""
    sort_by, order = sort_params.sort_by, sort_params.order

    resp = await client_with_db.get(f"/api/photos?sortBy={sort_by}&order={order}")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == len(e2e_photos)

    received_fields = [photo[sort_by] for photo in photos if photo[sort_by]]
    assert received_fields == sorted(received_fields, reverse=expected_reversed)


@pytest.mark.asyncio
async def test_upload_photo_requires_auth(client_with_db):
    """Test that uploading a photo requires authentication"""
    response = await client_with_db.post(
        "/api/photos",
        files={"file": ("photo.jpg", b"imagedata", "image/jpeg")},
        data={"summitPhotoCreate": "{}"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "captured_at,file,expected_status,expected_msg",
    [
        (
            None,
            ("summit.jpg", b"binaryimagedata", "image/jpeg"),
            422,
            "Field required",
        ),
        (
            "2025-10-06T14:30:00",
            ("summit.jpg", b"binaryimagedata", "image/jpeg"),
            422,
            "Value error, captured_at must be timezone-aware (include offset or tzinfo).",
        ),
        (
            "2025-10-06T14:30:00Z",
            ("notes.txt", b"not an image", "text/plain"),
            400,
            "File must be of type image/",
        ),
    ],
)
async def test_upload_photo_validation_errors_parametrized(
    client_with_db,
    logged_in_user,
    captured_at: str,
    file: tuple,
    expected_status: int,
    expected_msg: str,
):
    """Test upload photo validation errors with various invalid inputs"""
    summit_photo_create = {"capturedAt": captured_at} if captured_at else {}

    resp = await client_with_db.post(
        "/api/photos",
        files={"file": file},
        data={"summitPhotoCreate": json.dumps(summit_photo_create)},
    )

    assert resp.status_code == expected_status
    detail = resp.json()["detail"]

    if expected_status == 422:
        assert detail[0]["msg"] == expected_msg
    else:
        assert detail == expected_msg


@pytest.mark.asyncio
async def test_upload_photo_success(
    client_with_db, db_peaks, coords_map, logged_in_user
):
    """Test successful photo upload"""
    summit_photo_create = {
        "capturedAt": "2025-10-06T14:30:00Z",
        "lat": coords_map["near_rysy"][0],
        "lng": coords_map["near_rysy"][1],
        "alt": 2450.0,
        "peakId": db_peaks[0].id,
    }

    resp = await client_with_db.post(
        "/api/photos",
        files={"file": ("summit.jpg", b"binaryimagedata", "image/jpeg")},
        data={"summitPhotoCreate": json.dumps(summit_photo_create)},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] is not None
    assert data["fileName"] is not None
    assert data["capturedAt"] == summit_photo_create["capturedAt"]
    assert data["lat"] == summit_photo_create["lat"]
    assert data["lng"] == summit_photo_create["lng"]
    assert data["alt"] == summit_photo_create["alt"]

    assert data["peakId"] == summit_photo_create["peakId"]
    assert data["ownerId"] is not None

    assert re.search(r".+\.jpg$", data["fileName"])
    assert Path(f"test_uploads/{data['fileName']}").exists()


@pytest.mark.asyncio
async def test_get_photo_by_id(client_with_db, e2e_photo):
    """Test getting a specific photo by ID"""
    photo_id = e2e_photo["id"]

    get_resp = await client_with_db.get(f"/api/photos/{photo_id}")

    assert get_resp.status_code == 200
    photo_data = get_resp.json()

    assert photo_data["id"] == photo_id
    assert photo_data["fileName"] == e2e_photo["fileName"]


@pytest.mark.asyncio
async def test_get_photo_by_id_get_nonexistent_photo(client_with_db, logged_in_user):
    """Test getting a photo that doesn't exist"""
    id = 9999

    resp = await client_with_db.get(f"/api/photos/{id}")

    assert resp.status_code == 404
    assert resp.json()["detail"] == f"Photo with ID {id} not found"


@pytest.mark.asyncio
async def test_delete_photo_success(client_with_db, e2e_photo):
    """Test deleting a photo successfully"""
    photo_id = e2e_photo["id"]
    file_path = f"test_uploads/{e2e_photo['fileName']}"

    delete_resp = await client_with_db.delete(f"/api/photos/{photo_id}")

    assert delete_resp.status_code == 200
    assert delete_resp.json()["success"] is True
    assert not os.path.exists(file_path)


@pytest.mark.asyncio
async def test_delete_nonexistent_photo(client_with_db, logged_in_user):
    """Test deleting a photo that doesn't exist"""
    id = 9999

    resp = await client_with_db.delete(f"/api/photos/{id}")

    assert resp.status_code == 404
    assert resp.json()["detail"] == f"Photo with ID {id} not found"

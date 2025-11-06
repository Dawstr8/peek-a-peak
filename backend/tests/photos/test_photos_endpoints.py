import json
import os
import re
from pathlib import Path

import pytest

from main import app
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


def test_get_all_photos_empty(client_with_db):
    """Test getting all photos when none exist"""
    resp = client_with_db.get("/api/photos/")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_all_photos(client_with_db, e2e_photos):
    """Test getting all photos"""
    resp = client_with_db.get("/api/photos/")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    for photo in photos:
        assert "id" in photo
        assert "file_name" in photo


def test_get_all_photos_with_peaks(client_with_db, test_peaks, e2e_photos):
    """Test getting all photos includes peak information when assigned"""
    resp = client_with_db.get("/api/photos/")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    photo_without_peak = next((p for p in photos if p["peak_id"] is None), None)
    photo_with_peak = next((p for p in photos if p["peak_id"] is not None), None)

    assert photo_without_peak is not None
    assert photo_without_peak["peak"] is None

    assert photo_with_peak is not None
    assert photo_with_peak["peak"] is not None
    assert photo_with_peak["peak"]["id"] == test_peaks[0].id
    assert photo_with_peak["peak"]["name"] == test_peaks[0].name


def test_get_all_photos_sorted_by_captured_at_asc(client_with_db, e2e_photos):
    """Test getting all photos sorted by captured_at ascending"""
    resp = client_with_db.get("/api/photos/?sort_by=captured_at&order=asc")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    captured_times = [photo["captured_at"] for photo in photos if photo["captured_at"]]
    assert captured_times == sorted(captured_times)


def test_get_all_photos_sorted_by_captured_at_desc(client_with_db, e2e_photos):
    """Test getting all photos sorted by captured_at descending"""
    resp = client_with_db.get("/api/photos/?sort_by=captured_at&order=desc")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    captured_times = [photo["captured_at"] for photo in photos if photo["captured_at"]]
    assert captured_times == sorted(captured_times, reverse=True)


def test_get_all_photos_sorted_by_captured_at_default_order(client_with_db, e2e_photos):
    """Test getting all photos sorted by captured_at with default ascending order"""
    resp = client_with_db.get("/api/photos/?sort_by=captured_at")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    captured_times = [photo["captured_at"] for photo in photos if photo["captured_at"]]
    assert captured_times == sorted(captured_times)


def test_upload_photo_success(client_with_db, logged_in_user):
    """Test successful photo upload"""

    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("summit.jpg", b"binaryimagedata", "image/jpeg")},
        data={"summit_photo_create": "{}"},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] is not None
    assert re.search(r".+\.jpg$", data["file_name"])
    assert Path(f"test_uploads/{data['file_name']}").exists()


def test_upload_photo_requires_auth(client_with_db):
    """Test that uploading a photo requires authentication"""
    response = client_with_db.post(
        "/api/photos/",
        files={"file": ("photo.jpg", b"imagedata", "image/jpeg")},
        data={"summit_photo_create": "{}"},
    )

    assert response.status_code == 401


def test_upload_invalid_file_type(client_with_db, logged_in_user):
    """Test upload with invalid file type"""

    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("notes.txt", b"not an image", "text/plain")},
        data={"summit_photo_create": "{}"},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "File must be of type image/"


def test_upload_with_metadata(
    client_with_db,
    test_peaks,
    peak_coords,
    logged_in_user,
):
    """Test upload photo with metadata provided as JSON"""
    summit_photo_create = {
        "captured_at": "2025-10-06T14:30:00",
        "latitude": peak_coords["near_rysy"][0],
        "longitude": peak_coords["near_rysy"][1],
        "altitude": 2450.0,
        "peak_id": None,
    }

    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("mountain_photo.jpg", b"binaryimagedata", "image/jpeg")},
        data={"summit_photo_create": json.dumps(summit_photo_create)},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] is not None
    assert data["file_name"] is not None

    assert data["latitude"] == summit_photo_create["latitude"]
    assert data["longitude"] == summit_photo_create["longitude"]
    assert data["altitude"] == summit_photo_create["altitude"]

    assert data["peak_id"] == summit_photo_create["peak_id"]
    assert data["distance_to_peak"] is None


def test_upload_without_peak_id(
    client_with_db, test_peaks, peak_coords, logged_in_user
):
    """Test upload photo with GPS coordinates but no peak_id"""
    summit_photo_create = {
        "captured_at": "2025-10-06T14:30:00",
        "latitude": peak_coords["warsaw"][0],
        "longitude": peak_coords["warsaw"][1],
        "altitude": 120.0,
    }

    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("city_photo.jpg", b"binaryimagedata", "image/jpeg")},
        data={"summit_photo_create": json.dumps(summit_photo_create)},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] is not None
    assert data["file_name"] is not None

    assert data["latitude"] == peak_coords["warsaw"][0]
    assert data["longitude"] == peak_coords["warsaw"][1]
    assert data["altitude"] == 120.0

    assert data["peak_id"] is None
    assert data["distance_to_peak"] is None


def test_upload_without_gps_data(client_with_db, test_peaks, logged_in_user):
    """Test upload photo without GPS coordinates"""
    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("indoor_photo.jpg", b"binaryimagedata", "image/jpeg")},
        data={"summit_photo_create": "{}"},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] is not None
    assert data["file_name"] is not None

    assert data["latitude"] is None
    assert data["longitude"] is None
    assert data["altitude"] is None

    assert data["peak_id"] is None
    assert data["distance_to_peak"] is None


def test_get_photo_by_id(client_with_db, e2e_photo):
    """Test getting a specific photo by ID"""
    photo_id = e2e_photo["id"]

    get_resp = client_with_db.get(f"/api/photos/{photo_id}")

    assert get_resp.status_code == 200
    photo_data = get_resp.json()

    assert photo_data["id"] == photo_id
    assert photo_data["file_name"] == e2e_photo["file_name"]


def test_get_nonexistent_photo(client_with_db, logged_in_user):
    """Test getting a photo that doesn't exist"""
    resp = client_with_db.get("/api/photos/9999")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Photo not found"


def test_delete_photo_success(client_with_db, e2e_photo):
    """Test deleting a photo successfully"""
    photo_id = e2e_photo["id"]
    file_path = f"test_uploads/{e2e_photo['file_name']}"

    delete_resp = client_with_db.delete(f"/api/photos/{photo_id}")

    assert delete_resp.status_code == 200
    assert delete_resp.json()["success"] is True
    assert not os.path.exists(file_path)


def test_delete_nonexistent_photo(client_with_db, logged_in_user):
    """Test deleting a photo that doesn't exist"""
    resp = client_with_db.delete("/api/photos/9999")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Photo not found"

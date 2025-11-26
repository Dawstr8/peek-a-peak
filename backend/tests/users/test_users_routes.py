import pytest

from src.models import SortParams
from src.users.models import User

BASE_URL = "/api/users"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,url",
    [
        ("get", f"{BASE_URL}/username/photos"),
        ("get", f"{BASE_URL}/username/peaks/count"),
    ],
)
async def test_endpoints_require_auth(client_with_db, method, url):
    """Test that user endpoints require authentication"""
    resp = await getattr(client_with_db, method)(url)

    assert resp.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,url",
    [
        ("get", f"{BASE_URL}/username/photos"),
        ("get", f"{BASE_URL}/username/peaks/count"),
    ],
)
async def test_endpoints_forbidden_for_other_user(
    client_with_db, method, url, logged_in_user
):
    """Test that user endpoints are forbidden for other users"""
    url = url.replace("username", logged_in_user["username"] + "other")

    resp = await getattr(client_with_db, method)(url)

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Not authorized to access this resource"


@pytest.mark.asyncio
async def test_get_user_photos_for_user(client_with_db, e2e_photos, logged_in_user):
    """Test getting photos for a specific user"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/photos")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    for photo in photos:
        assert "id" in photo
        assert "fileName" in photo

    assert photos[0]["ownerId"] == photos[1]["ownerId"]


@pytest.mark.asyncio
async def test_get_user_photos_with_peaks(
    client_with_db, db_peaks, e2e_photos, logged_in_user
):
    """Test getting user photos includes peak information when assigned"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/photos")

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    photo_without_peak = next((p for p in photos if p["peakId"] is None), None)
    photo_with_peak = next((p for p in photos if p["peakId"] is not None), None)

    assert photo_without_peak is not None
    assert photo_without_peak["peak"] is None

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
async def test_get_user_photos_with_sorting_parameters(
    client_with_db,
    e2e_photos,
    logged_in_user: User,
    sort_params: SortParams,
    expected_reversed: bool,
):
    """Test getting user photos sorted by various parameters"""
    username = logged_in_user["username"]
    sort_by, order = sort_params.sort_by, sort_params.order

    resp = await client_with_db.get(
        f"{BASE_URL}/{username}/photos?sortBy={sort_by}&order={order}"
    )

    assert resp.status_code == 200
    photos = resp.json()
    assert len(photos) == 2

    received_fields = [photo[sort_by] for photo in photos if photo[sort_by]]
    assert received_fields == sorted(received_fields, reverse=expected_reversed)


@pytest.mark.asyncio
async def test_get_summited_peaks_count_for_user(
    client_with_db, db_peaks, e2e_photos, logged_in_user
):
    """Test getting summited peaks count for a specific user"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/peaks/count")

    assert resp.status_code == 200
    count = resp.json()
    assert count == 1

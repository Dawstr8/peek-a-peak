import pytest

from src.sorting.models import SortParams
from src.users.models import User

BASE_URL = "/api/users"


@pytest.mark.asyncio
async def test_check_user_access_granted(client_with_db, logged_in_user):
    """Test checking user access returns granted"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/access")

    assert resp.status_code == 200
    access_data = resp.json()
    assert access_data["access"] == "granted"


@pytest.mark.asyncio
async def test_get_user_success(client_with_db, logged_in_user):
    """Test getting user information successfully"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}")

    assert resp.status_code == 200
    user_data = resp.json()
    assert user_data["username"] == logged_in_user["username"]
    assert user_data["email"] == logged_in_user["email"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username_fn",
    [
        (lambda username: username),
        (lambda username: username.upper()),
    ],
)
async def test_get_user_photos_for_user(
    client_with_db, e2e_photos, logged_in_user, username_fn
):
    """Test getting photos for a specific user"""
    username = username_fn(logged_in_user["username"])

    paginated_resp = await client_with_db.get(f"{BASE_URL}/{username}/photos")

    assert paginated_resp.status_code == 200
    paginated_photos = paginated_resp.json()

    assert paginated_photos["total"] == 3
    assert paginated_photos["page"] == 1
    assert paginated_photos["perPage"] == 10

    photos = paginated_photos["items"]
    assert len(photos) == 3

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
    paginated_photos = resp.json()

    assert paginated_photos["total"] == 3
    assert paginated_photos["page"] == 1
    assert paginated_photos["perPage"] == 10

    photos = paginated_photos["items"]
    assert len(photos) == 3

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
        (SortParams(sort_by="createdAt", order=None), False),
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
    paginated_photos = resp.json()

    assert paginated_photos["total"] == 3
    assert paginated_photos["page"] == 1
    assert paginated_photos["perPage"] == 10

    photos = paginated_photos["items"]
    assert len(photos) == 3

    received_fields = [photo[sort_by] for photo in photos if photo[sort_by]]
    assert received_fields == sorted(received_fields, reverse=expected_reversed)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pagination_params,expected_ids",
    [
        ({"page": 1, "perPage": 2}, [2, 1]),
        ({"page": 2, "perPage": 2}, [0]),
        ({"page": 1, "perPage": 5}, [2, 1, 0]),
    ],
)
async def test_get_user_photos_with_pagination_parameters(
    client_with_db,
    e2e_photos,
    logged_in_user: User,
    pagination_params: dict,
    expected_ids: list,
):
    """Test getting user photos with pagination parameters"""
    username = logged_in_user["username"]
    sort_by = "capturedAt"
    order = "desc"
    page = pagination_params["page"]
    per_page = pagination_params["perPage"]

    resp = await client_with_db.get(
        f"{BASE_URL}/{username}/photos?page={page}&perPage={per_page}&sortBy={sort_by}&order={order}"
    )

    assert resp.status_code == 200
    paginated_photos = resp.json()

    assert paginated_photos["total"] == 3
    assert paginated_photos["page"] == page
    assert paginated_photos["perPage"] == per_page

    photos = paginated_photos["items"]
    e2e_photos_in_order = [e2e_photos[i] for i in expected_ids]
    for photo, expected_photo in zip(photos, e2e_photos_in_order):
        assert photo["id"] == expected_photo["id"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username_fn",
    [
        (lambda username: username),
        (lambda username: username.upper()),
    ],
)
async def test_get_summited_peaks_count_for_user(
    client_with_db, db_peaks, e2e_photos, logged_in_user, username_fn
):
    """Test getting summited peaks count for a specific user"""
    username = username_fn(logged_in_user["username"])

    resp = await client_with_db.get(f"{BASE_URL}/{username}/peaks/count")

    assert resp.status_code == 200
    count = resp.json()
    assert count == 1


@pytest.mark.asyncio
async def test_get_user_photo_locations(client_with_db, e2e_photos, logged_in_user):
    """Test getting photo locations for a specific user"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/photos/locations")

    assert resp.status_code == 200
    locations = resp.json()
    assert len(locations) == 2

    for location in locations:
        assert location["id"] is not None
        assert location["lat"] is not None
        assert location["lng"] is not None
        assert location["alt"] is not None


@pytest.mark.asyncio
async def test_get_user_photo_dates(client_with_db, e2e_photos, logged_in_user):
    """Test getting photo dates for a specific user"""
    username = logged_in_user["username"]

    resp = await client_with_db.get(f"{BASE_URL}/{username}/photos/dates")

    assert resp.status_code == 200
    dates = resp.json()
    assert len(dates) == 3

    for date in dates:
        assert date["id"] is not None
        assert date["capturedAt"] is not None


@pytest.mark.asyncio
async def test_update_user_success(client_with_db, logged_in_user):
    """Test updating user information successfully"""
    username = logged_in_user["username"]
    update_data = {
        "isPrivate": True,
    }

    resp = await client_with_db.patch(f"{BASE_URL}/{username}", json=update_data)

    assert resp.status_code == 200
    updated_user = resp.json()
    assert updated_user["isPrivate"] == update_data["isPrivate"]

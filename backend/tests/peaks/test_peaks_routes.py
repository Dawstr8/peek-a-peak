import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_peaks(client_with_db: AsyncClient, db_peaks):
    """Test getting all peaks"""
    response = await client_with_db.get("/api/peaks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    peak_names = [peak["name"] for peak in data]
    expected_nearest_names = ["Rysy", "Śnieżka", "Babia Góra"]
    assert all(name in peak_names for name in expected_nearest_names)

    for peak in data:
        assert "id" in peak
        assert "name" in peak
        assert "elevation" in peak
        assert "lat" in peak
        assert "lng" in peak
        assert "mountain_range" in peak
        assert "created_at" in peak


@pytest.mark.asyncio
async def test_get_peaks_empty_database(client_with_db: AsyncClient):
    """Test getting peaks when the database is empty"""
    response = await client_with_db.get("/api/peaks")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "coords_key,expected_nearest_name",
    [
        ("near_rysy", "Rysy"),
        ("near_sniezka", "Śnieżka"),
    ],
)
async def test_find_nearest_peaks_parametrized(
    client_with_db: AsyncClient,
    db_peaks,
    coords_map: dict,
    coords_key: str,
    expected_nearest_name: str,
):
    """Happy-path nearest peaks search for multiple coordinate sets."""
    lat, lng = coords_map[coords_key]

    response = await client_with_db.get(
        "/api/peaks/find",
        params={"lat": lat, "lng": lng},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    assert all("peak" in item and "distance" in item for item in data)
    assert all(isinstance(item["distance"], (int, float)) for item in data)

    distances = [item["distance"] for item in data]
    assert distances == sorted(distances)

    assert data[0]["peak"]["name"] == expected_nearest_name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,expected_len,expected_nearest_name",
    [
        ({}, 3, "Rysy"),
        ({"limit": 2}, 2, "Rysy"),
        ({"max_distance": 100}, 1, "Rysy"),
        ({"name_filter": "rysy"}, 1, "Rysy"),
        ({"limit": 1, "max_distance": 100, "name_filter": "rysy"}, 1, "Rysy"),
    ],
)
async def test_find_nearest_peaks_filters_parametrized(
    client_with_db: AsyncClient,
    db_peaks,
    coords_map: dict,
    params: dict,
    expected_len: int,
    expected_nearest_name: str,
):
    """Nearest peaks with various filtering combinations (limit, max_distance)."""
    lat, lng = coords_map["near_rysy"]
    query = {"lat": lat, "lng": lng, **params}

    response = await client_with_db.get("/api/peaks/find", params=query)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == expected_len
    assert data[0]["peak"]["name"] == expected_nearest_name
    assert all("peak" in item and "distance" in item for item in data)


@pytest.mark.asyncio
async def test_find_nearest_peaks_empty_database(
    client_with_db: AsyncClient, coords_map: dict
):
    """Nearest peaks returns empty list when DB has no peaks."""
    lat, lng = coords_map["near_rysy"]

    response = await client_with_db.get(
        "/api/peaks/find", params={"lat": lat, "lng": lng}
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {},
        {"lat": 49.0},
        {"lng": 20.0},
        {"lat": "invalid", "lng": 20.0},
        {"lat": 49.0, "lng": 20.0, "limit": "invalid"},
    ],
)
async def test_find_nearest_peaks_validation_errors_parametrized(
    client_with_db: AsyncClient, params: dict
):
    """Validation error scenarios for nearest peaks endpoint."""
    response = await client_with_db.get("/api/peaks/find", params=params)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_peak(client_with_db: AsyncClient, db_peaks):
    """Test getting a specific peak by ID"""
    peak_id = db_peaks[0].id

    response = await client_with_db.get(f"/api/peaks/{peak_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == peak_id
    assert data["name"] == "Rysy"
    assert data["elevation"] == 2499
    assert data["lat"] == 49.1795
    assert data["lng"] == 20.0881
    assert data["mountain_range"]["name"] == "Tatry"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_peak_not_found(client_with_db: AsyncClient):
    """Test getting a non-existent peak"""
    response = await client_with_db.get("/api/peaks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Peak not found"}

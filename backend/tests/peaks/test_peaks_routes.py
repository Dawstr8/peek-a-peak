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
        assert "mountainRange" in peak
        assert "createdAt" in peak


@pytest.mark.asyncio
async def test_get_peaks_empty_database(client_with_db: AsyncClient):
    """Test getting peaks when the database is empty"""
    response = await client_with_db.get("/api/peaks")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_peaks_count(client_with_db: AsyncClient, db_peaks):
    response = await client_with_db.get("/api/peaks/count")

    assert response.status_code == 200
    data = response.json()
    assert data == 3


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,expected_peaks_ids",
    [
        ({}, [0, 1, 2]),
        ({"nameFilter": "rysy"}, [0]),
        ({"limit": 2}, [0, 1]),
        ({"sortBy": "elevation", "order": "desc"}, [0, 2, 1]),
    ],
)
async def test_search_peaks_parametrized(
    client_with_db: AsyncClient, db_peaks, params: dict, expected_peaks_ids: list
):
    """Test searching peaks with various parameters."""
    response = await client_with_db.get("/api/peaks/search", params=params)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(expected_peaks_ids)

    expected_peaks = [db_peaks[idx] for idx in expected_peaks_ids]
    for peak, expected_peak in zip(data, expected_peaks):
        assert peak["id"] == expected_peak.id
        assert peak["name"] == expected_peak.name
        assert peak["elevation"] == expected_peak.elevation
        assert peak["lat"] == expected_peak.lat
        assert peak["lng"] == expected_peak.lng
        assert peak["mountainRange"]["name"] == expected_peak.mountain_range.name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "coords_key,expected_nearest_name",
    [
        ("near_rysy", "Rysy"),
        ("near_sniezka", "Śnieżka"),
    ],
)
async def test_find_nearby_peaks_parametrized(
    client_with_db: AsyncClient,
    db_peaks,
    coords_map: dict,
    coords_key: str,
    expected_nearest_name: str,
):
    """Happy-path nearby peaks search for multiple coordinate sets."""
    lat, lng = coords_map[coords_key]

    response = await client_with_db.get(
        "/api/peaks/nearby",
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
        ({"maxDistance": 100}, 1, "Rysy"),
        ({"nameFilter": "rysy"}, 1, "Rysy"),
        ({"limit": 1, "maxDistance": 100, "nameFilter": "rysy"}, 1, "Rysy"),
    ],
)
async def test_find_nearby_peaks_filters_parametrized(
    client_with_db: AsyncClient,
    db_peaks,
    coords_map: dict,
    params: dict,
    expected_len: int,
    expected_nearest_name: str,
):
    """Nearby peaks with various filtering combinations (limit, maxDistance, nameFilter)."""
    lat, lng = coords_map["near_rysy"]
    query = {"lat": lat, "lng": lng, **params}

    response = await client_with_db.get("/api/peaks/nearby", params=query)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == expected_len
    assert data[0]["peak"]["name"] == expected_nearest_name
    assert all("peak" in item and "distance" in item for item in data)


@pytest.mark.asyncio
async def test_find_nearby_peaks_empty_database(
    client_with_db: AsyncClient, coords_map: dict
):
    """Nearest peaks returns empty list when DB has no peaks."""
    lat, lng = coords_map["near_rysy"]

    response = await client_with_db.get(
        "/api/peaks/nearby", params={"lat": lat, "lng": lng}
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
async def test_find_nearby_peaks_validation_errors_parametrized(
    client_with_db: AsyncClient, params: dict
):
    """Validation error scenarios for nearby peaks endpoint."""
    response = await client_with_db.get("/api/peaks/nearby", params=params)

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
    assert data["mountainRange"]["name"] == "Tatry"
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_get_peak_not_found(client_with_db: AsyncClient):
    """Test getting a non-existent peak"""
    id = 999

    response = await client_with_db.get(f"/api/peaks/{id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Peak with id {id} not found."}

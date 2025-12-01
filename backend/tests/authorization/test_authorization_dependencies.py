from dataclasses import dataclass
from typing import Literal

import pytest

from src.users.models import User
from tests.auth.auth_fixtures import temporary_login


@dataclass
class RouteTestCase:
    """Represents a test case for route authorization."""

    url: str
    method: Literal["get", "post", "patch", "put", "delete"] = "get"
    requires_private_user: bool = False


ROUTES = {
    "public": RouteTestCase(url="/api/peaks"),
    "owner_public": RouteTestCase(url="/api/users/{username}"),
    "owner_private": RouteTestCase(
        url="/api/users/{username}", requires_private_user=True
    ),
    "owner_only": RouteTestCase(method="patch", url="/api/users/{username}"),
}


async def _setup_user_privacy(client_with_db, user: User, is_private: bool):
    if not is_private:
        return

    username, password = user["username"], user["password"]
    async with temporary_login(client_with_db, username, password):
        await client_with_db.patch(f"/api/users/{username}", json={"isPrivate": True})


async def _make_request(client_with_db, route_case: RouteTestCase, username: str):
    url = route_case.url.replace("{username}", username)

    if route_case.method.lower() == "patch":
        return await getattr(client_with_db, route_case.method)(
            url, json={"isPrivate": False}
        )
    else:
        return await getattr(client_with_db, route_case.method)(url)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route_name,expected_status",
    [
        ("public", 200),
        ("owner_public", 200),
        ("owner_private", 403),
        ("owner_only", 401),
    ],
)
async def test_route_access_without_login(
    client_with_db, registered_users, route_name, expected_status
):
    """Test that routes properly handle access when not logged in."""
    route_case = ROUTES[route_name]
    owner = registered_users[0]
    await _setup_user_privacy(client_with_db, owner, route_case.requires_private_user)

    response = await _make_request(client_with_db, route_case, owner["username"])

    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route_name,expected_status",
    [
        ("public", 200),
        ("owner_public", 200),
        ("owner_private", 403),
        ("owner_only", 403),
    ],
)
async def test_route_access_as_different_user(
    client_with_db, registered_users, route_name, expected_status
):
    """Test that routes properly handle access from non-owner authenticated users."""
    route_case = ROUTES[route_name]
    owner, current_user = registered_users
    await _setup_user_privacy(client_with_db, owner, route_case.requires_private_user)

    async with temporary_login(
        client_with_db, current_user["username"], current_user["password"]
    ):
        response = await _make_request(client_with_db, route_case, owner["username"])

        assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route_name,expected_status",
    [
        ("public", 200),
        ("owner_public", 200),
        ("owner_private", 200),
        ("owner_only", 200),
    ],
)
async def test_route_access_as_owner(
    client_with_db, registered_users, route_name, expected_status
):
    """Test that routes properly allow access from resource owners."""
    route_case = ROUTES[route_name]
    owner = registered_users[0]
    await _setup_user_privacy(client_with_db, owner, route_case.requires_private_user)

    async with temporary_login(client_with_db, owner["username"], owner["password"]):
        response = await _make_request(client_with_db, route_case, owner["username"])

        assert response.status_code == expected_status

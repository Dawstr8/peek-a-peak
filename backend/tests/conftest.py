import shutil
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import UploadFile
from httpx import ASGITransport, AsyncClient
from starlette.datastructures import Headers

from main import app
from src.database.core import get_db
from src.uploads.services.local_storage import LocalFileStorage
from tests.auth.auth_fixtures import logged_in_user, registered_user, registered_users
from tests.database.database_fixtures import setup_database, test_db
from tests.peaks.peaks_fixtures import (
    coords_map,
    db_peaks,
    mock_peaks_map,
    mock_peaks_repository,
)
from tests.photos.photos_fixtures import (
    db_photos,
    e2e_photo,
    e2e_photos,
    mock_photo,
    mock_photos,
    mock_photos_repository,
)
from tests.users.users_fixtures import (
    db_user,
    db_users,
    mock_user,
    mock_users_repository,
)


@pytest_asyncio.fixture
async def client_with_db(test_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with a test database session.
    Reuses the test_db fixture for database operations.
    """

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://testserver"
    ) as async_test_client:
        yield async_test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_upload_dir():
    """Creates a temporary upload directory for tests"""
    test_dir = Path("test_uploads")
    test_dir.mkdir(exist_ok=True)
    yield test_dir

    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture
def local_storage(test_upload_dir):
    """Creates a LocalFileStorage instance with test directory"""
    return LocalFileStorage(upload_dir=str(test_upload_dir))


@pytest.fixture
def mock_upload_file(tmp_path):
    """Creates a mock UploadFile for testing"""
    test_content = b"test image content"
    test_file = tmp_path / "test.jpg"
    test_file.write_bytes(test_content)

    return UploadFile(
        filename="test.jpg",
        file=open(test_file, "rb"),
        headers=Headers({"content-type": "image/jpeg"}),
    )

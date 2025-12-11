import shutil
from pathlib import Path
from typing import AsyncGenerator
from unittest.mock import Mock

import pytest
import pytest_asyncio
from fastapi import BackgroundTasks, UploadFile
from httpx import ASGITransport, AsyncClient
from starlette.datastructures import Headers

from main import app
from src.database.core import get_db
from src.photos.dependencies import get_uploads_service
from src.uploads.service import UploadsService
from src.uploads.services.local_storage import LocalFileStorage
from src.weather.client import OpenWeatherMapClient
from src.weather.dependencies import get_openweathermap_client
from tests.auth.auth_fixtures import *
from tests.database.database_fixtures import *
from tests.mountain_ranges.mountain_ranges_fixtures import *
from tests.peaks.peaks_fixtures import *
from tests.photos.photos_fixtures import *
from tests.users.users_fixtures import *
from tests.weather.weather_fixtures import *


@pytest.fixture
def test_upload_dir():
    """Creates a temporary upload directory for tests"""
    test_dir = Path("test_uploads")
    test_dir.mkdir(exist_ok=True)
    yield test_dir

    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest_asyncio.fixture
async def client_with_db(
    test_db, mock_weather_client: OpenWeatherMapClient, test_upload_dir
) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with a test database session.
    Reuses the test_db fixture for database operations.
    """

    async def override_get_db():
        yield test_db

    async def override_get_openweathermap_client():
        yield mock_weather_client

    def _get_uploads_service():
        return UploadsService(LocalFileStorage(upload_dir=str(test_upload_dir)))

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_openweathermap_client] = (
        override_get_openweathermap_client
    )
    app.dependency_overrides[get_uploads_service] = _get_uploads_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://testserver"
    ) as async_test_client:
        yield async_test_client

    app.dependency_overrides.clear()


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


@pytest.fixture
def mock_background_tasks():
    """Create a mock BackgroundTasks"""
    return Mock(spec=BackgroundTasks)

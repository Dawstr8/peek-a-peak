import shutil
from pathlib import Path

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlmodel import Session, SQLModel, create_engine
from starlette.datastructures import Headers

from config import Config
from main import app
from src.database.core import get_db
from src.uploads.services.local_storage import LocalFileStorage
from tests.auth.auth_fixtures import logged_in_user, registered_user, registered_users
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


@pytest.fixture
def client():
    """Creates a TestClient instance for API testing"""
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client


@pytest.fixture
def client_with_db(test_db):
    """
    Create a test client with a test database session.
    Reuses the test_db fixture for database operations.
    """

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def db_engine():
    test_db = "peek_a_peak_test"
    postgres_url = f"{Config.POSTGRES_SERVER_URL}/postgres"
    test_url = f"{Config.POSTGRES_SERVER_URL}/{test_db}"

    engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {test_db}"))

    test_engine = create_engine(test_url, echo=True)
    SQLModel.metadata.create_all(test_engine)

    yield test_engine

    test_engine.dispose()

    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db}"))

    engine.dispose()


@pytest.fixture
def test_db(db_engine):
    """
    Creates an isolated database session for each test.
    Uses transactions that rollback after each test to ensure isolation.
    """
    connection = db_engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)

    try:
        yield db
    finally:
        db.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


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

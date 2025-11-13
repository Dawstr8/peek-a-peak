import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.sessions.repository import SessionsRepository


@pytest.fixture
def test_sessions_repository(test_db: AsyncSession) -> SessionsRepository:
    """Create a SessionsRepository instance for testing."""
    return SessionsRepository(test_db)


@pytest.mark.asyncio
async def test_create_session(test_sessions_repository: SessionsRepository, db_user):
    """Test creating a new session"""
    user_id = db_user.id
    expires_in_days = 7

    session = await test_sessions_repository.create(user_id, expires_in_days)

    assert session.id is not None
    assert session.user_id == user_id
    assert session.is_active


@pytest.mark.asyncio
async def test_get_active_by_id_valid(
    test_sessions_repository: SessionsRepository, db_user
):
    """Test retrieving valid active session by ID"""
    user_id = db_user.id
    session = await test_sessions_repository.create(user_id, expires_in_days=7)

    retrieved_session = await test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is not None
    assert retrieved_session.id == session.id
    assert retrieved_session.user_id == user_id
    assert retrieved_session.is_active


@pytest.mark.asyncio
async def test_get_active_by_id_expired(
    test_sessions_repository: SessionsRepository, db_user
):
    """Test retrieving expired session by ID returns None"""
    user_id = db_user.id
    session = await test_sessions_repository.create(user_id, expires_in_days=0)

    retrieved_session = await test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is None


@pytest.mark.asyncio
async def test_get_active_by_id_invalidated(
    test_sessions_repository: SessionsRepository, db_user
):
    """Test retrieving invalidated session by ID returns None"""
    user_id = db_user.id
    session = await test_sessions_repository.create(user_id, expires_in_days=7)
    await test_sessions_repository.invalidate_by_id(session.id)

    retrieved_session = await test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is None


@pytest.mark.asyncio
async def test_invalidate_by_id(test_sessions_repository: SessionsRepository, db_user):
    """Test invalidating a session"""
    user_id = db_user.id
    session = await test_sessions_repository.create(user_id, expires_in_days=7)

    await test_sessions_repository.invalidate_by_id(session.id)

    inactive_session = await test_sessions_repository.get_active_by_id(session.id)
    assert inactive_session is None

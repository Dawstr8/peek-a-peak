import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config import Config


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    test_db = "peek_a_peak_test"
    postgres_url = f"{Config.POSTGRES_SERVER_URL}/postgres"
    admin_engine = create_async_engine(postgres_url, isolation_level="AUTOCOMMIT")
    async with admin_engine.connect() as conn:
        try:
            await conn.execute(text(f"CREATE DATABASE {test_db}"))
        except Exception:
            pass

    yield

    await admin_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Creates a new database session for a test."""
    db_url = f"{Config.POSTGRES_SERVER_URL}/peek_a_peak_test"
    engine = create_async_engine(db_url)
    async_sessionmaker = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_sessionmaker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()

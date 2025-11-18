"""
Seed the database with sample Polish peaks, mountain ranges, and their associations.

Usage:
    python -m src.database.seed.run_seed
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.database.seed.wikipedia_seed import seed_wikipedia


async def _run_seed():
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as db:
        print("Seeding wikipedia data...")
        await seed_wikipedia(db)

        print("Database seeding completed successfully!")


def run_seed():
    asyncio.run(_run_seed())


if __name__ == "__main__":
    run_seed()

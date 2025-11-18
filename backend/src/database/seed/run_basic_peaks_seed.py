"""
Seed the database with basic Polish peaks and mountain ranges data from Wikipedia.
This script scrapes the main Wikipedia page for highest peaks in Poland and saves
basic information (names, elevations, wiki_page links) without location data.

Usage:
    python -m src.database.seed.run_basic_peaks_seed
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.database.seed.basic_peaks_seed import seed_basic_peaks


async def _run_basic_peaks_seed():
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as db:
        print("Starting basic peaks seeding...")
        await seed_basic_peaks(db)

        print("Basic peaks seeding completed successfully!")


def run_basic_peaks_seed():
    asyncio.run(_run_basic_peaks_seed())


if __name__ == "__main__":
    run_basic_peaks_seed()

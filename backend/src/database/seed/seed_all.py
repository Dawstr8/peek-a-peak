"""
Seed the database with sample Polish peaks, mountain ranges, and their associations.

Usage:
    python -m src.database.seed.seed_all
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.mountain_ranges.models import MountainRange
from src.peaks.models import Peak

MOUNTAIN_RANGES_DATA = [
    {"name": "Tatry"},
    {"name": "Karkonosze"},
    {"name": "Beskidy"},
    {"name": "Bieszczady"},
    {"name": "Masyw Śnieżnika"},
    {"name": "Góry Sowie"},
]

PEAKS_DATA_MAP = {
    "Tatry": [
        {
            "name": "Rysy",
            "elevation": 2499,
            "location": "POINT(20.0881 49.1795)",
        },
    ],
    "Karkonosze": [
        {
            "name": "Śnieżka",
            "elevation": 1602,
            "location": "POINT(15.7400 50.7361)",
        },
    ],
    "Beskidy": [
        {
            "name": "Babia Góra",
            "elevation": 1725,
            "location": "POINT(19.5297 49.5731)",
        },
    ],
    "Bieszczady": [
        {
            "name": "Tarnica",
            "elevation": 1346,
            "location": "POINT(22.7267 49.0758)",
        },
    ],
    "Masyw Śnieżnika": [
        {
            "name": "Śnieżnik",
            "elevation": 1425,
            "location": "POINT(16.8483 50.2067)",
        },
    ],
    "Góry Sowie": [
        {
            "name": "Kalenica",
            "elevation": 964,
            "location": "POINT(16.5464 50.6428)",
        },
    ],
}


async def _seed_all():
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        existing_ranges = (await session.exec(select(MountainRange))).all()
        if existing_ranges:
            print(
                f"Database already contains {len(existing_ranges)} mountain ranges. Skipping seeding."
            )
            return

        for data in MOUNTAIN_RANGES_DATA:
            session.add(MountainRange(**data))

        for range_name, peaks in PEAKS_DATA_MAP.items():
            result = await session.exec(
                select(MountainRange).where(MountainRange.name == range_name)
            )
            mountain_range = result.one()

            for peak_data in peaks:
                peak = Peak(**peak_data, mountain_range_id=mountain_range.id)
                session.add(peak)

        await session.commit()
        print("Database seeding completed successfully!")


def seed_all():
    """Entry point for seeding the database"""
    asyncio.run(_seed_all())


if __name__ == "__main__":
    seed_all()

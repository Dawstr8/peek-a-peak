"""
Script to seed the database with sample Polish peaks
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.peaks.models import Peak


def seed_peaks():
    """Seed the database with sample Polish peaks"""

    # Sample Polish peaks data
    peaks_data = [
        {
            "name": "Rysy",
            "elevation": 2499,
            "latitude": 49.1795,
            "longitude": 20.0881,
            "range": "Tatry",
        },
        {
            "name": "Śnieżka",
            "elevation": 1602,
            "latitude": 50.7361,
            "longitude": 15.7400,
            "range": "Karkonosze",
        },
        {
            "name": "Babia Góra",
            "elevation": 1725,
            "latitude": 49.5731,
            "longitude": 19.5297,
            "range": "Beskidy",
        },
        {
            "name": "Tarnica",
            "elevation": 1346,
            "latitude": 49.0758,
            "longitude": 22.7267,
            "range": "Bieszczady",
        },
        {
            "name": "Śnieżnik",
            "elevation": 1425,
            "latitude": 50.2067,
            "longitude": 16.8483,
            "range": "Masyw Śnieżnika",
        },
        {
            "name": "Kalenica",
            "elevation": 964,
            "latitude": 50.6428,
            "longitude": 16.5464,
            "range": "Góry Sowie",
        },
    ]

    async def _seed():
        async_session = async_sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            existing = (await session.exec(select(Peak))).all()
            if existing:
                print(
                    f"Database already contains {len(existing)} peaks. Skipping seeding."
                )
                return

            for data in peaks_data:
                session.add(Peak(**data))

            await session.commit()
            print("Database seeding completed successfully!")

    asyncio.run(_seed())


if __name__ == "__main__":
    seed_peaks()

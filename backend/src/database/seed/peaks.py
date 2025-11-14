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
            "location": "POINT(20.0881 49.1795)",
            "range": "Tatry",
        },
        {
            "name": "Śnieżka",
            "elevation": 1602,
            "location": "POINT(15.7400 50.7361)",
            "range": "Karkonosze",
        },
        {
            "name": "Babia Góra",
            "elevation": 1725,
            "location": "POINT(19.5297 49.5731)",
            "range": "Beskidy",
        },
        {
            "name": "Tarnica",
            "elevation": 1346,
            "location": "POINT(22.7267 49.0758)",
            "range": "Bieszczady",
        },
        {
            "name": "Śnieżnik",
            "elevation": 1425,
            "location": "POINT(16.8483 50.2067)",
            "range": "Masyw Śnieżnika",
        },
        {
            "name": "Kalenica",
            "elevation": 964,
            "location": "POINT(16.5464 50.6428)",
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

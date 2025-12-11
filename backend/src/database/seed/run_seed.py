"""
Seed the database with sample Polish peaks, mountain ranges, and their associations.

This script follows the Wikimedia Robot Policy guidelines:
https://wikitech.wikimedia.org/wiki/Robot_policy

Key compliance measures:
- Proper User-Agent identification (not browser impersonation)
- Gzip compression for reduced bandwidth
- Rate limiting with 3-second delays between requests
- Respect for HTTP 429 (Too Many Requests) with Retry-After header
- 15-minute pause on 5xx server errors
- Uses CDN-cached /wiki/ URLs for efficiency
- Sequential (non-concurrent) requests to minimize server load

Usage:
    python -m src.database.seed.run_seed
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.database.seed.basic_peaks_seed import seed_basic_peaks
from src.database.seed.peak_location_enricher import enrich_peaks_with_locations


async def _run_seed():
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as db:
        print("Seeding basic peaks data...")
        await seed_basic_peaks(db)

        print("Enriching peaks with location data...")
        await enrich_peaks_with_locations(db)

        print("Database seeding completed successfully!")


def run_seed():
    asyncio.run(_run_seed())


if __name__ == "__main__":
    run_seed()

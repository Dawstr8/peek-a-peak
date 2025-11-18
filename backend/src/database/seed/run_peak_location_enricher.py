"""
Enrich existing peaks in the database with location data from their Wikipedia pages.
This script finds peaks that have wiki_page attributes but no location data,
then visits each Wikipedia page to extract coordinate information.

Usage:
    python -m src.database.seed.run_peak_location_enricher
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.core import engine
from src.database.seed.peak_location_enricher import enrich_peaks_with_locations


async def _run_peak_location_enricher():
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as db:
        print("Starting peak location enrichment...")
        await enrich_peaks_with_locations(db)

        print("Peak location enrichment completed successfully!")


def run_peak_location_enricher():
    asyncio.run(_run_peak_location_enricher())


if __name__ == "__main__":
    run_peak_location_enricher()

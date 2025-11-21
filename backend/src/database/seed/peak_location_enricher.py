import time
import traceback
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from sqlmodel.ext.asyncio.session import AsyncSession

from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


async def enrich_peaks_with_locations(db: AsyncSession):
    """
    Find peaks without locations and enrich them by scraping their individual Wikipedia pages.
    This function looks for peaks that have a wiki_page attribute but no location data,
    then visits each Wikipedia page to extract coordinate information.
    """
    try:
        print("Starting peak location enrichment...")

        peaks_without_location = await _get_peaks_without_location(db)
        total_peaks = len(peaks_without_location)

        if total_peaks == 0:
            print("No peaks without location found!")
            return

        print(f"Found {total_peaks} peaks without location data")

        enriched_count = 0
        for i, peak in enumerate(peaks_without_location, 1):
            if not peak.wiki_page:
                print(f"[{i}/{total_peaks}] Skipping {peak.name} - no wiki page")
                continue

            print(f"[{i}/{total_peaks}] Processing {peak.name}...")

            try:
                time.sleep(1)  # Be polite and avoid overwhelming the server
                soup = _fetch_webpage_content(peak.wiki_page, HEADERS)
                location = _extract_peak_location(soup)

                if location:
                    await _enrich_peak_with_location(db, peak, location)
                    enriched_count += 1
                else:
                    print(f"No location coordinates found for {peak.name}")

            except Exception as e:
                print(f"Failed to process {peak.name}: {e}")
                continue

        print(
            f"Peak location enrichment completed! Enriched {enriched_count}/{total_peaks} peaks"
        )

    except Exception as e:
        print(f"Failed to enrich peak locations: {e}")
        traceback.print_exc()


async def _get_peaks_without_location(db: AsyncSession) -> list[Peak]:
    repository = PeaksRepository(db)
    return await repository.get_all_without_location()


def _fetch_webpage_content(url: str, headers: Dict[str, str]) -> BeautifulSoup:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return BeautifulSoup(response.content, "html.parser")


def _extract_peak_location(soup: BeautifulSoup) -> Optional[str]:
    lat_span = soup.select_one("span.geo-nondefault span.geo-dms span.latitude")
    lng_span = soup.select_one("span.geo-nondefault span.geo-dms span.longitude")

    if not lat_span or not lng_span:
        return None

    lat = _parse_coordinate(lat_span.get_text(strip=True))
    lng = _parse_coordinate(lng_span.get_text(strip=True))

    if lat is not None and lng is not None:
        return f"POINT({lng} {lat})"


def _parse_coordinate(coordinate_str: str) -> float:
    return float(coordinate_str.replace(",", "."))


async def _enrich_peak_with_location(
    db: AsyncSession, peak: Peak, location: str
) -> None:
    repository = PeaksRepository(db)

    peak = await repository.get_by_name_elevation_and_mountain_range(
        peak.name, peak.elevation, peak.mountain_range_id
    )

    if not peak:
        return

    peak.location = location
    await repository.save(peak)
    print(f"Updated location for peak: {peak.name}")

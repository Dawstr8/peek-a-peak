import time
import traceback
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from sqlmodel.ext.asyncio.session import AsyncSession

from src.common.exceptions import NotFoundException
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository

# Following Wikimedia Robot Policy: https://wikitech.wikimedia.org/wiki/Robot_policy
# User-Agent must identify the bot clearly per Wikimedia Foundation User-Agent Policy
# Format: <client name>/<version> (<contact information>) <library/framework name>/<version>
HEADERS = {
    "User-Agent": "PeekAPeak/1.0 (https://github.com/Dawstr8/peek-a-peak; dawid.strojek@gmail.com) python-requests/2.31.0",
    "Accept-Encoding": "gzip",  # Always request gzip compression to reduce bandwidth
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
                # Website rules: Keep requests below 20/second, ideally with delays
                # Using 3 seconds between requests to be conservative and polite
                time.sleep(3)
                soup = _fetch_webpage_content(peak.wiki_page, HEADERS)
                location = _extract_peak_location(soup)

                if location:
                    await _enrich_peak_with_location(db, peak, location)
                    enriched_count += 1
                else:
                    print(f"No location coordinates found for {peak.name}")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    # Respect 429 Too Many Requests with Retry-After header
                    retry_after = e.response.headers.get("Retry-After", "60")
                    print(
                        f"Rate limited. Waiting {retry_after} seconds before retrying..."
                    )
                    time.sleep(int(retry_after))
                    # Retry the request once
                    try:
                        soup = _fetch_webpage_content(peak.wiki_page, HEADERS)
                        location = _extract_peak_location(soup)
                        if location:
                            await _enrich_peak_with_location(db, peak, location)
                            enriched_count += 1
                    except Exception as retry_error:
                        print(f"Retry failed for {peak.name}: {retry_error}")
                elif e.response.status_code >= 500:
                    # For 5xx errors, pause for 15 minutes as per guidelines
                    print(
                        f"Server error {e.response.status_code}. Pausing for 15 minutes..."
                    )
                    time.sleep(900)
                else:
                    print(f"HTTP error for {peak.name}: {e}")
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
    """
    Fetch webpage content following Wikimedia Robot Policy.
    Uses /wiki/ URLs which are CDN-cached for faster responses.
    """
    response = requests.get(url, headers=headers, timeout=30)
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

    try:
        peak = await repository.get_by_fields(
            {
                "name": peak.name,
                "elevation": peak.elevation,
                "mountain_range_id": peak.mountain_range_id,
            }
        )
    except NotFoundException:
        peak = None

    if not peak:
        return

    peak.location = location
    await repository.save(peak)
    print(f"Updated location for peak: {peak.name}")

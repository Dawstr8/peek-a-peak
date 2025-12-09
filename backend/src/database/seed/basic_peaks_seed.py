import re
import traceback
from io import StringIO
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository

BASE_URL = "https://pl.wikipedia.org"
HIGHEST_PEAKS_URL = (
    f"{BASE_URL}/wiki/Lista_najwy%C5%BCszych_szczyt%C3%B3w_g%C3%B3rskich_w_Polsce"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


async def seed_basic_peaks(db: AsyncSession):
    """
    Scrape basic peak data (names, elevations, wiki_page links) from the main Wikipedia page
    and save mountain ranges and peaks to the database.
    """
    try:
        print("Starting basic Wikipedia peaks data seeding...")

        soup = _fetch_webpage_content(HIGHEST_PEAKS_URL, HEADERS)
        mountain_ranges_with_peaks = _scrape_mountain_ranges_with_peaks(soup)
        await _save_mountain_range_and_peaks(db, mountain_ranges_with_peaks)

        print("Basic Wikipedia peaks data seeding completed successfully!")

    except Exception as e:
        print(f"Failed to seed basic peaks data: {e}")
        traceback.print_exc()


def _fetch_webpage_content(url: str, headers: Dict[str, str]) -> BeautifulSoup:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return BeautifulSoup(response.content, "html.parser")


def _scrape_mountain_ranges_with_peaks(
    soup: BeautifulSoup,
) -> List[Tuple[MountainRange, List[Peak]]]:
    mountain_ranges_with_peaks = []

    h3_elements = soup.find_all("h3")
    for h3 in h3_elements:
        table = h3.parent.find_next_sibling("table")

        mountain_range_name = _extract_mountain_range_name(h3)
        peaks = _extract_peaks(table)

        mountain_ranges_with_peaks.append(
            (MountainRange(name=mountain_range_name), peaks)
        )

    return mountain_ranges_with_peaks


def _extract_mountain_range_name(h3_element: BeautifulSoup) -> str:
    mountain_range_name = h3_element.get_text(strip=True)

    return _parse_mountain_range_name(mountain_range_name)


def _parse_mountain_range_name(name: str) -> str:
    return re.sub(r"\s*\[.*?\]\s*", "", name).strip()


def _extract_peaks(table_element: BeautifulSoup) -> List[Peak]:
    df = pd.read_html(StringIO(str(table_element)), header=0)[0]
    links = _extract_table_links(table_element)

    df["Nazwa"] = df["Nazwa"].astype(str).apply(_parse_peak_name)
    df["Wysokość (m n.p.m.)"] = (
        df["Wysokość (m n.p.m.)"].astype(str).str.extract(r"(\d+)").astype(int)
    )

    peaks = [
        Peak(
            name=row["Nazwa"],
            elevation=row["Wysokość (m n.p.m.)"],
            wiki_page=links[i],
        )
        for i, row in df.iterrows()
    ]

    return peaks


def _extract_table_links(table_element: BeautifulSoup) -> List[Optional[str]]:
    links = []
    rows = table_element.find_all("tr")

    for row in rows[1:]:
        tds = row.find_all("td")
        if tds:
            first_td = tds[0]
            link_el = first_td.find("a")
            href = link_el.get("href", None) if link_el else None

            links.append(f"{BASE_URL}{href}" if href else None)

    return links


def _parse_peak_name(peak_name: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*", "", peak_name).strip()


async def _save_mountain_range_and_peaks(
    db: AsyncSession,
    mountain_ranges_with_peaks: List[Tuple[MountainRange, List[Peak]]],
):
    for mountain_range, peaks in mountain_ranges_with_peaks:
        mountain_range = await _get_or_create_mountain_range(db, mountain_range)
        await _save_or_update_peaks(db, peaks, mountain_range)


async def _get_or_create_mountain_range(
    db: AsyncSession, mountain_range: MountainRange
) -> MountainRange:
    repository = MountainRangesRepository(db)

    name = mountain_range.name

    existing_mountain_range = await repository.get_by_field("name", name)
    if existing_mountain_range:
        print(f"Found existing mountain range: {name}")
        return existing_mountain_range

    print(f"Creating new mountain range: {name}")
    return await repository.save(mountain_range)


async def _save_or_update_peaks(
    db: AsyncSession, peaks: List[Peak], mountain_range: MountainRange
) -> None:
    repository = PeaksRepository(db)

    peaks_to_add = []
    peaks_updated = 0

    for peak in peaks:
        existing_peak = await repository.get_by_fields(
            {
                "name": peak.name,
                "elevation": peak.elevation,
                "mountain_range_id": mountain_range.id,
            }
        )

        if existing_peak is None:
            peak.mountain_range_id = mountain_range.id
            peaks_to_add.append(peak)
            continue

        updated = False
        if existing_peak.wiki_page != peak.wiki_page:
            existing_peak.wiki_page = peak.wiki_page
            updated = True

        if updated:
            await repository.save(existing_peak)
            peaks_updated += 1

    await repository.save_all(peaks_to_add)

    if len(peaks_to_add) > 0:
        print(f"Added {len(peaks_to_add)} new peaks to {mountain_range.name}")

    if peaks_updated > 0:
        print(f"Updated {peaks_updated} existing peaks in {mountain_range.name}")

    if len(peaks_to_add) == 0 and peaks_updated == 0:
        print(f"No changes needed for peaks in {mountain_range.name}")

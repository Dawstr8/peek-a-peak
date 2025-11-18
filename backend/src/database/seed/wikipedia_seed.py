import re
import traceback
from io import StringIO
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mountain_ranges.models import MountainRange
from src.mountain_ranges.repository import MountainRangesRepository
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository

URL = "https://pl.wikipedia.org/wiki/Lista_najwy%C5%BCszych_szczyt%C3%B3w_g%C3%B3rskich_w_Polsce"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def _fetch_webpage_content(url: str, headers: Dict[str, str]) -> BeautifulSoup:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return BeautifulSoup(response.content, "html.parser")


def _parse_mountain_range_name(name: str) -> str:
    return re.sub(r"\s*\[.*?\]\s*", "", name).strip()


def _parse_peak_name(peak_name: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*", "", peak_name).strip()


def _extract_mountain_range_name(h3_element: BeautifulSoup) -> str:
    mountain_range_name = h3_element.get_text(strip=True)

    return _parse_mountain_range_name(mountain_range_name)


def _extract_peaks_data(table_element: BeautifulSoup, mountain_range_name: str) -> list:
    try:
        df = pd.read_html(StringIO(str(table_element)), header=0)[0]

        df["Nazwa"] = df["Nazwa"].astype(str).apply(_parse_peak_name)
        df["Wysokość (m n.p.m.)"] = (
            df["Wysokość (m n.p.m.)"].astype(str).str.extract(r"(\d+)").astype(int)
        )

        peaks_data = [
            {"name": row["Nazwa"], "elevation": row["Wysokość (m n.p.m.)"]}
            for index, row in df.iterrows()
        ]

        return peaks_data

    except Exception as e:
        print(f"Error processing table for {mountain_range_name}: {e}")


def _scrape_mountain_ranges_data(soup: BeautifulSoup) -> Dict[str, list]:
    mountain_ranges_data = []

    h3_elements = soup.find_all("h3")
    for h3 in h3_elements:
        table = h3.parent.find_next_sibling("table")

        mountain_range_name = _extract_mountain_range_name(h3)
        peaks_data = _extract_peaks_data(table, mountain_range_name)

        mountain_ranges_data.append(
            {"mountain_range": {"name": mountain_range_name}, "peaks": peaks_data}
        )

    return mountain_ranges_data


async def _get_or_create_mountain_range(
    db: AsyncSession, mountain_range_data: dict
) -> MountainRange:
    repository = MountainRangesRepository(db)
    name = mountain_range_data["name"]

    existing_mountain_range = await repository.get_by_name(name)
    if existing_mountain_range:
        print(f"Found existing mountain range: {name}")
        return existing_mountain_range

    print(f"Creating new mountain range: {name}")
    return await repository.save(MountainRange(**mountain_range_data))


async def _save_peaks_if_not_exist(
    db: AsyncSession, peaks_data: list, mountain_range: MountainRange
) -> bool:
    repository = PeaksRepository(db)

    peaks_to_add = []
    for peak_data in peaks_data:
        peak = await repository.get_by_name_elevation_and_mountain_range(
            peak_data["name"], peak_data["elevation"], mountain_range.id
        )
        if peak is not None:
            continue

        peaks_to_add.append(Peak(**peak_data, mountain_range_id=mountain_range.id))

    await repository.save_multiple(peaks_to_add)

    if len(peaks_to_add) > 0:
        print(f"Added {len(peaks_to_add)} new peaks to {mountain_range.name}")
    else:
        print(f"No new peaks to add to {mountain_range.name}")


async def _save_mountain_range_and_peaks(db: AsyncSession, mountain_ranges_data: list):
    for data in mountain_ranges_data:
        mountain_range = await _get_or_create_mountain_range(db, data["mountain_range"])
        await _save_peaks_if_not_exist(db, data["peaks"], mountain_range)


async def seed_wikipedia(db: AsyncSession):
    try:
        print("Starting Wikipedia data seeding...")
        soup = _fetch_webpage_content(URL, HEADERS)
        mountain_ranges_data = _scrape_mountain_ranges_data(soup)
        await _save_mountain_range_and_peaks(db, mountain_ranges_data)
        print("Wikipedia data seeding completed successfully!")

    except Exception as e:
        print(f"Failed to seed wikipedia data: {e}")
        traceback.print_exc()

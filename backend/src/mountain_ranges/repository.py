from typing import Optional

from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.mountain_ranges.models import MountainRange


class MountainRangesRepository(BaseRepository[MountainRange]):
    model = MountainRange

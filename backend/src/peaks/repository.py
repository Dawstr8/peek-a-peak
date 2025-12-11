from typing import List, Optional
from uuid import UUID

from geoalchemy2.functions import (
    ST_Distance,
    ST_DWithin,
    ST_GeogFromWKB,
    ST_MakePoint,
    ST_SetSRID,
)
from sqlmodel import func, select

from src.database.base_repository import BaseRepository
from src.peaks.models import Peak, PeakWithDistance
from src.photos.models import SummitPhoto
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting


class PeaksRepository(BaseRepository[Peak]):
    model = Peak

    async def get_all_without_location(self) -> List[Peak]:
        query = select(Peak).where(Peak.location.is_(None))
        result = await self.db.exec(query)
        return result.all()

    async def get_summited_by_user_count(self, user_id: UUID) -> int:
        query = (
            select(func.count(func.distinct(Peak.id)))
            .select_from(Peak)
            .join(SummitPhoto, SummitPhoto.peak_id == Peak.id)
            .where(SummitPhoto.owner_id == user_id)
        )
        result = await self.db.exec(query)
        return result.one()

    async def search(
        self,
        sort_params: Optional[SortParams] = None,
        name_filter: Optional[str] = None,
        limit: int = 5,
    ) -> List[Peak]:
        """Search peaks with optional name filtering and sorting."""
        statement = select(Peak)
        statement = statement.limit(limit)

        if sort_params is not None:
            statement = apply_sorting(statement, Peak, sort_params)

        if name_filter is not None:
            statement = statement.where(Peak.name.ilike(f"%{name_filter}%"))

        restult = await self.db.exec(statement)
        return restult.all()

    async def find_nearby(
        self,
        lat: float,
        lng: float,
        max_distance: Optional[float] = None,
        limit: int = 5,
        name_filter: Optional[str] = None,
    ) -> List[PeakWithDistance]:
        """
        Find peaks near a given location.

        Args:
            lat: Latitude of the reference point
            lng: Longitude of the reference point
            max_distance: Maximum distance in meters to consider
            limit: Maximum number of results to return (ignored if 0 or negative)
            name_filter: Optional substring to filter peak names (case-insensitive)

        Returns:
            List of PeakWithDistance models sorted by ascending distance.
        """
        target_point = ST_GeogFromWKB(ST_SetSRID(ST_MakePoint(lng, lat), 4326))

        query = (
            select(
                Peak,
                ST_Distance(Peak.location, target_point).label("distance"),
            )
            .order_by("distance")
            .limit(limit)
        )

        if max_distance is not None:
            query = query.where(ST_DWithin(Peak.location, target_point, max_distance))

        if name_filter is not None:
            query = query.where(Peak.name.ilike(f"%{name_filter}%"))

        result = await self.db.exec(query)
        rows = result.all()

        return [
            PeakWithDistance(peak=peak, distance=float(distance))
            for peak, distance in rows
        ]

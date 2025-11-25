from typing import List, Optional

from geoalchemy2.functions import (
    ST_Distance,
    ST_DWithin,
    ST_GeogFromWKB,
    ST_MakePoint,
    ST_SetSRID,
)
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.peaks.models import Peak, PeakWithDistance
from src.photos.models import SummitPhoto


class PeaksRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, peak: Peak) -> Peak:
        self.db.add(peak)
        await self.db.commit()
        await self.db.refresh(peak)
        return peak

    async def save_multiple(self, peaks: List[Peak]) -> None:
        self.db.add_all(peaks)
        await self.db.commit()

    async def get_all(self) -> List[Peak]:
        query = select(Peak)
        result = await self.db.exec(query)
        return result.all()

    async def get_all_without_location(self) -> List[Peak]:
        query = select(Peak).where(Peak.location.is_(None))
        result = await self.db.exec(query)
        return result.all()

    async def get_count(self) -> int:
        query = select(func.count()).select_from(Peak)
        result = await self.db.exec(query)
        return result.one()

    async def get_summited_by_user_count(self, user_id: int) -> int:
        query = (
            select(func.count(func.distinct(Peak.id)))
            .select_from(Peak)
            .join(SummitPhoto, SummitPhoto.peak_id == Peak.id)
            .where(SummitPhoto.owner_id == user_id)
        )
        result = await self.db.exec(query)
        return result.one()

    async def get_by_id(self, peak_id: int) -> Optional[Peak]:
        return await self.db.get(Peak, peak_id)

    async def get_by_name_elevation_and_mountain_range(
        self, peak_name: str, elevation: int, mountain_range_id: int
    ) -> Optional[Peak]:
        query = select(Peak).where(
            Peak.name == peak_name,
            Peak.elevation == elevation,
            Peak.mountain_range_id == mountain_range_id,
        )
        result = await self.db.exec(query)
        return result.first()

    async def get_nearest(
        self,
        lat: float,
        lng: float,
        max_distance: Optional[float] = None,
        limit: int = 5,
        name_filter: Optional[str] = None,
    ) -> List[PeakWithDistance]:
        """Find nearest peaks to a given lat and lng.

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

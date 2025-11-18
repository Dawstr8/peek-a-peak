from typing import List, Optional

from geoalchemy2.functions import (
    ST_Distance,
    ST_DWithin,
    ST_GeogFromWKB,
    ST_MakePoint,
    ST_SetSRID,
)
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.peaks.models import Peak, PeakWithDistance


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
        latitude: float,
        longitude: float,
        max_distance: Optional[float] = None,
        limit: int = 5,
    ) -> List[PeakWithDistance]:
        """Find nearest peaks to a given latitude and longitude.

        Args:
            latitude: Latitude of the reference point
            longitude: Longitude of the reference point
            max_distance: Maximum distance in meters to consider
            limit: Maximum number of results to return (ignored if 0 or negative)

        Returns:
            List of PeakWithDistance models sorted by ascending distance.
        """
        target_point = ST_GeogFromWKB(
            ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        )

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

        result = await self.db.exec(query)
        rows = result.all()

        return [
            PeakWithDistance(peak=peak, distance=float(distance))
            for peak, distance in rows
        ]

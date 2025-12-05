"""
Service for matching geographical coordinates to peaks
"""

from typing import List, Optional

from src.peaks.models import Peak, PeakWithDistance
from src.peaks.repository import PeaksRepository
from src.sorting.models import SortParams


class PeaksService:
    """
    Service for matching geographical coordinates to peaks
    based on haversine distance calculation.
    """

    def __init__(self, peaks_repository: PeaksRepository):
        self.peaks_repository = peaks_repository

    async def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        return await self.peaks_repository.get_all()

    async def get_count(self) -> int:
        return await self.peaks_repository.get_count()

    async def get_by_id(self, peak_id: int) -> Peak:
        """
        Retrieve a peak by its ID.

        Returns:
            Peak with the given ID

        Raises:
            NotFoundException: If no peak with the given ID exists
        """
        return await self.peaks_repository.get_by_id(peak_id)

    async def search_peaks(
        self,
        sort_params: Optional[SortParams] = None,
        name_filter: str | None = None,
        limit: int = 5,
    ) -> List[Peak]:
        return await self.peaks_repository.search(
            name_filter=name_filter, limit=limit, sort_params=sort_params
        )

    async def find_nearby_peaks(
        self,
        lat: float,
        lng: float,
        max_distance: float | None = None,
        name_filter: str | None = None,
        limit: int = 5,
    ) -> List[PeakWithDistance]:
        """
        Find peaks near a given location.

        Args:
            lat: Latitude of the point
            lng: Longitude of the point
            max_distance: Optional maximum distance in meters to include
            name_filter: Optional substring to filter peak names (case-insensitive)
            limit: Maximum number of peaks to return (default: 5)

        Returns:
            List of PeakWithDistance models containing peak and distance from the point
        """
        return await self.peaks_repository.find_nearby(
            lat=lat,
            lng=lng,
            max_distance=max_distance,
            name_filter=name_filter,
            limit=limit,
        )

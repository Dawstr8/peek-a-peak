"""
Service for matching geographical coordinates to peaks
"""

from typing import List, Optional

from src.peaks.models import Peak, PeakWithDistance
from src.peaks.repository import PeaksRepository


class PeaksService:
    """
    Service for matching geographical coordinates to peaks
    based on haversine distance calculation.
    """

    def __init__(self, peaks_repository: PeaksRepository):
        """
        Initialize the PeaksService

        Args:
            peaks_repository: Repository for accessing peak data
        """
        self.peaks_repository = peaks_repository

    async def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        return await self.peaks_repository.get_all()

    async def get_by_id(self, peak_id: int) -> Optional[Peak]:
        """
        Get a specific peak by ID.

        Args:
            peak_id: ID of the peak to retrieve

        Returns:
            Peak if found, None otherwise
        """
        return await self.peaks_repository.get_by_id(peak_id)

    async def find_nearest_peaks(
        self,
        latitude: float,
        longitude: float,
        max_distance: float | None = None,
        limit: int = 5,
    ) -> List[PeakWithDistance]:
        """
        Find the nearest peaks to a given latitude and longitude.

        Args:
            latitude: Latitude of the point
            longitude: Longitude of the point
            max_distance: Optional maximum distance in meters to include
            limit: Maximum number of peaks to return (default: 5)

        Returns:
            List of dictionaries containing peak and its distance from the point
        """
        return await self.peaks_repository.get_nearest(
            latitude=latitude,
            longitude=longitude,
            max_distance=max_distance,
            limit=limit,
        )

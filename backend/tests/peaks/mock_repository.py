from typing import Optional
from uuid import UUID

from src.peaks.models import Peak, PeakWithDistance
from src.peaks.repository import PeaksRepository
from src.sorting.models import SortParams
from tests.database.base_mock_repository import BaseMockRepository


class MockPeaksRepository(BaseMockRepository[Peak]):
    repository_class = PeaksRepository
    model = Peak

    def __init__(self, coords_map: dict[str, tuple[float, float]], **kwargs):
        super().__init__(**kwargs)

        self._coords_map = coords_map

    def _setup_custom_methods(self):
        async def get_count() -> int:
            return len(self.items)

        async def get_summited_by_user_count(user_id: UUID) -> int:
            return 2

        async def search(
            sort_params: Optional[SortParams] = None,
            name_filter: Optional[str] = None,
            limit: int = 5,
        ):
            results = self.items
            if name_filter:
                results = [
                    peak for peak in results if name_filter.lower() in peak.name.lower()
                ]

            if sort_params:
                reverse = sort_params.order == "desc"
                if sort_params.sort_by == "name":
                    results = sorted(results, key=lambda p: p.name, reverse=reverse)
                elif sort_params.sort_by == "elevation":
                    results = sorted(
                        results, key=lambda p: p.elevation, reverse=reverse
                    )

            return list(results)[:limit]

        async def find_nearby(
            lat: float, lng: float, max_distance=None, name_filter=None, limit=5
        ):
            coords_map = self._coords_map
            [rysy, giewont, babia_gora] = self.items

            if (lat, lng) == coords_map["near_rysy"]:
                results = [
                    PeakWithDistance(peak=rysy, distance=50.0),
                    PeakWithDistance(peak=giewont, distance=30000.0),
                    PeakWithDistance(peak=babia_gora, distance=80000.0),
                ]
            elif (lat, lng) == coords_map["near_sniezka"]:
                results = [
                    PeakWithDistance(peak=giewont, distance=150000.0),
                    PeakWithDistance(peak=babia_gora, distance=250000.0),
                    PeakWithDistance(peak=rysy, distance=400000.0),
                ]
            elif (lat, lng) == coords_map["warsaw"]:
                results = [
                    PeakWithDistance(peak=babia_gora, distance=250000.0),
                    PeakWithDistance(peak=giewont, distance=300000.0),
                    PeakWithDistance(peak=rysy, distance=400000.0),
                ]

            results_within_distance = [
                result
                for result in results
                if max_distance is None or result.distance <= max_distance
            ]

            if name_filter:
                results_within_distance = [
                    result
                    for result in results_within_distance
                    if name_filter.lower() in result.peak.name.lower()
                ]

            return results_within_distance[:limit]

        self._add_method("get_count", get_count)
        self._add_method("get_summited_by_user_count", get_summited_by_user_count)
        self._add_method("search", search)
        self._add_method("find_nearby", find_nearby)

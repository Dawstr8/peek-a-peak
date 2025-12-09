from src.pagination.models import PaginationParams
from src.photos.models import SummitPhoto, SummitPhotoDate, SummitPhotoLocation
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from tests.database.base_mock_repository import BaseMockRepository


class MockPhotosRepository(BaseMockRepository[SummitPhoto]):
    repository_class = PhotosRepository
    model = SummitPhoto

    def _setup_custom_methods(self):
        async def get_by_owner_id(
            owner_id,
            sort_params=SortParams(),
            pagination_params=PaginationParams(),
        ):
            return [photo for photo in self.items if photo.owner_id == owner_id]

        async def get_locations_by_owner_id(owner_id, sort_params=None):
            return [
                SummitPhotoLocation(
                    id=photo.id, lat=photo.lat, lng=photo.lng, alt=photo.alt
                )
                for photo in self.items
                if photo.owner_id == owner_id and photo.location is not None
            ]

        async def get_dates_by_owner_id(owner_id, sort_params=None):
            return [
                SummitPhotoDate(id=photo.id, captured_at=photo.captured_at)
                for photo in self.items
                if photo.owner_id == owner_id
            ]

        self._add_method("get_by_owner_id", get_by_owner_id)
        self._add_method("get_locations_by_owner_id", get_locations_by_owner_id)
        self._add_method("get_dates_by_owner_id", get_dates_by_owner_id)

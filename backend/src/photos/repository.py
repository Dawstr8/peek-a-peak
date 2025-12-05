from typing import List

from sqlalchemy.orm import load_only
from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.pagination.models import PaginatedResponse, PaginationParams
from src.photos.models import SummitPhoto, SummitPhotoDate, SummitPhotoLocation
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting


class PhotosRepository(BaseRepository[SummitPhoto]):
    """
    Repository for SummitPhoto data access operations.
    """

    model = SummitPhoto

    async def get_by_owner_id(
        self,
        owner_id: int,
        sort_params: SortParams,
        pagination_params: PaginationParams,
    ) -> PaginatedResponse[SummitPhoto]:
        statement = select(SummitPhoto).where(SummitPhoto.owner_id == owner_id)
        statement = apply_sorting(statement, SummitPhoto, sort_params)
        return await self.paginator.paginate(statement, pagination_params)

    async def get_locations_by_owner_id(
        self, owner_id: int
    ) -> List[SummitPhotoLocation]:
        statement = (
            select(SummitPhoto)
            .where(SummitPhoto.owner_id == owner_id)
            .where(SummitPhoto.location != None)
            .options(load_only(SummitPhoto.id, SummitPhoto.location, SummitPhoto.alt))
        )
        result = await self.db.exec(statement)
        return result.all()

    async def get_dates_by_owner_id(self, owner_id: int) -> List[SummitPhotoDate]:
        statement = (
            select(SummitPhoto)
            .where(SummitPhoto.owner_id == owner_id)
            .options(load_only(SummitPhoto.id, SummitPhoto.captured_at))
        )
        result = await self.db.exec(statement)
        return result.all()

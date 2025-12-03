from typing import List

from src.common.exceptions import NotFoundException
from src.pagination.models import PaginatedResponse, PaginationParams
from src.peaks.repository import PeaksRepository
from src.photos.models import SummitPhoto, SummitPhotoDate, SummitPhotoLocation
from src.photos.repository import PhotosRepository
from src.sorting.models import SortParams
from src.users.models import User, UserUpdate
from src.users.repository import UsersRepository


class UsersService:
    def __init__(
        self,
        users_repository: UsersRepository,
        photos_repository: PhotosRepository,
        peaks_repository: PeaksRepository,
    ):
        self.users_repository = users_repository
        self.photos_repository = photos_repository
        self.peaks_repository = peaks_repository

    async def get_user(self, owner_id: int) -> User:
        return await self.users_repository.get_by_id(owner_id)

    async def get_user_by_username(self, username: str) -> User:
        user = await self.users_repository.get_by_username(username)
        if not user:
            raise NotFoundException(f"User {username} not found.")

        return user

    async def update_user(self, owner_id: int, user_update: UserUpdate) -> User:
        return await self.users_repository.update(owner_id, user_update)

    async def get_photos_by_user(
        self,
        owner_id: int,
        sort_params: SortParams,
        pagination_params: PaginationParams,
    ) -> PaginatedResponse[SummitPhoto]:
        return await self.photos_repository.get_by_owner_id(
            owner_id,
            sort_params=sort_params,
            pagination_params=pagination_params,
        )

    async def get_photos_locations_by_user(
        self, owner_id: int
    ) -> List[SummitPhotoLocation]:
        return await self.photos_repository.get_locations_by_owner_id(owner_id)

    async def get_photos_dates_by_user(self, owner_id: int) -> List[SummitPhotoDate]:
        return await self.photos_repository.get_dates_by_owner_id(owner_id)

    async def get_summited_peaks_count_by_user(self, owner_id: int) -> int:
        return await self.peaks_repository.get_summited_by_user_count(owner_id)

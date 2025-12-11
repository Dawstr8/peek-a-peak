from typing import List
from uuid import UUID

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

    async def get_user(self, owner_id: UUID) -> User:
        """
        Retrieve a user by their ID.

        Returns:
            User with the given ID

        Raises:
            NotFoundException: If no user with the given ID exists
        """
        return await self.users_repository.get_by_id(owner_id)

    async def get_user_by_username(self, username: str) -> User:
        return await self.users_repository.get_by_field("username", username)

    async def update_user(self, owner_id: UUID, user_update: UserUpdate) -> User:
        return await self.users_repository.update(owner_id, user_update)

    async def get_photos_by_user(
        self,
        owner_id: UUID,
        sort_params: SortParams,
        pagination_params: PaginationParams,
    ) -> PaginatedResponse[SummitPhoto]:
        return await self.photos_repository.get_by_owner_id(
            owner_id,
            sort_params=sort_params,
            pagination_params=pagination_params,
        )

    async def get_photos_locations_by_user(
        self, owner_id: UUID
    ) -> List[SummitPhotoLocation]:
        return await self.photos_repository.get_locations_by_owner_id(owner_id)

    async def get_photos_dates_by_user(self, owner_id: UUID) -> List[SummitPhotoDate]:
        return await self.photos_repository.get_dates_by_owner_id(owner_id)

    async def get_summited_peaks_count_by_user(self, owner_id: UUID) -> int:
        return await self.peaks_repository.get_summited_by_user_count(owner_id)

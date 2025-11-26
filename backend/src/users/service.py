from typing import List, Optional

from src.models import SortParams
from src.peaks.repository import PeaksRepository
from src.photos.models import SummitPhoto
from src.photos.repository import PhotosRepository
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

    async def get_photos_by_user(
        self, username: str, sort_params: Optional[SortParams] = None
    ) -> List[SummitPhoto]:
        user = await self.users_repository.get_by_username(username)
        return await self.photos_repository.get_by_owner_id(
            user.id, sort_params=sort_params
        )

    async def get_summited_peaks_count_by_user(self, username: str) -> int:
        user = await self.users_repository.get_by_username(username)
        return await self.peaks_repository.get_summited_by_user_count(user.id)

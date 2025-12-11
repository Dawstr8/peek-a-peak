from uuid import UUID

from src.users.models import User, UserUpdate
from src.users.repository import UsersRepository
from tests.database.base_mock_repository import BaseMockRepository


class MockUsersRepository(BaseMockRepository[User]):
    repository_class = UsersRepository
    model = User

    def _setup_custom_methods(self):
        async def update(user_id: UUID, user_update: UserUpdate) -> User:
            user = await self.mock.get_by_id(user_id)

            for field, value in user_update.model_dump(exclude_unset=True).items():
                setattr(user, field, value)

            return await self.mock.save(user)

        self._add_method("update", update)

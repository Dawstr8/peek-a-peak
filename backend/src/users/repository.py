from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.users.models import User, UserUpdate


class UsersRepository(BaseRepository[User]):
    """
    Repository for User data access operations.
    """

    model = User

    async def save(self, user: User) -> User:
        """
        Save a user with proper integrity constraint handling.

        Args:
            user: User instance to save

        Returns:
            The saved User object

        Raises:
            ValueError: If email or username constraints are violated
        """
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            error_str = str(e).lower()
            if "duplicate key" in error_str:
                if "ix_user_email" in error_str:
                    raise ValueError("Email is already in use.")
                if "ix_user_username" in error_str:
                    raise ValueError("Username is already taken.")
            raise

        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_update: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.users.models import User, UserUpdate


class UsersRepository(BaseRepository):
    """
    Repository for User data access operations.
    """

    async def save(self, user: User) -> User:
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
        if not user:
            raise ValueError("User not found.")

        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)

        result = await self.db.exec(statement)
        return result.first()

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        result = await self.db.exec(statement)
        return result.first()

    async def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)

        result = await self.db.exec(statement)
        return result.first()

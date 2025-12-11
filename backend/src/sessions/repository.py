from datetime import datetime, timedelta
from uuid import UUID

from sqlmodel import select

from src.database.base_repository import BaseRepository
from src.sessions.models import Session as UserSession


class SessionsRepository(BaseRepository[UserSession]):
    """
    Repository for managing user sessions.
    """

    model = UserSession

    async def create(self, user_id: UUID, expires_in_days: int) -> UserSession:
        """
        Create a new user session.

        Args:
            user_id: ID of the user to create session for
            expires_in_days: Number of days until session expiration

        Returns:
            Created session object
        """
        session = UserSession(
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_active_by_id(self, session_id: UUID) -> UserSession | None:
        """
        Get an active session by ID.

        Args:
            session_id: UUID of the session to retrieve

        Returns:
            Session if found and active, else None
        """
        statement = select(UserSession).where(
            UserSession.id == session_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow(),
        )

        result = await self.db.exec(statement)
        return result.first()

    async def invalidate_by_id(self, session_id: UUID) -> None:
        """
        Invalidate a session.

        Args:
            session_id: UUID of the session to invalidate
        """
        session = await self.get_active_by_id(session_id)

        if session:
            session.is_active = False
            await self.db.commit()

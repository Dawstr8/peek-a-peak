from uuid import UUID

from src.auth.exceptions import InvalidCredentialsException
from src.auth.password_service import PasswordService
from src.common.exceptions import NotFoundException
from src.sessions.repository import SessionsRepository
from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


class AuthService:
    """
    Service for user operations.
    """

    def __init__(
        self,
        users_repository: UsersRepository,
        sessions_repository: SessionsRepository,
        password_service: PasswordService,
    ):
        self.users_repository = users_repository
        self.sessions_repository = sessions_repository
        self.password_service = password_service

    async def authenticate_user(self, email_or_username: str, password: str) -> User:
        """
        Authenticate a user by email/username and password.

        Returns:
            The authenticated User object.

        Raises:
            InvalidCredentialsException: If authentication fails.
        """
        email_or_username = email_or_username.lower()

        try:
            user = (
                await self.users_repository.get_by_field("email", email_or_username)
                if "@" in email_or_username
                else await self.users_repository.get_by_field(
                    "username", email_or_username
                )
            )

            if not self.password_service.verify(password, user.hashed_password):
                raise InvalidCredentialsException()

            return user
        except NotFoundException:
            raise InvalidCredentialsException()

    async def register_user(self, user_create: UserCreate) -> User:
        """Register a new user."""
        hashed_password = self.password_service.get_hash(user_create.password)

        user = User(
            hashed_password=hashed_password,
            **user_create.model_dump(exclude={"email", "username"}),
            email=user_create.email.lower(),
            username=user_create.username.lower(),
            username_display=user_create.username
        )

        return await self.users_repository.save(user)

    async def login_user(self, email_or_username: str, password: str) -> UUID:
        """
        Log in a user by authenticating their credentials and creating a new session.

        Returns:
            The session ID (UUID) for the created session.

        Raises:
            InvalidCredentialsException: If authentication fails.
        """
        user = await self.authenticate_user(email_or_username, password)
        session = await self.sessions_repository.create(user.id, expires_in_days=30)

        return session.id

    async def logout_user(self, session_id: UUID) -> None:
        """Log out a user by invalidating their session."""
        await self.sessions_repository.invalidate_by_id(session_id)

    async def get_current_user(self, session_id: UUID) -> User:
        """
        Get the current authenticated user from a session ID.

        Returns:
            The authenticated User object.

        Raises:
            NotFoundException: If the session is invalid or expired.
            NotFoundException: If the user is not found.
        """
        session = await self.sessions_repository.get_active_by_id(session_id)
        if not session:
            raise NotFoundException("Invalid or expired session")

        return await self.users_repository.get_by_id(session.user_id)

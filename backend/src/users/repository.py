from sqlmodel import Session, select

from src.users.models import User


class UsersRepository:
    """
    Repository for User data access operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the UsersRepository.

        Args:
            db: Database session
        """
        self.db = db

    def save(self, user: User) -> User:
        """
        Save a user to the database. Raises ValueError if email already exists.

        Args:
            user: The User to save

        Returns:
            The saved User object with database ID assigned
        """
        from sqlalchemy.exc import IntegrityError

        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            error_str = str(e).lower()
            if "unique" in error_str:
                if "user.email" in error_str:
                    raise ValueError("Email is already in use.")
                if "user.username" in error_str:
                    raise ValueError("Username is already taken.")
            raise

        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """
        Get a user by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            User if found, else None
        """
        statement = select(User).where(User.id == user_id)

        return self.db.exec(statement).first()

    def get_by_email(self, email: str) -> User | None:
        """
        Get a user by email.

        Args:
            email: Email of the user to retrieve

        Returns:
            User if found, else None
        """
        statement = select(User).where(User.email == email)

        return self.db.exec(statement).first()

    def get_by_username(self, username: str) -> User | None:
        """
        Get a user by username.

        Args:
            username: Username of the user to retrieve

        Returns:
            User if found, else None
        """
        statement = select(User).where(User.username == username)

        return self.db.exec(statement).first()

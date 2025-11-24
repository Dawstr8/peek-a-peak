import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator
from sqlmodel import Field, SQLModel

from src.models import CamelModel


class User(SQLModel, table=True):
    """Database model for a user"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    username: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(CamelModel):
    """Request model for creating a new user"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=1)

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_.-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, hyphens, and periods"
            )

        return v


class UserRead(CamelModel):
    """Response model for user data without sensitive information"""

    email: str
    username: str
    created_at: datetime

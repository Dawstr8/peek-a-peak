import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator
from sqlmodel import Field

from src.common.models import CamelModel
from src.database.models import BaseTableModel


class User(BaseTableModel, table=True):
    email: str = Field(index=True, nullable=False, unique=True)
    username: str = Field(index=True, nullable=False, unique=True)
    username_display: str
    hashed_password: str
    is_private: bool = Field(default=False)


class UserCreate(CamelModel):
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


class UserUpdate(CamelModel):
    is_private: Optional[bool] = None


class UserRead(CamelModel):
    email: str
    username: str
    username_display: str
    is_private: bool
    created_at: datetime

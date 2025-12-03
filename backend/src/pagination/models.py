from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

from src.common.models import CamelModel


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 10


T = TypeVar("T", bound=SQLModel)


class PaginatedResponse(CamelModel, Generic[T]):
    total: int
    page: int
    per_page: int
    items: list[T]

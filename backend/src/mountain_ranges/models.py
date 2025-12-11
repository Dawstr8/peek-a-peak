from sqlmodel import Field

from src.database.models import BaseTableModel


class MountainRange(BaseTableModel, table=True):
    name: str = Field(index=True, unique=True)

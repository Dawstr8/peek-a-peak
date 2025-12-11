from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from src.database.models import BaseTableModel


class Session(BaseTableModel, table=True):
    """Database model for user sessions"""

    user_id: UUID = Field(foreign_key="user.id", index=True)
    expires_at: datetime
    is_active: bool = Field(default=True)

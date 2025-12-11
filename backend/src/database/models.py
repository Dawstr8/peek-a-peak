from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql as psql
from sqlmodel import Field, SQLModel


class BaseTableModel(SQLModel):
    """Base model for all database tables with UUID primary key and created_at timestamp."""

    id: UUID = Field(
        sa_type=psql.UUID(as_uuid=True),
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

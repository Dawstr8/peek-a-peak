from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.peaks.models import Peak
from src.users.models import User


class SummitPhoto(SQLModel, table=True):
    """Database model for a summit photo with metadata"""

    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    captured_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    distance_to_peak: Optional[float] = None

    owner_id: int = Field(foreign_key="user.id")
    peak_id: Optional[int] = Field(default=None, foreign_key="peak.id")

    peak: Optional[Peak] = Relationship()


class SummitPhotoCreate(BaseModel):
    """Request model for creating a new photo with metadata"""

    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    distance_to_peak: Optional[float] = None

    peak_id: Optional[int] = None

    @field_validator("captured_at")
    @classmethod
    def validate_captured_at_timezone(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return v
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError(
                "captured_at must be timezone-aware (include offset or tzinfo)."
            )

        return v


class SummitPhotoRead(BaseModel):
    """Response model for reading a photo with metadata"""

    id: int
    file_name: str
    uploaded_at: datetime
    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    distance_to_peak: Optional[float] = None

    peak_id: Optional[int] = None
    owner_id: int

    peak: Optional[Peak] = None

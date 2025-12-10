from datetime import datetime
from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape
from pydantic import field_validator
from shapely.geometry import Point
from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.common.models import CamelModel
from src.peaks.models import ReadPeak
from src.users.models import User

if TYPE_CHECKING:
    from src.peaks.models import Peak


class SummitPhoto(SQLModel, table=True):
    """Database model for a summit photo with metadata"""

    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    peak_id: Optional[int] = Field(default=None, foreign_key="peak.id")
    peak: Optional["Peak"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    file_name: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    captured_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    location: Optional[object] = Field(
        sa_column=Column(Geography(geometry_type="POINT", srid=4326))
    )
    alt: Optional[float] = None

    @property
    def lat(self) -> Optional[float]:
        if not self.location:
            return None

        point: Point = to_shape(self.location)
        return point.y

    @property
    def lng(self) -> Optional[float]:
        if not self.location:
            return None

        point: Point = to_shape(self.location)
        return point.x


class SummitPhotoCreate(CamelModel):
    """Request model for creating a new photo with metadata"""

    captured_at: datetime
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None

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


class SummitPhotoRead(CamelModel):
    """Response model for reading a photo with metadata"""

    id: int
    file_name: str
    uploaded_at: datetime
    captured_at: datetime
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None

    peak_id: Optional[int] = None
    owner_id: int

    peak: Optional[ReadPeak] = None


class SummitPhotoLocation(CamelModel):
    """Model representing the location of a summit photo"""

    id: int
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None


class SummitPhotoDate(CamelModel):
    """Model representing the captured dates of summit photos"""

    id: int
    captured_at: datetime

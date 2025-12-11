from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape
from pydantic import field_validator
from shapely.geometry import Point
from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship

from src.common.models import CamelModel
from src.database.models import BaseTableModel
from src.peaks.models import ReadPeak
from src.users.models import User
from src.weather.models import WeatherRecordRead

if TYPE_CHECKING:
    from src.peaks.models import Peak
    from src.weather.models import WeatherRecord


class SummitPhoto(BaseTableModel, table=True):
    """Database model for a summit photo with metadata"""

    owner_id: UUID = Field(foreign_key="user.id")
    owner: User = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    peak_id: Optional[UUID] = Field(default=None, foreign_key="peak.id")
    peak: Optional["Peak"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    weather_record: Optional["WeatherRecord"] = Relationship(
        back_populates="photo",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )

    file_name: str
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

    peak_id: Optional[UUID] = None

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

    id: UUID

    owner_id: UUID

    peak_id: Optional[UUID] = None
    peak: Optional[ReadPeak] = None

    weather_record: Optional[WeatherRecordRead] = None

    file_name: str
    created_at: datetime
    captured_at: datetime
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None


class SummitPhotoLocation(CamelModel):
    """Model representing the location of a summit photo"""

    id: UUID
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None


class SummitPhotoDate(CamelModel):
    """Model representing the captured dates of summit photos"""

    id: UUID
    captured_at: datetime

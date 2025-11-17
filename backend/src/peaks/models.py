from datetime import datetime
from typing import Optional

from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape
from pydantic import BaseModel
from shapely.geometry import Point
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from src.mountain_ranges.models import MountainRange


class Peak(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    elevation: int
    location: Optional[object] = Field(
        sa_column=Column(Geography(geometry_type="POINT", srid=4326))
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    mountain_range_id: int = Field(foreign_key="mountainrange.id")
    mountain_range: MountainRange = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    @property
    def latitude(self) -> Optional[float]:
        if not self.location:
            return None

        point: Point = to_shape(self.location)
        return point.y

    @property
    def longitude(self) -> Optional[float]:
        if not self.location:
            return None

        point: Point = to_shape(self.location)
        return point.x


class ReadPeak(BaseModel):
    """Response model for reading peak information"""

    id: int
    name: str
    elevation: int
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime

    mountain_range: MountainRange


class PeakWithDistance(BaseModel):
    """Model representing a peak along with its distance from a reference point"""

    peak: Peak
    distance: float


class ReadPeakWithDistance(BaseModel):
    """Response model for peak with distance information"""

    peak: ReadPeak
    distance: float

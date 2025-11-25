from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from sqlalchemy import Column, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from src.models import CamelModel
from src.mountain_ranges.models import MountainRange

if TYPE_CHECKING:
    from src.photos.models import SummitPhoto


class Peak(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "elevation",
            "mountain_range_id",
            name="uq_peak_name_elevation_mountain_range",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    elevation: int
    location: Optional[object] = Field(
        sa_column=Column(Geography(geometry_type="POINT", srid=4326))
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    wiki_page: Optional[str] = None

    mountain_range_id: int = Field(foreign_key="mountainrange.id")
    mountain_range: MountainRange = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    summit_photos: List["SummitPhoto"] = Relationship(
        back_populates="peak", sa_relationship_kwargs={"lazy": "selectin"}
    )

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


class ReadPeak(CamelModel):
    """Response model for reading peak information"""

    id: int
    name: str
    elevation: int
    lat: Optional[float]
    lng: Optional[float]
    created_at: datetime

    mountain_range: MountainRange


class PeakWithDistance(CamelModel):
    """Model representing a peak along with its distance from a reference point"""

    peak: Peak
    distance: float


class ReadPeakWithDistance(CamelModel):
    """Response model for peak with distance information"""

    peak: ReadPeak
    distance: float

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.common.models import CamelModel

if TYPE_CHECKING:
    from src.photos.models import SummitPhoto


class WeatherRecordWeatherConditionLink(SQLModel, table=True):
    record_id: int = Field(foreign_key="weatherrecord.id", primary_key=True)
    condition_id: int = Field(foreign_key="weathercondition.id", primary_key=True)


class WeatherCondition(SQLModel, table=True):
    """Database model for weather conditions"""

    id: Optional[int] = Field(default=None, primary_key=True)
    api_id: int = Field(
        description="ID of the weather condition from the weather API",
        unique=True,
        index=True,
    )
    main: Optional[str] = Field(
        default=None,
        description="Group of weather parameters (Rain, Snow, Extreme etc.)",
    )
    description: Optional[str] = Field(
        default=None, description="Weather condition within the group"
    )
    icon: Optional[str] = Field(default=None, description="Weather icon id")


class WeatherRecord(SQLModel, table=True):
    """Database model for detailed weather records"""

    id: Optional[int] = Field(default=None, primary_key=True)

    photo_id: int = Field(foreign_key="summitphoto.id", ondelete="CASCADE")
    photo: "SummitPhoto" = Relationship(
        back_populates="weather_record",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    conditions: list[WeatherCondition] = Relationship(
        sa_relationship_kwargs={
            "secondary": "weatherrecordweatherconditionlink",
            "lazy": "selectin",
        },
    )

    # Solar times
    sunrise: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
        description="Sunrise time, UTC",
    )
    sunset: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
        description="Sunset time, UTC",
    )
    # Temperature measurements
    temp: Optional[float] = Field(default=None, description="Temperature in Celsius")
    feels_like: Optional[float] = Field(
        default=None,
        description="Temperature in Celsius perceived by humans",
    )
    dew_point: Optional[float] = Field(
        default=None, description="Atmospheric temperature in Celsius"
    )

    # Atmospheric conditions
    pressure: Optional[int] = Field(
        default=None, description="Atmospheric pressure on the sea levelin hPa"
    )
    humidity: Optional[int] = Field(default=None, description="Humidity percentage")
    clouds: Optional[int] = Field(default=None, description="Cloudiness percentage")
    visibility: Optional[int] = Field(
        default=None, description="Average visibility in meters"
    )

    # Wind conditions
    wind_speed: Optional[float] = Field(
        default=None, description="Wind speed in meter/sec"
    )
    wind_deg: Optional[int] = Field(
        default=None, description="Wind direction in degrees (meteorological)"
    )

    # Precipitation
    rain: Optional[float] = Field(
        default=None, description="Precipitation for the last 1 hour in mm/h"
    )
    snow: Optional[float] = Field(
        default=None, description="Precipitation for the last 1 hour in mm/h"
    )


class WeatherConditionRead(CamelModel):
    main: Optional[str]
    description: Optional[str]
    icon: Optional[str]


class WeatherRecordRead(CamelModel):
    sunrise: Optional[datetime]
    sunset: Optional[datetime]
    temp: Optional[float]
    feels_like: Optional[float]
    dew_point: Optional[float]
    pressure: Optional[int]
    humidity: Optional[int]
    clouds: Optional[int]
    visibility: Optional[int]
    wind_speed: Optional[float]
    wind_deg: Optional[int]
    rain: Optional[float]
    snow: Optional[float]
    conditions: list[WeatherConditionRead]

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class WeatherCondition(SQLModel, table=True):
    """Database model for weather conditions"""

    id: Optional[int] = Field(default=None, primary_key=True)
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
    photo_id: int = Field(foreign_key="summitphoto.id")

    # Solar times
    sunrise: datetime = Field(default=None, description="Sunrise time, UTC")
    sunset: datetime = Field(default=None, description="Sunset time, UTC")

    # Temperature measurements
    temp: float = Field(default=None, description="Temperature in Celsius")
    feels_like: float = Field(
        default=None,
        description="Temperature in Celsius perceived by humans",
    )
    dew_point: float = Field(
        default=None, description="Atmospheric temperature in Celsius"
    )

    # Atmospheric conditions
    pressure: int = Field(
        default=None, description="Atmospheric pressure on the sea levelin hPa"
    )
    humidity: int = Field(default=None, description="Humidity percentage")
    clouds: int = Field(default=None, description="Cloudiness percentage")
    visibility: int = Field(default=None, description="Average visibility in meters")

    # Wind conditions
    wind_speed: float = Field(default=None, description="Wind speed in meter/sec")
    wind_deg: int = Field(
        default=None, description="Wind direction in degrees (meteorological)"
    )

    # Precipitation
    rain: float = Field(
        default=None, description="Precipitation for the last 1 hour in mm/h"
    )
    snow: float = Field(
        default=None, description="Precipitation for the last 1 hour in mm/h"
    )

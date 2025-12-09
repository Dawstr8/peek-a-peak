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

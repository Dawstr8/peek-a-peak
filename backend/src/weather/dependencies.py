from typing import Annotated

from fastapi import Depends

from config import settings
from src.common.dependencies import api_client_dep
from src.database.core import db_dep

from .client import OpenWeatherMapClient
from .repository import WeatherConditionsRepository, WeatherRecordsRepository
from .service import WeatherService


def get_weather_conditions_repository(db: db_dep) -> WeatherConditionsRepository:
    return WeatherConditionsRepository(db)


def get_weather_records_repository(db: db_dep) -> WeatherRecordsRepository:
    return WeatherRecordsRepository(db)


def get_openweathermap_client(
    client: api_client_dep,
) -> OpenWeatherMapClient:
    return OpenWeatherMapClient(
        api_key=settings.openweather_api_key,
        base_url=settings.openweather_base_url,
        client=client,
    )


weather_client_dep = Annotated[OpenWeatherMapClient, Depends(get_openweathermap_client)]


def get_weather_service(
    client: weather_client_dep,
    conditions_repository: WeatherConditionsRepository = Depends(
        get_weather_conditions_repository
    ),
    records_repository: WeatherRecordsRepository = Depends(
        get_weather_records_repository
    ),
) -> WeatherService:
    return WeatherService(
        conditions_repository=conditions_repository,
        records_repository=records_repository,
        client=client,
    )


weather_service_dep = Annotated[WeatherService, Depends(get_weather_service)]

__all__ = ["weather_client_dep", "weather_service_dep"]

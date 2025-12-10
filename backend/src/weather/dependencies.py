from typing import Annotated

from fastapi import Depends

from config import settings
from src.common.dependencies import api_client_dep
from src.weather.client import OpenWeatherMapClient


async def get_openweathermap_client(
    client: api_client_dep,
) -> OpenWeatherMapClient:
    return OpenWeatherMapClient(
        api_key=settings.openweather_api_key,
        base_url=settings.openweather_base_url,
        client=client,
    )


weather_client_dep = Annotated[OpenWeatherMapClient, Depends(get_openweathermap_client)]

from datetime import datetime
from typing import Any, Dict

import httpx

from src.common.base_api_client import BaseAPIClient


class OpenWeatherMapClient(BaseAPIClient):
    service_name = "OpenWeatherMap"

    def __init__(self, api_key: str, base_url: str, client: httpx.AsyncClient):
        self.api_key = api_key
        self.base_url = base_url
        self.client = client

    async def get_historical_weather(
        self, lat: float, lng: float, dt: datetime
    ) -> Dict[str, Any]:
        """
        Retrieve historical weather data for a specific location and time.

        Uses the OpenWeatherMap Timemachine API endpoint to fetch historical weather data.

        Args:
            lat: Latitude of the location
            lng: Longitude of the location
            dt: The datetime for which to retrieve weather data

        Returns:
            Dict[str, Any]: Raw JSON response from OpenWeatherMap API

        Raises:
            ExternalServiceException: If the API request fails or returns an error
        """

        return await self.get(
            "/onecall/timemachine",
            params={
                "lat": lat,
                "lon": lng,
                "dt": int(dt.timestamp()),
                "appid": self.api_key,
                "units": "metric",
            },
        )

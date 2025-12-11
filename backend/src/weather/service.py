from datetime import datetime, timezone
from uuid import UUID

from src.common.exceptions import NotFoundException

from .client import OpenWeatherMapClient
from .models import WeatherCondition, WeatherRecord
from .repository import WeatherConditionsRepository, WeatherRecordsRepository


class WeatherService:
    def __init__(
        self,
        conditions_repository: WeatherConditionsRepository,
        records_repository: WeatherRecordsRepository,
        client: OpenWeatherMapClient,
    ):
        self.conditions_repository = conditions_repository
        self.records_repository = records_repository
        self.client = client

    async def fetch_and_save_weather(
        self, lat: float, lng: float, dt: datetime, photo_id: UUID
    ) -> WeatherRecord:
        weather_data = await self.client.get_historical_weather(
            lat, lng, int(dt.timestamp())
        )

        weather_record = self.parse_weather_record_data(weather_data)
        weather_conditions = self.parse_weather_conditions_data(weather_data)

        for condition in weather_conditions:
            try:
                condition = await self.conditions_repository.get_by_field(
                    "api_id", condition.api_id
                )
            except NotFoundException:
                pass

            weather_record.conditions.append(condition)

        weather_record.photo_id = photo_id
        return await self.records_repository.save(weather_record)

    def parse_weather_conditions_data(self, data: dict) -> list[WeatherCondition]:
        data = data["data"][0]

        return [
            WeatherCondition(
                api_id=item.get("id"),
                main=item.get("main"),
                description=item.get("description"),
                icon=item.get("icon"),
            )
            for item in data["weather"]
        ]

    def parse_weather_record_data(self, data: dict) -> WeatherRecord:
        data = data["data"][0]

        return WeatherRecord(
            sunrise=datetime.fromtimestamp(data.get("sunrise"), tz=timezone.utc),
            sunset=datetime.fromtimestamp(data.get("sunset"), tz=timezone.utc),
            temp=data.get("temp"),
            feels_like=data.get("feels_like"),
            dew_point=data.get("dew_point"),
            pressure=data.get("pressure"),
            humidity=data.get("humidity"),
            clouds=data.get("clouds"),
            visibility=data.get("visibility"),
            wind_speed=data.get("wind_speed"),
            wind_deg=data.get("wind_deg"),
            rain=data.get("rain", {}).get("1h"),
            snow=data.get("snow", {}).get("1h"),
        )

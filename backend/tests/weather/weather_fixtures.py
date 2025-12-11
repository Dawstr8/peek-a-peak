from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.photos.models import SummitPhoto
from src.weather.client import OpenWeatherMapClient
from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherConditionsRepository, WeatherRecordsRepository
from src.weather.service import WeatherService

from .mock_repository import (
    MockWeatherConditionsRepository,
    MockWeatherRecordsRepository,
)


@pytest.fixture
def weather_conditions() -> list[WeatherCondition]:
    """Create a list of weather conditions for testing"""
    return [
        WeatherCondition(api_id=800, main="Clear", description="clear sky", icon="01d"),
        WeatherCondition(
            api_id=804, main="Clouds", description="overcast clouds", icon="04d"
        ),
    ]


@pytest.fixture
def weather_records(
    photos: list[SummitPhoto], weather_conditions: list[WeatherCondition]
) -> list[WeatherRecord]:
    """Create a list of weather records for testing"""
    return [
        WeatherRecord(
            photo=photos[0],
            weather_conditions=weather_conditions,
            sunrise=datetime.fromtimestamp(1645866123),
            sunset=datetime.fromtimestamp(1645891727),
            temp=15.0,
            feels_like=14.0,
            dew_point=10.0,
            pressure=1015,
            humidity=60,
            clouds=20,
            visibility=10000,
            wind_speed=3.5,
            wind_deg=150,
            rain=0.0,
            snow=0.0,
        ),
        WeatherRecord(
            photo=photos[1],
            weather_conditions=[weather_conditions[1]],
            sunrise=datetime.fromtimestamp(1645880000),
            sunset=datetime.fromtimestamp(1645880000),
            temp=5.0,
            feels_like=3.0,
            dew_point=2.0,
            pressure=1020,
            humidity=80,
            clouds=90,
            visibility=8000,
            wind_speed=5.0,
            wind_deg=200,
            rain=1.2,
            snow=0.5,
        ),
    ]


@pytest.fixture
def sample_weather_client_response():
    return {
        "lat": 50.0,
        "lon": 20.0,
        "timezone": "Europe/Warsaw",
        "timezone_offset": 7200,
        "data": [
            {
                "dt": 1645886400,
                "sunrise": 1645866123,
                "sunset": 1645891727,
                "temp": 15.0,
                "feels_like": 14.0,
                "pressure": 1015,
                "humidity": 60,
                "dew_point": 10.0,
                "uvi": 5.0,
                "clouds": 20,
                "visibility": 10000,
                "wind_speed": 3.5,
                "wind_deg": 150,
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d",
                    },
                    {
                        "id": 804,
                        "main": "Clouds",
                        "description": "overcast clouds",
                        "icon": "04d",
                    },
                ],
                "rain": {"1h": 0.0},
                "snow": {"1h": 0.0},
            }
        ],
    }


@pytest.fixture
def mock_weather_client(sample_weather_client_response) -> OpenWeatherMapClient:
    client = AsyncMock(spec=OpenWeatherMapClient)

    async def get_historical_weather(lat: float, lon: float, dt: int):
        sample_weather_client_response["lat"] = lat
        sample_weather_client_response["lon"] = lon
        sample_weather_client_response["data"][0]["dt"] = dt

        return sample_weather_client_response

    client.get_historical_weather.side_effect = get_historical_weather

    return client


@pytest.fixture
def mock_weather_conditions_repository(
    weather_conditions: list[WeatherCondition],
) -> WeatherConditionsRepository:
    return MockWeatherConditionsRepository(items=weather_conditions).mock


@pytest.fixture
def mock_weather_records_repository(
    weather_records: list[WeatherRecord],
) -> WeatherRecordsRepository:
    return MockWeatherRecordsRepository(items=weather_records).mock


@pytest.fixture
def mock_weather_service() -> WeatherService:
    return AsyncMock(spec=WeatherService)

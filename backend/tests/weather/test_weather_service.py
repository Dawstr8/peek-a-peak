from datetime import datetime, timezone

import pytest

from src.weather.client import OpenWeatherMapClient
from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherConditionsRepository, WeatherRecordsRepository
from src.weather.service import WeatherService


@pytest.fixture
def mock_service(
    mock_weather_conditions_repository: WeatherConditionsRepository,
    mock_weather_records_repository: WeatherRecordsRepository,
    mock_weather_client: OpenWeatherMapClient,
) -> WeatherService:
    return WeatherService(
        conditions_repository=mock_weather_conditions_repository,
        records_repository=mock_weather_records_repository,
        client=mock_weather_client,
    )


@pytest.mark.asyncio
async def test_fetch_and_save_weather_success(
    mock_service,
    mock_weather_client: OpenWeatherMapClient,
    mock_weather_conditions_repository: WeatherConditionsRepository,
    mock_weather_records_repository: WeatherRecordsRepository,
):
    # Arrange
    lat = 40.7128
    lng = -74.0060
    dt = datetime(2022, 2, 26, 12, 0, 0)
    photo_id = 1

    # Act
    result = await mock_service.fetch_and_save_weather(lat, lng, dt, photo_id)

    # Assert
    assert result.id is not None

    mock_weather_client.get_historical_weather.assert_awaited_once_with(
        lat, lng, int(dt.timestamp())
    )
    mock_weather_conditions_repository.get_by_field.assert_awaited()
    mock_weather_records_repository.save.assert_awaited_once()


@pytest.mark.asyncio
async def parse_weather_conditions_data(mock_service, sample_weather_client_response):
    # Act
    conditions = mock_service.parse_weather_conditions_data(
        sample_weather_client_response
    )

    # Assert
    assert isinstance(conditions, list)
    assert len(conditions) == len(sample_weather_client_response["data"][0]["weather"])

    for condition in conditions:
        assert isinstance(condition, WeatherCondition)
        assert condition.api_id is not None
        assert condition.main is not None
        assert condition.description is not None
        assert condition.icon is not None


@pytest.mark.asyncio
async def test_parse_weather_data_full_data(
    mock_service, sample_weather_client_response
):
    # Act
    weather_record = mock_service.parse_weather_record_data(
        sample_weather_client_response
    )

    # Assert
    assert isinstance(weather_record, WeatherRecord)
    assert weather_record.sunrise == datetime.fromtimestamp(1645866123, tz=timezone.utc)
    assert weather_record.sunset == datetime.fromtimestamp(1645891727, tz=timezone.utc)
    assert weather_record.temp == 15.0
    assert weather_record.feels_like == 14.0
    assert weather_record.dew_point == 10.0
    assert weather_record.pressure == 1015
    assert weather_record.humidity == 60
    assert weather_record.clouds == 20
    assert weather_record.visibility == 10000
    assert weather_record.wind_speed == 3.5
    assert weather_record.wind_deg == 150
    assert weather_record.rain == 0.0
    assert weather_record.snow == 0.0


@pytest.mark.asyncio
async def test_parse_weather_data_missing_optional_fields(
    mock_service, sample_weather_client_response
):
    # Arrange
    sample_weather_client_response["data"][0].pop("feels_like")
    sample_weather_client_response["data"][0].pop("visibility")
    sample_weather_client_response["data"][0]["rain"] = {}
    sample_weather_client_response["data"][0]["snow"] = {}

    # Act
    weather_record = mock_service.parse_weather_record_data(
        sample_weather_client_response
    )

    # Assert
    assert isinstance(weather_record, WeatherRecord)
    assert weather_record.sunrise == datetime.fromtimestamp(1645866123, tz=timezone.utc)
    assert weather_record.sunset == datetime.fromtimestamp(1645891727, tz=timezone.utc)
    assert weather_record.temp == 15.0
    assert weather_record.feels_like is None
    assert weather_record.dew_point == 10.0
    assert weather_record.pressure == 1015
    assert weather_record.humidity == 60
    assert weather_record.clouds == 20
    assert weather_record.visibility is None
    assert weather_record.wind_speed == 3.5
    assert weather_record.wind_deg == 150
    assert weather_record.rain is None
    assert weather_record.snow is None

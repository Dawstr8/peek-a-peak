from datetime import datetime

import pytest

from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherConditionsRepository, WeatherRecordsRepository
from tests.database.mixins import BaseRepositoryMixin


class TestWeatherConditionsRepository(
    BaseRepositoryMixin[WeatherCondition, WeatherConditionsRepository]
):
    repository_class = WeatherConditionsRepository
    model_class = WeatherCondition
    sort_by = "main"

    @pytest.fixture()
    def db_items(self, db_weather_conditions) -> list[WeatherCondition]:
        return db_weather_conditions

    @pytest.fixture()
    def new_item(self) -> WeatherCondition:
        return WeatherCondition(
            id=500, main="Rain", description="light rain", icon="10n"
        )

    @pytest.fixture()
    def updated_item(self) -> WeatherCondition:
        return WeatherCondition(
            id=804, main="Clouds", description="overcast clouds", icon="04d"
        )


class TestWeatherRecordsRepository(
    BaseRepositoryMixin[WeatherRecord, WeatherRecordsRepository]
):
    repository_class = WeatherRecordsRepository
    model_class = WeatherRecord
    sort_by = "sunrise"

    @pytest.fixture()
    def db_items(self, db_weather_records) -> list[WeatherRecord]:
        return db_weather_records

    @pytest.fixture()
    def new_item(self, db_photos) -> WeatherRecord:
        return WeatherRecord(
            photo_id=db_photos[2].id,
            sunrise=datetime.fromtimestamp(1645900000),
            sunset=datetime.fromtimestamp(1645938000),
            temp=10.0,
            feels_like=8.0,
            dew_point=5.0,
            pressure=1018,
            humidity=70,
            clouds=50,
            visibility=9000,
            wind_speed=4.0,
            wind_deg=180,
            rain=0.5,
            snow=0.0,
        )

    @pytest.fixture()
    def updated_item(self, db_photos) -> WeatherRecord:
        return WeatherRecord(
            photo_id=db_photos[1].id,
            sunrise=datetime.fromtimestamp(1645910000),
            sunset=datetime.fromtimestamp(1645910000),
            temp=6.0,
            feels_like=4.0,
            dew_point=3.0,
            pressure=1022,
            humidity=75,
            clouds=95,
            visibility=7000,
            wind_speed=6.0,
            wind_deg=210,
            rain=1.5,
            snow=0.7,
        )

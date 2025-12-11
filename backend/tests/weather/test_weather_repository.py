from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherConditionsRepository, WeatherRecordsRepository
from tests.database.mixins import BaseRepositoryMixin


class TestWeatherConditionsRepository(
    BaseRepositoryMixin[WeatherCondition, WeatherConditionsRepository]
):
    repository_class = WeatherConditionsRepository
    model_class = WeatherCondition
    sort_by = "main"
    unique_fields = ["api_id"]

    items_fixture = "weather_conditions"


class TestWeatherRecordsRepository(
    BaseRepositoryMixin[WeatherRecord, WeatherRecordsRepository]
):
    repository_class = WeatherRecordsRepository
    model_class = WeatherRecord
    sort_by = "sunrise"

    items_fixture = "weather_records"

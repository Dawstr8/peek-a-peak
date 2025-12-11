from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherRecordsRepository
from src.weather.repository.weather_conditions import WeatherConditionsRepository
from tests.database.base_mock_repository import BaseMockRepository


class MockWeatherConditionsRepository(BaseMockRepository[WeatherCondition]):
    repository_class = WeatherConditionsRepository
    model = WeatherCondition


class MockWeatherRecordsRepository(BaseMockRepository[WeatherRecord]):
    repository_class = WeatherRecordsRepository
    model = WeatherRecord

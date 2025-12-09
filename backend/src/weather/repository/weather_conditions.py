from src.database.base_repository import BaseRepository
from src.weather.models import WeatherCondition


class WeatherConditionsRepository(BaseRepository[WeatherCondition]):
    model = WeatherCondition

from src.database.base_repository import BaseRepository
from src.weather.models import WeatherRecord


class WeatherRecordsRepository(BaseRepository[WeatherRecord]):
    model = WeatherRecord

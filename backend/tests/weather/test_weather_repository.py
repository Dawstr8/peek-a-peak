import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.weather.models import WeatherCondition
from src.weather.repository import WeatherConditionsRepository
from tests.database.mixins import BaseRepositoryMixin


class TestWeatherConditionsRepository(BaseRepositoryMixin):
    model_class = WeatherCondition
    sort_by = "main"

    @pytest.fixture
    def test_repository(self, test_db: AsyncSession) -> WeatherConditionsRepository:
        return WeatherConditionsRepository(test_db)

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

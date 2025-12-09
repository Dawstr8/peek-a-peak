import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.weather.models import WeatherCondition
from src.weather.repository import WeatherConditionsRepository


@pytest_asyncio.fixture
async def db_weather_conditions(test_db: AsyncSession) -> list[WeatherCondition]:
    repo = WeatherConditionsRepository(test_db)

    return await repo.save_all(
        [
            WeatherCondition(id=800, main="Clear", description="clear sky", icon="01d"),
            WeatherCondition(
                id=804, main="Clouds", description="overcast clouds", icon="04d"
            ),
        ]
    )

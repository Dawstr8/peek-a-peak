from datetime import datetime

import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.photos.models import SummitPhoto
from src.weather.models import WeatherCondition, WeatherRecord
from src.weather.repository import WeatherConditionsRepository, WeatherRecordsRepository


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


@pytest_asyncio.fixture
async def db_weather_records(
    test_db: AsyncSession,
    db_photos: list[SummitPhoto],
    db_weather_conditions: list[WeatherCondition],
) -> list[WeatherRecord]:
    repo = WeatherRecordsRepository(test_db)

    return await repo.save_all(
        [
            WeatherRecord(
                photo_id=db_photos[0].id,
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
                weather_conditions=db_weather_conditions,
            ),
            WeatherRecord(
                photo_id=db_photos[1].id,
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
                weather_conditions=[db_weather_conditions[1]],
            ),
        ]
    )

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_server_url: str = (
        "postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432".format(
            db_user=os.getenv("DB_USER", "postgres"),
            db_password=os.getenv("DB_PASSWORD", "postgres"),
            db_host=os.getenv("DB_HOST", "postgres"),
        )
    )
    database_url: str = "{postgres_server_url}/{db_name}".format(
        postgres_server_url=postgres_server_url,
        db_name=os.getenv("DB_NAME", "peek_a_peak"),
    )

    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
    openweather_base_url: str = os.getenv(
        "OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/3.0"
    )


settings = Settings()

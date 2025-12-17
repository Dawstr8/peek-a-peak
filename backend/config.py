import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")

    # CORS
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(
        ","
    )

    # Allowed hosts
    allowed_hosts: list[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")

    # Database settings
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

    # Weather API settings
    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
    openweather_base_url: str = os.getenv(
        "OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/3.0"
    )

    # Storage settings
    storage_type: str = os.getenv("STORAGE_TYPE", "local")

    # S3 settings
    s3_endpoint: str = os.getenv("S3_ENDPOINT", "minio:9000")
    s3_access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    s3_secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "peek-a-peak")
    s3_secure: bool = os.getenv("S3_SECURE", "false").lower() == "true"


settings = Settings()

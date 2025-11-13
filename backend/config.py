import os


class Config:
    POSTGRES_SERVER_URL = (
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432".format(
            DB_USER=os.getenv("DB_USER", "postgres"),
            DB_PASSWORD=os.getenv("DB_PASSWORD", "postgres"),
            DB_HOST=os.getenv("DB_HOST", "postgres"),
        )
    )
    DATABASE_URL = "{POSTGRES_SERVER_URL}/{DB_NAME}".format(
        POSTGRES_SERVER_URL=POSTGRES_SERVER_URL,
        DB_NAME=os.getenv("DB_NAME", "peek_a_peak"),
    )

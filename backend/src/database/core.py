from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=True)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as db:
        yield db


db_dep = Annotated[AsyncSession, Depends(get_db)]

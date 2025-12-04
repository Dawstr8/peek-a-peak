from sqlmodel.ext.asyncio.session import AsyncSession

from src.pagination.paginator import Paginator


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.paginator = Paginator(db)

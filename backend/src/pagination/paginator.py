from sqlalchemy import Select, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.pagination.models import PaginatedResponse, PaginationParams, T


class Paginator:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _apply_pagination(statement, pagination_params: PaginationParams):
        offset = (pagination_params.page - 1) * pagination_params.per_page
        return statement.offset(offset).limit(pagination_params.per_page)

    async def paginate(
        self,
        statement: Select[T],
        pagination_params: PaginationParams,
    ) -> PaginatedResponse[T]:
        total = await self.count_total(statement)

        paginated_statement = self._apply_pagination(statement, pagination_params)
        result = await self.db.exec(paginated_statement)
        items = result.all()

        return PaginatedResponse(
            total=total,
            page=pagination_params.page,
            per_page=pagination_params.per_page,
            items=items,
        )

    async def count_total(self, statement) -> int:
        count_statement = select(func.count()).select_from(statement.subquery())
        count_result = await self.db.exec(count_statement)

        return count_result.scalar_one()

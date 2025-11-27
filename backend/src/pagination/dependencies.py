from typing import Annotated

from fastapi import Depends, Query

from src.pagination.models import PaginationParams


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    per_page: int = Query(
        10, ge=1, le=100, alias="perPage", description="Number of items per page"
    ),
) -> PaginationParams:
    return PaginationParams(per_page=per_page, page=page)


pagination_params_dep = Annotated[PaginationParams, Depends(get_pagination_params)]

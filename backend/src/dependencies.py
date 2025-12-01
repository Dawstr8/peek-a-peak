from typing import Annotated, Optional

from fastapi import Depends, Query

from src.models import SortParams, camel_to_snake


def get_sort_params(
    sort_by: Optional[str] = Query(
        None, alias="sortBy", description="Field to sort by"
    ),
    order: Optional[str] = Query(None, description="Sort order: 'asc' or 'desc'"),
) -> SortParams:
    if sort_by:
        sort_by = camel_to_snake(sort_by)

    return SortParams(sort_by=sort_by, order=order)


sort_params_dep = Annotated[SortParams, Depends(get_sort_params)]

__all__ = ["sort_params_dep"]

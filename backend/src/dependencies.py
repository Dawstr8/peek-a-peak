from typing import Annotated, Optional

from fastapi import Depends, Query

from src.models import SortParams


def get_sort_params(
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order: 'asc' or 'desc'"),
) -> SortParams:
    return SortParams(sort_by=sort_by, order=order)


sort_params_dep = Annotated[SortParams, Depends(get_sort_params)]

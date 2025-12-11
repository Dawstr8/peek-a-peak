from typing import Type

from sqlmodel import SQLModel, desc

from src.sorting.models import SortParams


def apply_sorting(statement, model: Type[SQLModel], sort_params: SortParams):
    if not sort_params.sort_by or not hasattr(model, sort_params.sort_by):
        return statement

    column = getattr(model, sort_params.sort_by)
    created_at = model.created_at

    if sort_params.order == "desc":
        column, created_at = desc(column), desc(created_at)

    return statement.order_by(column, created_at)

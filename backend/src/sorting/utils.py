from typing import Type

from sqlmodel import SQLModel, desc

from src.sorting.models import SortParams


def apply_sorting(statement, model: Type[SQLModel], sort_params: SortParams):
    if not sort_params.sort_by or not hasattr(model, sort_params.sort_by):
        return statement

    column = getattr(model, sort_params.sort_by)
    id_column = model.id

    if sort_params.order == "desc":
        column, id_column = desc(column), desc(id_column)

    return statement.order_by(column, id_column)

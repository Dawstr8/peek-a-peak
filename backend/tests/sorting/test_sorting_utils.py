import pytest
from sqlmodel import select

from src.photos.models import SummitPhoto
from src.sorting.models import SortParams
from src.sorting.utils import apply_sorting


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_params",
    [
        (SortParams(sort_by=None, order=None)),
        (SortParams(sort_by="invalid_column", order="asc")),
    ],
)
async def test_apply_sorting_with_invalid_or_missing_params(
    test_db,
    db_photos,
    sort_params: SortParams,
):
    statement = select(SummitPhoto)

    result_statement = apply_sorting(
        statement, model=SummitPhoto, sort_params=sort_params
    )

    photos = (await test_db.exec(result_statement)).all()
    assert len(photos) == len(db_photos)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_params,expected_ids",
    [
        (SortParams(sort_by="captured_at", order=None), [0, 1, 3, 2]),
        (SortParams(sort_by="captured_at", order="asc"), [0, 1, 3, 2]),
        (SortParams(sort_by="captured_at", order="desc"), [2, 3, 1, 0]),
        (SortParams(sort_by="uploaded_at", order=None), [0, 1, 2, 3]),
    ],
)
async def test_apply_sorting_with_valid_params(
    test_db,
    db_photos,
    sort_params: SortParams,
    expected_ids: list[int],
):
    statement = select(SummitPhoto)

    result_statement = apply_sorting(
        statement, model=SummitPhoto, sort_params=sort_params
    )

    photos = (await test_db.exec(result_statement)).all()
    assert photos == [db_photos[i] for i in expected_ids]

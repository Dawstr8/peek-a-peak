import pytest
from sqlmodel import select

from src.pagination.models import PaginationParams
from src.pagination.paginator import Paginator
from src.photos.models import SummitPhoto


@pytest.fixture()
def test_paginator(test_db):
    return Paginator(test_db)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "owner_id_fn,page,per_page,expected_total,expected_ids",
    [
        (lambda user: None, 1, 10, 4, [0, 1, 2, 3]),
        (lambda user: None, 1, 3, 4, [0, 1, 2]),
        (lambda user: None, 1, 1, 4, [0]),
        (lambda user: None, 2, 1, 4, [1]),
        (lambda user: None, 3, 1, 4, [2]),
        (lambda user: user.id, 1, 3, 3, [0, 1, 3]),
    ],
)
async def test_paginate(
    db_photos,
    db_user,
    owner_id_fn,
    page,
    per_page,
    expected_total,
    expected_ids,
    test_paginator,
):
    statement = select(SummitPhoto)
    owner_id = owner_id_fn(db_user)
    if owner_id is not None:
        statement = statement.where(SummitPhoto.owner_id == owner_id)

    pagination_params = PaginationParams(page=page, per_page=per_page)

    paginated_response = await test_paginator.paginate(statement, pagination_params)

    assert paginated_response.total == expected_total
    assert paginated_response.page == page
    assert paginated_response.per_page == per_page
    assert paginated_response.items == [db_photos[i] for i in expected_ids]

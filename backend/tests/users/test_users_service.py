import pytest

from src.models import SortParams
from src.pagination.models import PaginationParams
from src.photos.models import SummitPhotoDate, SummitPhotoLocation
from src.users.models import UserUpdate
from src.users.service import UsersService


@pytest.fixture
def users_service(
    mock_users_repository, mock_photos_repository, mock_peaks_repository
) -> UsersService:
    return UsersService(
        mock_users_repository, mock_photos_repository, mock_peaks_repository
    )


@pytest.mark.asyncio
async def test_update_user(
    users_service,
    mock_users_repository,
    mock_user,
):
    user_id = mock_user.id
    update_data = UserUpdate(is_private=True)

    updated_user = await users_service.update_user(user_id, update_data)

    assert updated_user.is_private is True
    mock_users_repository.update.assert_called_once_with(user_id, update_data)


@pytest.mark.asyncio
async def test_get_photos_by_user(
    users_service,
    mock_photos_repository,
    mock_photos,
    mock_user,
):
    user_id = mock_user.id
    sort_params = SortParams(field="captured_at", direction="desc")
    pagination_params = PaginationParams(page=1, per_page=10)

    result = await users_service.get_photos_by_user(
        user_id,
        sort_params=sort_params,
        pagination_params=pagination_params,
    )

    expected_photos = [photo for photo in mock_photos if photo.owner_id == user_id]
    assert result == expected_photos
    mock_photos_repository.get_by_owner_id.assert_called_once_with(
        user_id,
        sort_params=sort_params,
        pagination_params=pagination_params,
    )


@pytest.mark.asyncio
async def test_get_photos_locations_by_user(
    users_service,
    mock_photos_repository,
    mock_photos,
    mock_user,
):
    user_id = mock_user.id

    result = await users_service.get_photos_locations_by_user(user_id)

    expected_locations = [
        SummitPhotoLocation(id=photo.id, lat=photo.lat, lng=photo.lng, alt=photo.alt)
        for photo in mock_photos
        if photo.owner_id == user_id
    ]
    assert result == expected_locations
    mock_photos_repository.get_locations_by_owner_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_photos_dates_by_user(
    users_service,
    mock_users_repository,
    mock_photos_repository,
    mock_photos,
    mock_user,
):
    user_id = mock_user.id

    result = await users_service.get_photos_dates_by_user(user_id)

    expected_dates = [
        SummitPhotoDate(id=photo.id, captured_at=photo.captured_at)
        for photo in mock_photos
        if photo.owner_id == user_id
    ]
    assert result == expected_dates
    mock_photos_repository.get_dates_by_owner_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_summited_by_user_count(
    users_service, mock_peaks_repository, mock_user
):
    user_id = mock_user.id

    count = await users_service.get_summited_peaks_count_by_user(user_id)

    assert count == 2
    mock_peaks_repository.get_summited_by_user_count.assert_called_once_with(user_id)

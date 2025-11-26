import pytest

from src.users.service import UsersService


@pytest.fixture
def users_service(
    mock_users_repository, mock_photos_repository, mock_peaks_repository
) -> UsersService:
    return UsersService(
        mock_users_repository, mock_photos_repository, mock_peaks_repository
    )


@pytest.mark.asyncio
async def test_get_photos_by_user(
    users_service,
    mock_users_repository,
    mock_photos_repository,
    mock_photos,
    mock_user,
):
    user_id = mock_user.id
    username = mock_user.username

    result = await users_service.get_photos_by_user(username)

    expected_photos = [photo for photo in mock_photos if photo.owner_id == user_id]
    assert result == expected_photos
    mock_users_repository.get_by_username.assert_called_once_with(username)
    mock_photos_repository.get_by_owner_id.assert_called_once_with(
        user_id, sort_params=None
    )


@pytest.mark.asyncio
async def test_get_summited_by_user_count(
    users_service, mock_users_repository, mock_peaks_repository, mock_user
):
    user_id = mock_user.id
    username = mock_user.username

    count = await users_service.get_summited_peaks_count_by_user(username)

    assert count == 2
    mock_users_repository.get_by_username.assert_called_once_with(username)
    mock_peaks_repository.get_summited_by_user_count.assert_called_once_with(user_id)

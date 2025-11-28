from typing import List

from fastapi import APIRouter, HTTPException

from src.auth.dependencies import check_access_by_username_dep
from src.dependencies import sort_params_dep
from src.photos.models import SummitPhotoDate, SummitPhotoLocation, SummitPhotoRead
from src.users.dependencies import users_service_dep

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{username}/photos", response_model=List[SummitPhotoRead])
async def get_photos_by_user(
    service: users_service_dep,
    username: check_access_by_username_dep,
    sort_params: sort_params_dep,
):
    """Get all photos uploaded by a specific user, optionally sorted by a field."""
    try:
        return await service.get_photos_by_user(username, sort_params=sort_params)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user photos: {str(e)}"
        )


@router.get("/{username}/photos/locations", response_model=List[SummitPhotoLocation])
async def get_photo_locations_by_user(
    service: users_service_dep,
    username: check_access_by_username_dep,
):
    """Get all photo locations uploaded by a specific user."""
    try:
        return await service.get_photos_locations_by_user(username)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user photo locations: {str(e)}"
        )


@router.get("/{username}/photos/dates", response_model=List[SummitPhotoDate])
async def get_photo_dates_by_user(
    service: users_service_dep,
    username: check_access_by_username_dep,
):
    """Get all photo captured dates uploaded by a specific user."""
    try:
        return await service.get_photos_dates_by_user(username)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user photo dates: {str(e)}"
        )


@router.get("/{username}/peaks/count", response_model=int)
async def get_summited_peaks_count_by_user(
    service: users_service_dep,
    username: check_access_by_username_dep,
):
    """Get the count of photos uploaded by a specific user."""
    return await service.get_summited_peaks_count_by_user(username)

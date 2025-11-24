from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.auth.dependencies import check_access_by_username_dep, current_user_dep
from src.dependencies import sort_params_dep
from src.photos.dependencies import photos_service_dep
from src.photos.models import SummitPhotoCreate, SummitPhotoRead

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.get("", response_model=List[SummitPhotoRead], tags=["photos"])
async def get_all_photos(
    photos_service: photos_service_dep,
    sort_params: sort_params_dep,
):
    """
    Get all uploaded photos, optionally sorted by a field.

    Args:
        sort_params: Sorting parameters

    Returns:
        List[SummitPhotoRead]: List of all uploaded photos, with peak information, sorted as specified or in default order.
    """
    try:
        return await photos_service.get_all_photos(sort_params=sort_params)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve photos: {str(e)}"
        )


@router.get("/user/{username}", response_model=List[SummitPhotoRead], tags=["photos"])
async def get_user_photos(
    photos_service: photos_service_dep,
    username: check_access_by_username_dep,
    sort_params: sort_params_dep,
):
    """
    Get all photos uploaded by the current user.

    Args:
        username: Username of the user whose photos to retrieve
        sort_params: Sorting parameters

    Returns:
        List[SummitPhotoRead]: List of photos uploaded by the current user, with peak information, sorted as specified or in default order.
    """
    try:
        return await photos_service.get_photos_by_user(
            username, sort_params=sort_params
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user photos: {str(e)}"
        )


@router.post("", response_model=SummitPhotoRead, tags=["photos"])
async def upload_photo(
    photos_service: photos_service_dep,
    current_user: current_user_dep,
    file: UploadFile = File(...),
    summit_photo_create: str = Form(...),
):
    """
    Upload a photo file with metadata

    Args:
        file: The photo file to upload
        summit_photo_create: Metadata for the photo (captured_at, lat, lng, alt, peak_id)

    Returns:
        SummitPhotoRead: The uploaded photo object with peak information
    """
    summit_photo_create = SummitPhotoCreate.model_validate_json(summit_photo_create)

    try:
        return await photos_service.upload_photo(
            file, summit_photo_create, current_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photo: {str(e)}")


@router.get("/{photo_id}", response_model=SummitPhotoRead, tags=["photos"])
async def get_photo_by_id(
    photo_id: int,
    photos_service: photos_service_dep,
):
    """
    Get a specific photo by ID

    Args:
        photo_id: ID of the photo to retrieve

    Returns:
        SummitPhotoRead: The requested photo object with peak information
    """
    photo = await photos_service.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


@router.delete("/{photo_id}", response_model=dict, tags=["photos"])
async def delete_photo(
    photo_id: int,
    photos_service: photos_service_dep,
):
    """
    Delete an uploaded photo by ID

    Args:
        photo_id: ID of the photo to delete

    Returns:
        dict: Success status of the operation
    """
    success = await photos_service.delete_photo(photo_id)

    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True}

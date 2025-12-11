from fastapi import APIRouter, HTTPException, Query

from src.common.exceptions import NotFoundException
from src.peaks.dependencies import peaks_service_dep
from src.peaks.models import ReadPeak, ReadPeakWithDistance
from src.sorting.dependencies import sort_params_dep

router = APIRouter(prefix="/api/peaks", tags=["peaks"])
from uuid import UUID


@router.get("", response_model=list[ReadPeak])
async def get_peaks(service: peaks_service_dep):
    """
    Retrieve all peaks.
    """
    return await service.get_all()


@router.get("/count", response_model=int)
async def get_peaks_count(service: peaks_service_dep):
    """
    Retrieve the total count of peaks.
    """
    return await service.get_count()


@router.get("/search", response_model=list[ReadPeak])
async def search_peaks(
    service: peaks_service_dep,
    sort_params: sort_params_dep,
    name_filter: str | None = Query(None, alias="nameFilter"),
    limit: int = 5,
):
    """
    Search peaks with optional filters and ordering.
    """
    return await service.search_peaks(
        name_filter=name_filter, limit=limit, sort_params=sort_params
    )


@router.get("/nearby", response_model=list[ReadPeakWithDistance])
async def find_nearby_peaks(
    service: peaks_service_dep,
    lat: float,
    lng: float,
    max_distance: float | None = Query(None, alias="maxDistance"),
    name_filter: str | None = Query(None, alias="nameFilter"),
    limit: int = 5,
):
    """
    Find peaks near a given location.

    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        max_distance: Maximum distance in meters (optional)
        name_filter: Optional substring to filter peak names (case-insensitive)
        limit: Maximum number of peaks to return (default: 5)

    Returns:
        List of nearest peaks with distances in meters
    """
    return await service.find_nearby_peaks(
        lat=lat,
        lng=lng,
        max_distance=max_distance,
        name_filter=name_filter,
        limit=limit,
    )


@router.get("/{peak_id}", response_model=ReadPeak)
async def get_peak(peak_id: UUID, service: peaks_service_dep):
    """
    Get a specific peak by ID.
    """
    try:
        return await service.get_by_id(peak_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

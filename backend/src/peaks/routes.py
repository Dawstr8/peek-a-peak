from fastapi import APIRouter, HTTPException, Query

from src.exceptions import NotFoundException
from src.peaks.dependencies import peaks_service_dep
from src.peaks.models import ReadPeak, ReadPeakWithDistance

router = APIRouter(
    prefix="/api/peaks",
    tags=["peaks"],
)


@router.get("", response_model=list[ReadPeak], tags=["peaks"])
async def get_peaks(service: peaks_service_dep):
    """
    Retrieve all peaks.
    """
    return await service.get_all()


@router.get("/count", response_model=int, tags=["peaks"])
async def get_peaks_count(service: peaks_service_dep):
    """
    Retrieve the total count of peaks.
    """
    return await service.get_count()


@router.get("/find", response_model=list[ReadPeakWithDistance], tags=["peaks"])
async def find_nearest_peaks(
    service: peaks_service_dep,
    lat: float,
    lng: float,
    max_distance: float | None = Query(None, alias="maxDistance"),
    name_filter: str | None = Query(None, alias="nameFilter"),
    limit: int = 5,
):
    """
    Find the nearest peaks to a given lat and lng.

    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        max_distance: Maximum distance in meters (optional)
        name_filter: Optional substring to filter peak names (case-insensitive)
        limit: Maximum number of peaks to return (default: 5)

    Returns:
        List of nearest peaks with distances in meters
    """
    return await service.find_nearest_peaks(
        lat=lat,
        lng=lng,
        max_distance=max_distance,
        name_filter=name_filter,
        limit=limit,
    )


@router.get("/{peak_id}", response_model=ReadPeak, tags=["peaks"])
async def get_peak(peak_id: int, service: peaks_service_dep):
    """
    Get a specific peak by ID.
    """
    try:
        return await service.get_by_id(peak_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

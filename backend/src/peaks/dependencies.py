from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.repository import PeaksRepository
from src.peaks.service import PeaksService


def get_repository(db: db_dep) -> PeaksRepository:
    return PeaksRepository(db)


peaks_repository_dep = Annotated[PeaksRepository, Depends(get_repository)]


def get_service(repository: peaks_repository_dep) -> PeaksService:
    return PeaksService(repository)


peaks_service_dep = Annotated[PeaksService, Depends(get_service)]


__all__ = ["peaks_repository_dep", "peaks_service_dep"]

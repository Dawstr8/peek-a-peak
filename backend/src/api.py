from fastapi import FastAPI

from src.auth.routes import router as auth_router
from src.peaks.routes import router as peaks_router
from src.photos.routes import router as photos_router
from src.users.routes import router as users_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(peaks_router)
    app.include_router(photos_router)
    app.include_router(users_router)

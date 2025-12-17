from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from src.api import register_routes

app = FastAPI(
    title="Peek-a-Peak API",
    description="API for managing Polish mountain summit photos and achievements",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=(settings.allowed_hosts))

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

if settings.storage_type == "local":
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

register_routes(app)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Peek-a-Peak API",
    }

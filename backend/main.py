from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import register_routes
from src.database.core import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully")
    yield
    pass


app = FastAPI(
    title="Peek-a-Peak API",
    description="API for managing Polish mountain summit photos and achievements",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

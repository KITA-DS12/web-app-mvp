from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logger
from app.api.v1 import posts
from app.db.repository import post_repository

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await post_repository.connect()
    await post_repository.init_db()
    logger.info("Application startup complete")
    yield
    await post_repository.disconnect()
    logger.info("Application shutdown complete")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router, prefix=settings.API_PREFIX)

if os.path.exists("/public"):
    app.mount("/", StaticFiles(directory="/public", html=True), name="static")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
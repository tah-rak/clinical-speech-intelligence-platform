"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, entities, evaluation, health, soap, transcription, uploads, visits
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.models.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.DEBUG)
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Clinical Speech Intelligence Platform API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(uploads.router, prefix=settings.API_PREFIX)
app.include_router(transcription.router, prefix=settings.API_PREFIX)
app.include_router(entities.router, prefix=settings.API_PREFIX)
app.include_router(soap.router, prefix=settings.API_PREFIX)
app.include_router(visits.router, prefix=settings.API_PREFIX)
app.include_router(analytics.router, prefix=settings.API_PREFIX)
app.include_router(evaluation.router, prefix=settings.API_PREFIX)

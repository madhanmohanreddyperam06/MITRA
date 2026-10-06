"""API router for health check endpoints."""
from fastapi import APIRouter
from app.core.logging import logger

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns the current status of the API service.
    """
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "MITRA"
    }


@router.get("/")
async def root():
    """
    Root endpoint.

    Returns a welcome message.
    """
    logger.debug("Root endpoint requested")
    return {"message": "Smart College Helpdesk Bot API is running!"}

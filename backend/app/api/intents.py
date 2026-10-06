"""API router for intent-related endpoints."""
from fastapi import APIRouter
from app.core.logging import logger

router = APIRouter()


@router.get("/intents")
async def get_available_intents():
    """
    Get list of available intents.

    Returns all supported intent categories for the NLP pipeline.
    """
    logger.debug("Available intents requested")
    return {
        "intents": [
            "admission_info",
            "course_info",
            "fee_inquiry",
            "hostel_info",
            "library_info",
            "placement_info",
            "contact_info",
            "general_info",
        ]
    }

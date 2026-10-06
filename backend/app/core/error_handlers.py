"""Global error handlers for FastAPI application."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import MITRAError, DatabaseError, KnowledgeNotFoundError, InvalidQueryError, NLPProcessingError, ConfigurationError
from app.core.logging import logger


async def mitra_error_handler(request: Request, exc: MITRAError) -> JSONResponse:
    """Handle MITRA base exceptions."""
    logger.error(f"MITRA error: {exc.__class__.__name__} - {str(exc)}")

    error_code = "INTERNAL_ERROR"
    if isinstance(exc, DatabaseError):
        error_code = "DATABASE_ERROR"
    elif isinstance(exc, KnowledgeNotFoundError):
        error_code = "KNOWLEDGE_NOT_FOUND"
    elif isinstance(exc, InvalidQueryError):
        error_code = "INVALID_QUERY"
    elif isinstance(exc, NLPProcessingError):
        error_code = "NLP_ERROR"
    elif isinstance(exc, ConfigurationError):
        error_code = "CONFIGURATION_ERROR"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": str(exc) if str(exc) else "An error occurred processing your request."
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc.__class__.__name__} - {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later."
            }
        }
    )

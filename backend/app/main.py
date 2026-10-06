"""Main FastAPI application with refactored architecture."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import MITRAError
from app.core.error_handlers import mitra_error_handler, generic_exception_handler
from app.api.chat import router as chat_router
from app.api.knowledge import router as knowledge_router
from app.api.health import router as health_router
from app.api.intents import router as intents_router
from app.api.auth import router as auth_router
from app.database.connection import init_db

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with timing information."""
    start_time = time.time()

    # Log request
    logger.info(f"{request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate and log response time
    process_time = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} -> {process_time:.0f}ms")

    return response

# Register exception handlers
app.add_exception_handler(MITRAError, mitra_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(knowledge_router, tags=["Knowledge"])
app.include_router(intents_router, tags=["Intents"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    init_db()
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Application shutdown")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

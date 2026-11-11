"""
AgriSense AI - Core FastAPI Application Entrypoint.
Coordinates modules across team members:
- Crop Recommendation (Sujay)
- Crop Yield Prediction (Chetan)
- Fertilizer Recommendation (Avinash)
- Platform & Authentication (Dhyan)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging_config import logger
from backend.app.db.session import check_db_connection
from backend.app.api.fertilizer import router as fertilizer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for application startup and shutdown."""
    logger.info("Initializing AgriSense AI Backend Services...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Check shared database status
    db_ok = check_db_connection()
    if db_ok:
        logger.info("PostgreSQL database connection: ONLINE")
    else:
        logger.info("PostgreSQL database connection: OFFLINE / STANDALONE MODE (normal for local module dev)")
        
    logger.info("Fertilizer Recommendation Module: ACTIVE (Version: %s)", settings.FERTILIZER_MODEL_VERSION)
    yield
    logger.info("Shutting down AgriSense AI Backend Services...")


app = FastAPI(
    title="AgriSense AI – Agricultural Prediction & Decision Support System",
    description=(
        "Full-stack AI platform providing Crop Recommendation, Crop Yield Prediction, "
        "and Fertilizer Recommendation for precision agriculture."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler for safe error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An internal server error occurred. Please contact system administrator.",
            "detail": str(exc) if settings.ENVIRONMENT == "development" else "Internal server error",
        },
    )


# System Health Endpoints
@app.get("/", tags=["System"])
def root():
    return {
        "project": "AgriSense AI",
        "description": "Intelligent Agricultural Prediction and Decision Support System",
        "version": "1.0.0",
        "documentation": "/docs",
    }


@app.get("/api/health", tags=["System"])
def health_check():
    db_status = "connected" if check_db_connection() else "disconnected"
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "modules": {
            "fertilizer_recommendation": "ready",
            "crop_recommendation": "coordinated_sujay",
            "crop_yield_prediction": "coordinated_chetan",
            "platform_auth": "coordinated_dhyan",
        },
    }


# Include Fertilizer Recommendation Router
app.include_router(fertilizer_router, prefix="/api")

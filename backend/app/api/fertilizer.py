"""
FastAPI route definitions for the Fertilizer Recommendation module.
Provides:
- POST /api/predict/fertilizer (Main inference endpoint)
- GET  /api/predict/fertilizer/health (Module readiness check)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.logging_config import logger
from backend.app.db.session import get_db
from backend.app.schemas.fertilizer import (
    FertilizerPredictionRequest,
    FertilizerPredictionResponse,
    FertilizerHealthResponse,
)
from backend.app.services.fertilizer_service import fertilizer_service

router = APIRouter(prefix="/predict/fertilizer", tags=["Fertilizer Recommendation"])


@router.get(
    "/health",
    response_model=FertilizerHealthResponse,
    summary="Check Fertilizer Recommendation Module Health",
)
def get_fertilizer_health():
    """Returns the operational status of the Fertilizer ML pipeline."""
    return fertilizer_service.get_health_status()


@router.post(
    "",
    response_model=FertilizerPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Fertilizer Recommendation",
    description="Predicts the optimal fertilizer category given soil chemical indices and climate parameters.",
)
def predict_fertilizer(
    payload: FertilizerPredictionRequest,
    authorization: str | None = Header(default=None),
    db: Session | None = Depends(get_db),
):
    """
    Inference endpoint for fertilizer prediction.
    - Validates inputs using Pydantic.
    - Runs preprocessing and trained classification pipeline.
    - Attaches standard agricultural safety disclaimer.
    - Integrates with Dhyan's authentication and database history if present.
    """
    logger.info(
        f"Prediction request received: soil_type={payload.soil_type}, crop_type={payload.crop_type}, "
        f"N={payload.nitrogen}, P={payload.phosphorous}, K={payload.potassium}"
    )

    # Optional extraction of authenticated user identity from Authorization header
    user_id = None
    if authorization and authorization.startswith("Bearer "):
        # Placeholder integration with Dhyan's JWT auth provider
        user_id = "authenticated_user"

    try:
        result = fertilizer_service.predict(payload.model_dump())
    except FileNotFoundError as fnf:
        logger.error(f"Model artifact not found: {fnf}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Fertilizer prediction model artifact is not loaded or training is pending. "
                "Please run model training pipeline."
            ),
        )
    except ValueError as ve:
        logger.warning(f"Validation / inference error: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Inference execution failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the fertilizer recommendation.",
        )

    response = FertilizerPredictionResponse(
        prediction_type="fertilizer_recommendation",
        prediction=result["prediction"],
        model_version=settings.FERTILIZER_MODEL_VERSION,
        input_summary=payload.model_dump(),
        user_id=user_id,
    )

    # If database is connected and Dhyan's history model is defined, record can be saved here
    if db is not None:
        try:
            logger.debug("Database session available for recording prediction history.")
        except Exception as dbe:
            logger.warning(f"History persistence skipped: {dbe}")

    return response

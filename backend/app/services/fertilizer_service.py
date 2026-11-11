"""
Backend service adapter for Fertilizer Inference.
Encapsulates ML pipeline calls and health status reporting.
"""

from typing import Any
from backend.app.core.logging_config import logger
from backend.app.core.config import settings

# Attempt import of ml inference engine
try:
    from ml.inference.fertilizer_service import FertilizerInferenceService
    _inference_engine = FertilizerInferenceService()
except Exception as e:
    logger.warning(f"Inference engine deferred initialization: {e}")
    _inference_engine = None


class FertilizerService:
    """Service layer coordinating requests with ML inference engine."""

    def __init__(self):
        self.engine = _inference_engine

    def get_health_status(self) -> dict[str, Any]:
        """Queries inference engine status and supported feature labels."""
        if self.engine is None:
            try:
                from ml.inference.fertilizer_service import FertilizerInferenceService
                self.engine = FertilizerInferenceService()
            except Exception as e:
                return {
                    "module": "fertilizer_recommendation",
                    "status": "degraded",
                    "model_loaded": False,
                    "model_version": settings.FERTILIZER_MODEL_VERSION,
                    "supported_soil_types": [],
                    "supported_crop_types": [],
                    "supported_fertilizers": [],
                }

        is_loaded = self.engine.is_model_loaded()
        metadata = self.engine.get_metadata() if is_loaded else {}
        
        return {
            "module": "fertilizer_recommendation",
            "status": "operational" if is_loaded else "model_not_trained",
            "model_loaded": is_loaded,
            "model_version": settings.FERTILIZER_MODEL_VERSION,
            "supported_soil_types": metadata.get("supported_soil_types", []),
            "supported_crop_types": metadata.get("supported_crop_types", []),
            "supported_fertilizers": metadata.get("supported_fertilizers", []),
        }

    def predict(self, feature_data: dict[str, Any]) -> dict[str, Any]:
        """Delegates feature dictionary to inference engine."""
        if self.engine is None or not self.engine.is_model_loaded():
            try:
                from ml.inference.fertilizer_service import FertilizerInferenceService
                self.engine = FertilizerInferenceService()
            except Exception as e:
                raise FileNotFoundError(f"Model engine initialization failed: {e}")

        return self.engine.predict(feature_data)


fertilizer_service = FertilizerService()

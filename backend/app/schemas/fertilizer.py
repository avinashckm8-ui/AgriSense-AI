"""
Pydantic schemas for the Fertilizer Recommendation module.
Defines strict validation for incoming prediction requests and responses.
All field names strictly adhere to snake_case.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, field_validator


class FertilizerPredictionRequest(BaseModel):
    """
    Input features for fertilizer recommendation derived from soil and climate indicators.
    Features:
    - Temperature (°C)
    - Humidity (%)
    - Moisture (%)
    - Soil Type (Categorical)
    - Crop Type (Categorical)
    - Nitrogen (N) content
    - Potassium (K) content
    - Phosphorous (P) content
    """
    temperature: float = Field(..., ge=-10.0, le=60.0, description="Ambient air temperature in Celsius", example=26.0)
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative air humidity percentage", example=52.0)
    moisture: float = Field(..., ge=0.0, le=100.0, description="Soil moisture percentage", example=38.0)
    soil_type: str = Field(..., min_length=2, max_length=50, description="Soil classification category", example="Sandy")
    crop_type: str = Field(..., min_length=2, max_length=50, description="Planted crop category", example="Maize")
    nitrogen: float = Field(..., ge=0.0, le=300.0, description="Soil Nitrogen (N) ratio / ppm", example=37.0)
    potassium: float = Field(..., ge=0.0, le=300.0, description="Soil Potassium (K) ratio / ppm", example=0.0)
    phosphorous: float = Field(..., ge=0.0, le=300.0, description="Soil Phosphorous (P) ratio / ppm", example=0.0)

    @field_validator("soil_type", "crop_type")
    @classmethod
    def strip_and_capitalize(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Field cannot be empty or whitespace.")
        return clean


class FertilizerPredictionResponse(BaseModel):
    """Structured response conforming to AgriSense AI team integration standards."""
    
    prediction_type: str = Field(default="fertilizer_recommendation")
    prediction: str = Field(..., description="Recommended fertilizer category (e.g., Urea, DAP, 14-35-14)")
    model_version: str = Field(..., description="Semantic version of the trained ML pipeline")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    input_summary: dict[str, Any] = Field(..., description="Echo of normalized input parameters")
    disclaimer: str = Field(
        default=(
            "CAUTION: This recommendation is an AI-assisted decision support guideline based on machine learning "
            "classification. Always verify fertilizer application decisions with professional soil-test laboratory "
            "results and local agricultural extension authorities before field application. Do not use as a dosage directive."
        )
    )
    user_id: str | None = Field(default=None, description="Authenticated user identifier if session is present")


class FertilizerHealthResponse(BaseModel):
    """Health check status for fertilizer inference service."""
    
    module: str = "fertilizer_recommendation"
    status: str
    model_loaded: bool
    model_version: str
    supported_soil_types: list[str] = []
    supported_crop_types: list[str] = []
    supported_fertilizers: list[str] = []

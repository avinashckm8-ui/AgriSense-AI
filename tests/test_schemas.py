"""
Unit tests for Pydantic schema validation in Fertilizer Recommendation module.
"""

import pytest
from pydantic import ValidationError
from backend.app.schemas.fertilizer import (
    FertilizerPredictionRequest,
    FertilizerPredictionResponse,
    FertilizerHealthResponse,
)


def test_valid_fertilizer_request():
    """Verify that valid agricultural input features pass validation."""
    payload = {
        "temperature": 26.0,
        "humidity": 52.0,
        "moisture": 38.0,
        "soil_type": "Sandy",
        "crop_type": "Maize",
        "nitrogen": 37.0,
        "potassium": 0.0,
        "phosphorous": 0.0,
    }
    req = FertilizerPredictionRequest(**payload)
    assert req.soil_type == "Sandy"
    assert req.crop_type == "Maize"
    assert req.temperature == 26.0
    assert req.nitrogen == 37.0


def test_invalid_temperature_out_of_range():
    """Verify that unrealistic temperatures (> 60C or < -10C) fail validation."""
    payload = {
        "temperature": 150.0,  # Unrealistic ambient temperature
        "humidity": 50.0,
        "moisture": 40.0,
        "soil_type": "Loamy",
        "crop_type": "Wheat",
        "nitrogen": 40.0,
        "potassium": 20.0,
        "phosphorous": 30.0,
    }
    with pytest.raises(ValidationError) as exc_info:
        FertilizerPredictionRequest(**payload)
    assert "temperature" in str(exc_info.value)


def test_invalid_negative_nutrients():
    """Verify that negative nutrient concentrations fail validation."""
    payload = {
        "temperature": 25.0,
        "humidity": 50.0,
        "moisture": 40.0,
        "soil_type": "Loamy",
        "crop_type": "Wheat",
        "nitrogen": -10.0,  # Negative nutrient
        "potassium": 20.0,
        "phosphorous": 30.0,
    }
    with pytest.raises(ValidationError) as exc_info:
        FertilizerPredictionRequest(**payload)
    assert "nitrogen" in str(exc_info.value)


def test_empty_string_categories():
    """Verify that empty or whitespace-only soil/crop names are rejected."""
    payload = {
        "temperature": 25.0,
        "humidity": 50.0,
        "moisture": 40.0,
        "soil_type": "   ",  # Blank
        "crop_type": "Wheat",
        "nitrogen": 40.0,
        "potassium": 20.0,
        "phosphorous": 30.0,
    }
    with pytest.raises(ValidationError):
        FertilizerPredictionRequest(**payload)


def test_fertilizer_prediction_response_schema():
    """Verify response model formatting and agricultural caution presence."""
    resp = FertilizerPredictionResponse(
        prediction="Urea",
        model_version="1.0.0",
        input_summary={"temperature": 26.0, "soil_type": "Sandy"},
    )
    assert resp.prediction == "Urea"
    assert resp.prediction_type == "fertilizer_recommendation"
    assert "CAUTION" in resp.disclaimer
    assert resp.created_at.endswith("Z")

"""
Automated unit tests for Fertilizer ML Pipeline and Inference Service.
"""

import pytest
from ml.inference.fertilizer_service import FertilizerInferenceService


def test_inference_service_model_loaded():
    """Verify that the champion model pipeline artifact loads successfully."""
    service = FertilizerInferenceService()
    assert service.is_model_loaded() is True
    metadata = service.get_metadata()
    assert metadata["model_name"] == "DecisionTreeClassifier"
    assert metadata["model_version"] == "1.0.0"
    assert "Urea" in metadata["supported_fertilizers"]


def test_inference_service_prediction():
    """Verify prediction output for known soil/crop condition."""
    service = FertilizerInferenceService()
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
    result = service.predict(payload)
    assert result["prediction"] == "Urea"
    assert result["model_name"] == "DecisionTreeClassifier"
    assert result["model_version"] == "1.0.0"


def test_inference_service_missing_feature():
    """Verify that missing input features trigger a descriptive ValueError."""
    service = FertilizerInferenceService()
    incomplete_payload = {
        "temperature": 26.0,
        "humidity": 52.0,
        # Missing moisture, N, P, K, etc.
    }
    with pytest.raises(ValueError) as exc:
        service.predict(incomplete_payload)
    assert "Missing required feature" in str(exc.value)

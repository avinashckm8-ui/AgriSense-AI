"""
Inference engine for Fertilizer Recommendation Module.
Handles model artifact loading, input feature alignment, and prediction.
"""

import sys
from pathlib import Path
from typing import Any
import pandas as pd
import joblib

# Ensure ml package is in sys.path and models are available for joblib unpickling
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
import ml.training.models  # noqa: F401

from backend.app.core.logging_config import logger


class FertilizerInferenceService:
    """Manages prediction pipeline loading and inference execution."""

    def __init__(self, artifacts_dir: Path | str | None = None):
        if artifacts_dir is None:
            self.artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
        else:
            self.artifacts_dir = Path(artifacts_dir)

        self.pipeline_path = self.artifacts_dir / "fertilizer_pipeline.joblib"
        self.metadata_path = self.artifacts_dir / "model_metadata.joblib"

        self._pipeline = None
        self._metadata = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Loads serialized pipeline and metadata if available."""
        if self.pipeline_path.exists() and self.metadata_path.exists():
            try:
                self._pipeline = joblib.load(self.pipeline_path)
                self._metadata = joblib.load(self.metadata_path)
                logger.info(
                    f"Fertilizer model pipeline successfully loaded: {self.pipeline_path} "
                    f"(Algorithm: {self._metadata.get('model_name')}, Version: {self._metadata.get('model_version')})"
                )
            except Exception as e:
                logger.error(f"Failed to load fertilizer pipeline artifacts: {e}", exc_info=True)
                self._pipeline = None
                self._metadata = None
        else:
            logger.info(
                f"Fertilizer pipeline artifacts not found at {self.pipeline_path}. "
                "Inference will be unavailable until model training is executed."
            )

    def is_model_loaded(self) -> bool:
        """Checks if pipeline and metadata are actively loaded."""
        return self._pipeline is not None and self._metadata is not None

    def get_metadata(self) -> dict[str, Any]:
        """Returns loaded model metadata or empty dict."""
        return self._metadata if self._metadata is not None else {}

    def predict(self, feature_data: dict[str, Any]) -> dict[str, Any]:
        """
        Executes prediction on incoming feature dictionary.
        Maps snake_case keys to training feature names.
        """
        if not self.is_model_loaded():
            self._load_artifacts()
            if not self.is_model_loaded():
                raise FileNotFoundError(
                    f"Model pipeline artifact not found at {self.pipeline_path}. "
                    "Please run the model training pipeline first."
                )

        feature_mapping = {
            "temperature": "Temparature",
            "humidity": "Humidity",
            "moisture": "Moisture",
            "soil_type": "Soil Type",
            "crop_type": "Crop Type",
            "nitrogen": "Nitrogen",
            "potassium": "Potassium",
            "phosphorous": "Phosphorous",
        }

        # Normalize and map incoming input
        row = {}
        for key, target_col in feature_mapping.items():
            if key not in feature_data:
                raise ValueError(f"Missing required feature: '{key}'")
            val = feature_data[key]
            if isinstance(val, str):
                val = val.strip()
            row[target_col] = val

        expected_columns = self._metadata.get(
            "feature_names",
            ["Temparature", "Humidity", "Moisture", "Soil Type", "Crop Type", "Nitrogen", "Potassium", "Phosphorous"]
        )

        input_df = pd.DataFrame([row], columns=expected_columns)

        try:
            prediction_label = self._pipeline.predict(input_df)[0]
        except Exception as e:
            logger.error(f"Pipeline prediction error: {e}", exc_info=True)
            raise ValueError(f"Model prediction failed on input features: {e}")

        return {
            "prediction": str(prediction_label),
            "model_name": self._metadata.get("model_name", "Classification Pipeline"),
            "model_version": self._metadata.get("model_version", "1.0.0"),
        }

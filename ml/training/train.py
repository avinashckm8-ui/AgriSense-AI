"""
Machine Learning Training & Benchmark Pipeline for Fertilizer Recommendation.
Trains baseline (DummyClassifier), DecisionTree, RandomForest, and LogisticRegression.
Selects best model using Macro F1-score and exports complete fitted pipeline via Joblib.
"""

from datetime import datetime, timezone
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import joblib
import numpy as np
import pandas as pd

from ml.training.models import (
    ColumnTransformer,
    DecisionTreeClassifier,
    DummyClassifier,
    FertilizerPipeline,
    LogisticRegression,
    RandomForestClassifier,
    compute_metrics,
)
DATA_RAW_PATH = BASE_DIR / "data" / "raw" / "Fertilizer Prediction.csv"
DATA_PROCESSED_PATH = BASE_DIR / "data" / "processed" / "fertilizer_processed.csv"
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
DOCS_DIR = BASE_DIR / "docs"


def load_and_validate_raw_data() -> pd.DataFrame:
    """Loads raw dataset from data/raw/ and validates required schema."""
    if not DATA_RAW_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found at '{DATA_RAW_PATH}'.")

    df = pd.read_csv(DATA_RAW_PATH)
    print(f"[DATA] Successfully loaded raw dataset with shape: {df.shape}")

    # Strip column names (e.g. 'Humidity ' -> 'Humidity')
    df.columns = [c.strip() for c in df.columns]

    expected_cols = [
        "Temparature", "Humidity", "Moisture", "Soil Type",
        "Crop Type", "Nitrogen", "Potassium", "Phosphorous", "Fertilizer Name"
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # Strip categories
    df["Soil Type"] = df["Soil Type"].astype(str).str.strip()
    df["Crop Type"] = df["Crop Type"].astype(str).str.strip()
    df["Fertilizer Name"] = df["Fertilizer Name"].astype(str).str.strip()

    null_count = df.isnull().sum().sum()
    duplicate_count = df.duplicated().sum()
    print(f"[DATA QUALITY] Null values: {null_count} | Duplicate records: {duplicate_count}")

    return df


def run_training_pipeline():
    """Executes end-to-end data processing, model benchmarking, and artifact export."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_and_validate_raw_data()

    # Save cleaned processed dataset
    df.to_csv(DATA_PROCESSED_PATH, index=False)
    print(f"[DATA] Saved processed dataset to: {DATA_PROCESSED_PATH}")

    target_col = "Fertilizer Name"
    X = df.drop(columns=[target_col])
    y = df[target_col].values

    num_cols = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]
    cat_cols = ["Soil Type", "Crop Type"]

    # Reproducible 80/20 train/test split with stratification by class
    rng = np.random.RandomState(42)
    train_indices = []
    test_indices = []

    for cls in np.unique(y):
        cls_indices = np.where(y == cls)[0]
        rng.shuffle(cls_indices)
        split_point = int(len(cls_indices) * 0.8)
        # Ensure at least 1 test sample per class
        if split_point == len(cls_indices):
            split_point = len(cls_indices) - 1
        train_indices.extend(cls_indices[:split_point])
        test_indices.extend(cls_indices[split_point:])

    X_train, y_train = X.iloc[train_indices].reset_index(drop=True), y[train_indices]
    X_test, y_test = X.iloc[test_indices].reset_index(drop=True), y[test_indices]
    print(f"[SPLIT] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    # Candidate algorithms to benchmark
    candidate_algorithms = {
        "DummyClassifier (Baseline)": DummyClassifier(),
        "LogisticRegression": LogisticRegression(lr=0.08, n_iters=800, reg=0.01, random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=8, min_samples_split=2, random_state=42),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=35, max_depth=8, min_samples_split=2, random_state=42),
    }

    results = {}
    fitted_pipelines = {}

    print("\n" + "=" * 70)
    print("MODEL BENCHMARKING & EVALUATION (Macro Metrics for Class Imbalance)")
    print("=" * 70)

    for name, clf in candidate_algorithms.items():
        preprocessor = ColumnTransformer(num_cols, cat_cols)
        pipeline = FertilizerPipeline(preprocessor=preprocessor, model=clf)
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        metrics = compute_metrics(y_test, y_pred)
        results[name] = metrics
        fitted_pipelines[name] = pipeline

        print(f"\nModel: {name}")
        print(f"  Test Accuracy:         {metrics['accuracy']:.4f}")
        print(f"  Macro Precision:       {metrics['macro_precision']:.4f}")
        print(f"  Macro Recall:          {metrics['macro_recall']:.4f}")
        print(f"  Macro F1-Score:        {metrics['macro_f1']:.4f}")

    # Select champion based on Macro F1
    non_baseline = {k: v for k, v in results.items() if "Dummy" not in k}
    best_name = max(non_baseline, key=lambda k: (non_baseline[k]["macro_f1"], non_baseline[k]["accuracy"]))
    best_pipeline = fitted_pipelines[best_name]
    best_metrics = results[best_name]

    print("\n" + "=" * 70)
    print(f"CHAMPION MODEL SELECTED: {best_name}")
    print(f"Accuracy: {best_metrics['accuracy'] * 100:.2f}% | Macro F1: {best_metrics['macro_f1'] * 100:.2f}%")
    print("=" * 70)

    # Save Pipeline and Metadata
    pipeline_export_path = ARTIFACTS_DIR / "fertilizer_pipeline.joblib"
    joblib.dump(best_pipeline, pipeline_export_path)
    print(f"[ARTIFACTS] Exported champion pipeline to: {pipeline_export_path}")

    unique_fertilizers = sorted(list(df["Fertilizer Name"].unique()))
    unique_soils = sorted(list(df["Soil Type"].unique()))
    unique_crops = sorted(list(df["Crop Type"].unique()))

    metadata = {
        "model_name": best_name,
        "model_version": "1.0.0",
        "training_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dataset_source": "Fertilizer Prediction Dataset (Kaggle / Indian Soil & Crop Testing Laboratories)",
        "dataset_rows": len(df),
        "feature_names": ["Temparature", "Humidity", "Moisture", "Soil Type", "Crop Type", "Nitrogen", "Potassium", "Phosphorous"],
        "target_label": target_col,
        "supported_fertilizers": unique_fertilizers,
        "supported_soil_types": unique_soils,
        "supported_crop_types": unique_crops,
        "champion_metrics": best_metrics,
        "benchmark_comparison": results,
    }

    metadata_export_path = ARTIFACTS_DIR / "model_metadata.joblib"
    joblib.dump(metadata, metadata_export_path)
    print(f"[ARTIFACTS] Exported model metadata to: {metadata_export_path}")

    # Write Model Evaluation Markdown Report
    report_md = f"""# Fertilizer Recommendation Module – Model Evaluation Report

**Generated:** {metadata['training_date']}  
**Selected Champion:** `{best_name}` (Version: `{metadata['model_version']}`)  
**Dataset:** {len(df)} samples ({len(X_train)} Train / {len(X_test)} Test)

---

## 1. Algorithm Benchmarking & Performance Comparison

| Model | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
"""
    for m_name, m_data in results.items():
        report_md += f"| {m_name} | {m_data['accuracy']:.4f} | {m_data['macro_precision']:.4f} | {m_data['macro_recall']:.4f} | **{m_data['macro_f1']:.4f}** |\n"

    report_md += f"""
---

## 2. Champion Model Performance (`{best_name}`)

- **Overall Test Accuracy:** `{best_metrics['accuracy'] * 100:.2f}%`
- **Macro Precision:** `{best_metrics['macro_precision'] * 100:.2f}%`
- **Macro Recall:** `{best_metrics['macro_recall'] * 100:.2f}%`
- **Macro F1-Score:** `{best_metrics['macro_f1'] * 100:.2f}%`

### Confusion Matrix (Test Set)
Classes: {', '.join([f'`{c}`' for c in best_metrics['classes']])}

```text
{json.dumps(best_metrics['confusion_matrix'], indent=2)}
```

### Supported Fertilizer Formulations ({len(unique_fertilizers)})
{', '.join([f'`{f}`' for f in unique_fertilizers])}

### Supported Soil Types ({len(unique_soils)})
{', '.join([f'`{s}`' for s in unique_soils])}

### Supported Crop Types ({len(unique_crops)})
{', '.join([f'`{c}`' for c in unique_crops])}

---

## 3. Operational Deployment
- Pipeline serialized at [`ml/artifacts/fertilizer_pipeline.joblib`](file:///c:/Users/Avinash%20H/Documents/AgriSense-AI/ml/artifacts/fertilizer_pipeline.joblib).
- Metadata saved at [`ml/artifacts/model_metadata.joblib`](file:///c:/Users/Avinash%20H/Documents/AgriSense-AI/ml/artifacts/model_metadata.joblib).
"""
    (DOCS_DIR / "MODEL_EVALUATION.md").write_text(report_md, encoding="utf-8")
    print(f"[DOCUMENTATION] Generated: {DOCS_DIR / 'MODEL_EVALUATION.md'}")


if __name__ == "__main__":
    run_training_pipeline()

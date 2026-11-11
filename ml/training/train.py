"""
Machine Learning Training & Benchmark Pipeline for Fertilizer Recommendation.
Trains baseline (DummyClassifier), DecisionTree, RandomForest, and LogisticRegression.
Selects best model using Macro F1-score and exports complete fitted pipeline via Joblib.
"""

from datetime import datetime
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Workspace directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_RAW_PATH = BASE_DIR / "data" / "raw" / "Fertilizer Prediction.csv"
DATA_PROCESSED_PATH = BASE_DIR / "data" / "processed" / "fertilizer_processed.csv"
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
DOCS_DIR = BASE_DIR / "docs"


def load_and_validate_raw_data() -> pd.DataFrame:
    """Loads raw dataset from data/raw/ and validates required schema."""
    if not DATA_RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at '{DATA_RAW_PATH}'. "
            "Please ensure raw dataset is downloaded before initiating training."
        )

    df = pd.read_csv(DATA_RAW_PATH)
    print(f"[DATA] Successfully loaded raw dataset with shape: {df.shape}")

    # Normalize column names (strip trailing/leading spaces)
    df.columns = [c.strip() for c in df.columns]

    # Verify column presence
    expected_cols = [
        "Temparature", "Humidity", "Moisture", "Soil Type",
        "Crop Type", "Nitrogen", "Potassium", "Phosphorous", "Fertilizer Name"
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing expected columns: {missing}. Found: {list(df.columns)}")

    # Clean string categories
    df["Soil Type"] = df["Soil Type"].astype(str).str.strip()
    df["Crop Type"] = df["Crop Type"].astype(str).str.strip()
    df["Fertilizer Name"] = df["Fertilizer Name"].astype(str).str.strip()

    # Data Quality Audits
    null_count = df.isnull().sum().sum()
    duplicate_count = df.duplicated().sum()
    print(f"[DATA QUALITY] Null values: {null_count} | Duplicate records: {duplicate_count}")

    if null_count > 0:
        print("[DATA CLEANING] Imputing missing values with median for numerical and mode for categorical...")
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
        for col in df.select_dtypes(include=[object]).columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df


def build_preprocessor(numerical_cols: list[str], categorical_cols: list[str]) -> ColumnTransformer:
    """Constructs Scikit-learn ColumnTransformer for scalable encoding and scaling."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
        ],
        remainder="drop",
    )


def run_training_pipeline():
    """Executes end-to-end data processing, model benchmarking, and artifact export."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_and_validate_raw_data()

    # Separate features and target
    target_col = "Fertilizer Name"
    X = df.drop(columns=[target_col])
    y = df[target_col]

    numerical_cols = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]
    categorical_cols = ["Soil Type", "Crop Type"]

    # Save cleaned processed dataset
    df.to_csv(DATA_PROCESSED_PATH, index=False)
    print(f"[DATA] Saved processed dataset to: {DATA_PROCESSED_PATH}")

    # Stratified Train/Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[SPLIT] Training instances: {len(X_train)} | Test instances: {len(X_test)}")

    preprocessor = build_preprocessor(numerical_cols, categorical_cols)

    # Candidate Models to benchmark
    candidate_algorithms = {
        "DummyClassifier (Baseline)": DummyClassifier(strategy="most_frequent"),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(random_state=42, max_depth=8),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    fitted_pipelines = {}

    print("\n" + "=" * 70)
    print("MODEL BENCHMARKING & EVALUATION (Macro Metrics for Class Imbalance)")
    print("=" * 70)

    for name, clf in candidate_algorithms.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", build_preprocessor(numerical_cols, categorical_cols)),
            ("classifier", clf),
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(float(acc), 4),
            "macro_precision": round(float(prec_macro), 4),
            "macro_recall": round(float(rec_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "confusion_matrix": cm,
            "classification_report": classification_report(y_test, y_pred, zero_division=0, output_dict=True),
        }
        fitted_pipelines[name] = pipeline

        print(f"\nModel: {name}")
        print(f"  Accuracy:         {acc:.4f}")
        print(f"  Macro Precision:  {prec_macro:.4f}")
        print(f"  Macro Recall:     {rec_macro:.4f}")
        print(f"  Macro F1-Score:   {f1_macro:.4f}")

    # Select best model based on Macro F1 score
    non_baseline_models = {k: v for k, v in results.items() if "Dummy" not in k}
    best_model_name = max(non_baseline_models, key=lambda k: (non_baseline_models[k]["macro_f1"], non_baseline_models[k]["accuracy"]))
    best_pipeline = fitted_pipelines[best_model_name]
    best_metrics = results[best_model_name]

    print("\n" + "=" * 70)
    print(f"SELECTED CHAMPION MODEL: {best_model_name}")
    print(f"Champion Test Macro F1: {best_metrics['macro_f1']} | Accuracy: {best_metrics['accuracy']}")
    print("=" * 70)

    # Export Champion Pipeline
    pipeline_export_path = ARTIFACTS_DIR / "fertilizer_pipeline.joblib"
    joblib.dump(best_pipeline, pipeline_export_path)
    print(f"[SERIALIZATION] Exported complete fitted pipeline to: {pipeline_export_path}")

    # Extract class labels and metadata
    unique_fertilizers = sorted(list(df["Fertilizer Name"].unique()))
    unique_soils = sorted(list(df["Soil Type"].unique()))
    unique_crops = sorted(list(df["Crop Type"].unique()))

    metadata = {
        "model_name": best_model_name,
        "model_version": "1.0.0",
        "training_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dataset_source": "Fertilizer Prediction Dataset (Kaggle / Indian Agricultural Research Repository)",
        "dataset_rows": len(df),
        "feature_names": list(X.columns),
        "target_label": target_col,
        "supported_fertilizers": unique_fertilizers,
        "supported_soil_types": unique_soils,
        "supported_crop_types": unique_crops,
        "champion_metrics": best_metrics,
        "benchmark_comparison": results,
    }

    metadata_export_path = ARTIFACTS_DIR / "model_metadata.joblib"
    joblib.dump(metadata, metadata_export_path)
    print(f"[SERIALIZATION] Exported model metadata to: {metadata_export_path}")

    # Generate Markdown Evaluation Report
    report_md = f"""# Fertilizer Recommendation Module – Model Evaluation Report

**Generated on:** {metadata['training_date']}  
**Selected Model:** `{best_model_name}` (Version: `{metadata['model_version']}`)  
**Dataset Size:** {len(df)} samples ({len(X_train)} Train / {len(X_test)} Test)

---

## 1. Algorithm Comparison & Benchmark Results

| Model | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
"""
    for m_name, m_data in results.items():
        report_md += f"| {m_name} | {m_data['accuracy']:.4f} | {m_data['macro_precision']:.4f} | {m_data['macro_recall']:.4f} | **{m_data['macro_f1']:.4f}** |\n"

    report_md += f"""
---

## 2. Champion Model Performance (`{best_model_name}`)

- **Overall Test Accuracy:** `{best_metrics['accuracy'] * 100:.2f}%`
- **Macro Precision:** `{best_metrics['macro_precision'] * 100:.2f}%`
- **Macro Recall:** `{best_metrics['macro_recall'] * 100:.2f}%`
- **Macro F1-Score:** `{best_metrics['macro_f1'] * 100:.2f}%`

### Target Label Support ({len(unique_fertilizers)} Fertilizer Formulations)
{', '.join([f'`{f}`' for f in unique_fertilizers])}

### Supported Soil Types ({len(unique_soils)})
{', '.join([f'`{s}`' for s in unique_soils])}

### Supported Crop Types ({len(unique_crops)})
{', '.join([f'`{c}`' for c in unique_crops])}

---

## 3. Operational Deployment
- Pipeline serialized at `ml/artifacts/fertilizer_pipeline.joblib`.
- Metadata saved at `ml/artifacts/model_metadata.joblib`.
"""
    evaluation_doc_path = DOCS_DIR / "MODEL_EVALUATION.md"
    evaluation_doc_path.write_text(report_md, encoding="utf-8")
    print(f"[DOCUMENTATION] Written evaluation report to: {evaluation_doc_path}")


if __name__ == "__main__":
    from sklearn.tree import DecisionTreeClassifier
    run_training_pipeline()

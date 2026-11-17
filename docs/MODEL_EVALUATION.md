# Fertilizer Recommendation Module – Model Evaluation Report

**Generated:** 2026-11-17 08:28:02 UTC  
**Selected Champion:** `DecisionTreeClassifier` (Version: `1.0.0`)  
**Dataset:** 99 samples (76 Train / 23 Test)

---

## 1. Algorithm Benchmarking & Performance Comparison

| Model | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| DummyClassifier (Baseline) | 0.2174 | 0.0311 | 0.1429 | **0.0510** |
| LogisticRegression | 0.8696 | 0.7571 | 0.8214 | **0.7732** |
| DecisionTreeClassifier | 0.9130 | 0.7810 | 0.8571 | **0.8127** |
| RandomForestClassifier | 0.9130 | 0.7810 | 0.8571 | **0.8127** |

---

## 2. Champion Model Performance (`DecisionTreeClassifier`)

- **Overall Test Accuracy:** `91.30%`
- **Macro Precision:** `78.10%`
- **Macro Recall:** `85.71%`
- **Macro F1-Score:** `81.27%`

### Confusion Matrix (Test Set)
Classes: `10-26-26`, `14-35-14`, `17-17-17`, `20-20`, `28-28`, `DAP`, `Urea`

```text
[
  [
    2,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    0,
    1,
    0,
    0
  ],
  [
    0,
    0,
    0,
    3,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    5
  ]
]
```

### Supported Fertilizer Formulations (7)
`10-26-26`, `14-35-14`, `17-17-17`, `20-20`, `28-28`, `DAP`, `Urea`

### Supported Soil Types (5)
`Black`, `Clayey`, `Loamy`, `Red`, `Sandy`

### Supported Crop Types (11)
`Barley`, `Cotton`, `Ground Nuts`, `Maize`, `Millets`, `Oil seeds`, `Paddy`, `Pulses`, `Sugarcane`, `Tobacco`, `Wheat`

---

## 3. Operational Deployment
- Pipeline serialized at [`ml/artifacts/fertilizer_pipeline.joblib`](file:///c:/Users/Avinash%20H/Documents/AgriSense-AI/ml/artifacts/fertilizer_pipeline.joblib).
- Metadata saved at [`ml/artifacts/model_metadata.joblib`](file:///c:/Users/Avinash%20H/Documents/AgriSense-AI/ml/artifacts/model_metadata.joblib).

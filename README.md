# AgriSense AI – Intelligent Agricultural Prediction and Decision Support System

AgriSense AI is a full-stack, AI-powered agricultural decision support platform designed to assist farmers, agronomists, and agricultural extension workers in making data-driven decisions.

## Project Modules & Team Allocation

| Team Member | Module Responsibility | Branch |
| :--- | :--- | :--- |
| **Sujay** | Crop Recommendation Module | `feature/sujay-crop` |
| **Chetan** | Crop Yield Prediction Module | `feature/chetan-yield` |
| **Avinash** | Fertilizer Recommendation Module | `feature/avinash-fertilizer` |
| **Dhyan** | User Auth, Dashboard & Prediction History | `feature/dhyan-auth` |

---

## Fertilizer Recommendation Module (Avinash)

The **Fertilizer Recommendation Module** analyzes environmental conditions and soil nutrient levels to recommend the optimal fertilizer formulation for specific crops, preventing over-fertilization, soil degradation, and unnecessary agricultural expenses.

### Key Features
- **Machine Learning Engine**: Trained on agricultural soil and climatic data using Decision Trees with stratified validation (91.30% Accuracy, 81.27% Macro F1-Score).
- **Supported Formulations**: `Urea`, `DAP`, `14-35-14`, `28-28`, `17-17-17`, `20-20`, and `10-26-26`.
- **FastAPI REST Endpoints**: High-performance endpoints with Pydantic v2 input validation and OpenAPI documentation.
- **Modern React Interface**: Responsive UI built with Tailwind CSS, real-time input validation, interactive prediction results, and agricultural safety guidance.
- **Safety Disclaimers**: Actionable application instructions with prominent agricultural caution notices.

---

## Repository Structure

```text
AgriSense-AI/
├── backend/
│   └── app/
│       ├── api/
│       │   └── fertilizer.py          # FastAPI fertilizer prediction router
│       ├── core/
│       │   ├── config.py              # Environment configuration & settings
│       │   └── logging_config.py      # Structured application logging
│       ├── db/
│       │   └── session.py             # SQLAlchemy session manager
│       ├── schemas/
│       │   └── fertilizer.py          # Pydantic v2 request & response schemas
│       ├── services/
│       │   └── fertilizer_service.py  # Business logic & ML bridge
│       └── main.py                    # FastAPI application entrypoint
├── data/
│   ├── raw/                           # Immutable raw dataset (CC0)
│   └── processed/                     # Preprocessed & scaled datasets
├── docs/
│   ├── AVINASH_PROGRESS.md            # Module development milestone tracker
│   ├── DATASET_DOCUMENTATION.md       # Dataset metadata & schema documentation
│   └── MODEL_EVALUATION.md            # ML benchmark results & confusion matrix
├── frontend/
│   ├── src/
│   │   ├── components/                # Modular React components
│   │   │   ├── FertilizerCard.jsx
│   │   │   ├── FertilizerDisclaimer.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   └── FertilizerPage.jsx     # Main fertilizer recommendation UI
│   │   ├── services/
│   │   │   └── api.js                 # Axios API service with fallback
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── ml/
│   ├── artifacts/                     # Serialized pipelines and metadata (.joblib)
│   ├── inference/
│   │   └── fertilizer_service.py      # ML inference engine
│   └── training/
│       ├── fertilizer_eda.ipynb       # Exploratory data analysis notebook
│       ├── models.py                  # Standalone pure-Python/NumPy estimators
│       └── train.py                   # Multi-model training and evaluation script
├── tests/
│   ├── test_api_endpoints.py          # FastAPI endpoint integration tests
│   ├── test_environment.py            # Environment & runtime verification
│   ├── test_ml_pipeline.py            # ML pipeline inference verification
│   └── test_schemas.py                # Pydantic schema validation tests
├── requirements.txt                   # Backend Python dependencies
└── README.md                          # Project documentation
```

---

## Getting Started

### 1. Prerequisites
- Python 3.11+ (Python 3.14 verified)
- Node.js LTS (v20.x+) & npm

### 2. Backend Setup & Execution

1. **Activate virtual environment or use Python**:
   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start FastAPI Development Server**:
   ```bash
   uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   - Swagger API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Health check: [http://127.0.0.1:8000/api/predict/fertilizer/health](http://127.0.0.1:8000/api/predict/fertilizer/health)

### 3. Frontend Setup & Execution

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Vite Development Server**:
   ```bash
   npm run dev
   ```
   - Frontend Application: [http://localhost:5173](http://localhost:5173)

3. **Production Build**:
   ```bash
   npm run build
   ```

### 4. Running the Test Suite

Execute the complete 18-test validation suite:
```bash
pytest tests/ -v
```

---

## Machine Learning Pipeline & Performance

| Model | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| Dummy Baseline | 21.74% | 0.0311 | 0.1429 | 0.0510 |
| Logistic Regression | 86.96% | 0.7571 | 0.8214 | 0.7732 |
| **Decision Tree (Champion)** | **91.30%** | **0.7810** | **0.8571** | **0.8127** |
| Random Forest | 91.30% | 0.7810 | 0.8571 | 0.8127 |

The champion model (`DecisionTreeClassifier`) achieves **91.30% test accuracy** and **81.27% Macro F1-Score** across all 7 fertilizer categories. See [docs/MODEL_EVALUATION.md](docs/MODEL_EVALUATION.md) for full confusion matrices and per-class metrics.

---

## License & Safety Notice
This software provides decision-support guidance based on statistical patterns. Output recommendations should be evaluated alongside local soil test laboratory reports and regional agricultural extension guidelines before field application.

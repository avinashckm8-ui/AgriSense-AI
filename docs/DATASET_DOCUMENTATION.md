# Fertilizer Recommendation Module – Dataset Documentation

## 1. Dataset Overview
- **Dataset Title:** Fertilizer Prediction Dataset
- **Domain:** Precision Agriculture & Soil Nutrient Management
- **Source:** Kaggle Agricultural Research Data / Indian Soil and Agricultural Test Repositories (Glady Cleetus / Abhishek)
- **License:** Open Access / CC0 (Public Domain Dedication)
- **Target File Path:** `data/raw/Fertilizer Prediction.csv`

---

## 2. Feature Schema & Column Definitions

The dataset contains **8 input features** and **1 target classification label**:

| Column Name | Data Type | Units / Range | Description | Role |
| :--- | :--- | :--- | :--- | :--- |
| `Temparature` | Numerical (float) | °C (approx. 25°C – 38°C) | Ambient atmospheric temperature | Input Feature |
| `Humidity` | Numerical (float) | % (approx. 50% – 72%) | Relative ambient humidity | Input Feature |
| `Moisture` | Numerical (float) | % (approx. 25% – 65%) | Soil moisture percentage | Input Feature |
| `Soil Type` | Categorical (string) | 5 Classes: Sandy, Loamy, Black, Red, Clayey | Soil morphological classification | Input Feature |
| `Crop Type` | Categorical (string) | 11 Classes: Maize, Sugarcane, Cotton, Tobacco, Paddy, Barley, Wheat, Millets, Oil seeds, Pulses, Ground Nuts | Target cultivated crop | Input Feature |
| `Nitrogen` | Numerical (float) | Ratio / ppm (0 – 42) | Available soil nitrogen (N) level | Input Feature |
| `Potassium` | Numerical (float) | Ratio / ppm (0 – 19) | Available soil potassium (K) level | Input Feature |
| `Phosphorous` | Numerical (float) | Ratio / ppm (0 – 42) | Available soil phosphorous (P) level | Input Feature |
| `Fertilizer Name` | Categorical (string) | 7 Classes (Urea, DAP, 14-35-14, 28-28-0, 17-17-17, 20-20, 10-26-26) | Optimal chemical fertilizer formulation | **Target Label** |

---

## 3. Supported Fertilizer Categories

The model is strictly constrained to recommending the following 7 commercial formulations supported by the dataset:

1. **Urea:** High-nitrogen synthetic fertilizer (46-0-0), primarily recommended for nitrogen-deficient soils in leafy and vegetative growth stages.
2. **DAP (Diammonium Phosphate):** High-phosphorus and nitrogen fertilizer (18-46-0), recommended for root establishment and flowering.
3. **14-35-14:** High-phosphorus complex fertilizer with balanced nitrogen and potassium.
4. **28-28-0:** Nitrogen-phosphorus complex fertilizer suitable for initial growth phases.
5. **17-17-17:** Complete balanced N-P-K formulation for multi-nutrient deficient soils.
6. **20-20:** Balanced nitrogen and phosphorus formulation.
7. **10-26-26:** High-potassium and phosphorus complex fertilizer for fruiting, grain-filling, and disease resistance.

---

## 4. Agricultural Safety & Constraints

> [!WARNING]
> **Agronomic Limitation & Scope**
> 1. **Category Recommendation Only:** The dataset predicts the *formulation category*, **never the application rate or volumetric dosage per acre/hectare**.
> 2. **Soil Testing Required:** Automated recommendations must be corroborated by certified laboratory soil testing (pH, organic carbon, micro-nutrients).
> 3. **Local Extension Advice:** Regional agro-climatic conditions, seasonal rainfall, and irrigation availability require local agricultural extension officer guidance.

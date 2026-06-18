# Fashion Forward StyleSense Project

## Overview

This project builds a machine learning pipeline for StyleSense, a fashion e-commerce retailer, to predict whether a customer would recommend a product based on review text, customer age, product category, price range, and rating.

The pipeline handles:
- mixed data types (numerical, categorical, text)
- data preprocessing with scaling, one-hot encoding, and TF-IDF vectorization
- model training using Random Forest, Gradient Boosting, and Logistic Regression
- evaluation with accuracy, precision, recall, F1, and ROC-AUC
- sample prediction scenarios

## Project Structure

```
data_science_pipeline_project/
├── data/                     # Sample dataset folder
│   └── stylesense_reviews.csv
├── data_generation.py         # Synthetic dataset creation
├── preprocessing.py           # Data preprocessing pipeline
├── model.py                   # Model training, evaluation, saving, and comparison
├── train.py                   # End-to-end training and evaluation script
├── test.py                    # Pytest test suite
├── docs/                      # Validation and data profile docs
│   ├── business_scenario_validation.md
│   └── sample_data_profile.md
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Installation

```bash
cd data_science_pipeline_project
python -m pip install -r requirements.txt
```

## Environment Setup (Notebook)

This project is intended to run in a Jupyter-enabled Python environment.

Required packages for the code portion:
- `scikit-learn`
- `numpy`
- `pandas`
- `spacy`

Recommended setup:

```bash
# optional but recommended
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# install project dependencies
python -m pip install -r requirements.txt
```

Quick environment validation:

```bash
python -c "import sklearn,numpy,pandas,spacy,ipykernel; print('environment_ok')"
```

spaCy note:
- If spaCy installation requires platform-specific extras on your machine, install those first (for example, `python -m pip install 'spacy[apple]'` on Apple Silicon), then run `python -m pip install -r requirements.txt`.

## Usage

### Generate dataset and train models

```bash
cd data_science_pipeline_project
python train.py
```

### Run tests

```bash
cd data_science_pipeline_project
python -m pytest test.py -q
```

## Sample Data (Current Snapshot)

Sample dataset file:
- `data/stylesense_reviews.csv`

Last refreshed:
- 2026-06-18 (generated with `n_samples=1000`, `random_state=42`)

Current profile:
- Rows: 1000
- Columns: `age`, `category`, `price_range`, `rating`, `review_text`, `recommend`
- Missing values: 0
- Recommendation rate: 53.4%

To refresh sample data:

```bash
cd data_science_pipeline_project
python -c "from pathlib import Path; from data_generation import generate_stylesense_dataset, save_dataset; df=generate_stylesense_dataset(n_samples=1000, random_state=42); save_dataset(df, Path('data/stylesense_reviews.csv'))"
```

## Notes

- The dataset is synthetic and generated automatically if it does not already exist.
- Models are saved in the `models/` directory when persisted.
- The project focuses on building a robust pipeline for classification using mixed data types.
- Business scenario validation report: `docs/business_scenario_validation.md`.
- Sample data profile: `docs/sample_data_profile.md`.

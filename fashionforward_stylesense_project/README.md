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
fashionforward_stylesense_project/
├── data/                      # Generated dataset storage
├── data_generation.py         # Synthetic dataset creation
├── preprocessing.py           # Data preprocessing pipeline
├── model.py                   # Model training, evaluation, saving, and comparison
├── train.py                   # End-to-end training and evaluation script
├── requirements.txt           # Python dependencies
├── tests/                     # Pytest test suite
│   ├── __init__.py
│   └── test_fashionforward.py
├── notebooks/                 # Optional notebooks for exploration
└── README.md                  # Project documentation
```

## Installation

```bash
cd fashionforward_stylesense_project
python3 -m pip install -r requirements.txt
```

## Usage

### Generate dataset and train models

```bash
cd fashionforward_stylesense_project
python3 train.py
```

### Run tests

```bash
cd fashionforward_stylesense_project
python3 -m pytest -q
```

## Notes

- The dataset is synthetic and generated automatically if it does not already exist.
- Models are saved in the `models/` directory.
- The project focuses on building a robust pipeline for classification using mixed data types.

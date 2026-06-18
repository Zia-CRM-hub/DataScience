# Business Scenario Validation: Fashion Forward Forecasting

Date: 2026-06-18
Project: data_science_pipeline_project

## Scenario Summary

StyleSense needs a model that predicts whether a customer would recommend a product when the recommendation label is missing, using mixed feature types (text, numerical, categorical), with proper training and evaluation.

## Validation Against Requirements

### 1) Build a machine learning model pipeline from provided data

Status: PASS

Evidence:
- End-to-end orchestration exists in `train.py`.
- Dataset loading/generation in `data_generation.py`.
- Preprocessing and split logic in `preprocessing.py`.
- Model training/evaluation/comparison in `model.py`.
- Automated test coverage in `test.py`.

### 2) Handle mixed data types appropriately

Status: PASS

Evidence:
- Numerical features (`age`, `rating`) use `StandardScaler`.
- Categorical features (`category`, `price_range`) use `OneHotEncoder(handle_unknown='ignore')`.
- Text feature (`review_text`) uses `TfidfVectorizer`.
- Transformers are combined in a `ColumnTransformer` pipeline.

Implementation note:
- Text column routing was corrected so TF-IDF receives a 1D text series (required by scikit-learn).

### 3) Properly train and evaluate the model

Status: PASS

Evidence:
- Models trained: Random Forest, Gradient Boosting, Logistic Regression.
- Metrics computed: Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix, classification report.
- Best model selected by F1 score.

Observed run output (`python train.py`):
- Logistic Regression achieved the best F1: 0.8113.
- Full model comparison table is printed in pipeline output.

## Business Use-Case Check: Missing Recommendation Labels

Status: PASS

Validation approach:
- Trained logistic regression model.
- Removed `recommend` from a sample of records.
- Ran prediction using the fitted preprocessing pipeline + classifier.

Observed output:
- `unlabeled_rows = 25`
- `pred_recommend = 11`
- `pred_not_recommend = 14`

Conclusion:
- The project supports scoring unlabeled review records, matching the backlog triage scenario.

## Quality Gate Results

- Test run: `python -m pytest test.py -q`
- Result: `19 passed`

## Issues Found and Resolved During Validation

1. Training failed when `data/` directory did not exist.
- Fix: ensure parent directory creation before CSV write in `save_dataset`.

2. Preprocessing failed due to text transformer input shape mismatch.
- Fix: route text transformer to single column label (`review_text`) so TF-IDF gets 1D input.

3. Test compatibility and precision issues with modern pandas/sparse outputs.
- Fixes:
  - Updated dtype assertions to `is_string_dtype`.
  - Updated sparse matrix consistency assertion to tolerance-based `assert_allclose` on dense arrays.

## Final Validation Outcome

Business scenario is validated and operational for the current codebase.
The pipeline can train, evaluate, compare models, and predict recommendation outcomes for records with missing recommendation labels.

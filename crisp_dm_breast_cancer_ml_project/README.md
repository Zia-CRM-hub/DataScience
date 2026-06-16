# CRISP-DM Machine Learning Project: Predicting Breast Cancer Diagnosis

## Project Overview
This project follows the **CRISP-DM** process to explore, clean, model, evaluate, and interpret a machine learning solution using the Breast Cancer Wisconsin diagnostic dataset available in `scikit-learn`.

The goal is to build a classification model that predicts whether a tumor is **malignant** or **benign** based on diagnostic measurements computed from digitized images of fine needle aspirate samples.

## Motivation
Healthcare and diagnostic teams often need decision-support tools that can help prioritize cases for expert review. This project demonstrates how exploratory data analysis and supervised machine learning can help identify patterns in diagnostic measurements and generate a prediction for a new patient scenario.

> Note: This project is for learning and analytics demonstration only. It is not intended for clinical decision-making.

## CRISP-DM Process Followed
1. **Business Understanding**  
   Define the prediction problem and key questions of interest.

2. **Data Understanding**  
   Explore distributions, correlations, class balance, and underlying data structure.

3. **Data Preparation**  
   Check for missing values, duplicates, skewness, and scale features for modeling.

4. **Modeling**  
   Train classification models including Logistic Regression and Random Forest.

5. **Evaluation**  
   Compare accuracy, precision, recall, F1-score, and ROC-AUC.

6. **Deployment / Communication**  
   Provide an example prediction scenario and translate findings into a non-technical blog post.

## Questions of Interest
This project answers the following questions:

1. Which diagnostic features show strong differences between malignant and benign tumors?
2. Does the dataset require cleaning before modeling?
3. Which model performs better for predicting tumor diagnosis?
4. How should we interpret a prediction for a new diagnostic scenario?

## Repository Structure

| File | Description |
|---|---|
| `README.md` | Project overview, motivation, files, results, and acknowledgments |
| `crisp_dm_breast_cancer_analysis.ipynb` | Main Jupyter notebook containing EDA, cleaning, modeling, evaluation, and prediction scenario |
| `blog_post.md` | Non-technical blog post explaining questions, findings, and business-friendly interpretation |
| `requirements.txt` | Python libraries required to run the project |
| `.gitignore` | Suggested files and folders to exclude from GitHub |

## Libraries Used
- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- joblib

## Summary of Results
The notebook trains and compares Logistic Regression and Random Forest classifiers. The evaluation focuses not only on overall accuracy but also on **recall**, because in a health-oriented screening scenario missing a malignant case can be more serious than creating a false alert.

Typical results from this dataset show that both models perform strongly, with high accuracy and recall. The final model selection should be based on the actual metrics produced when the notebook is run.

## Example Prediction Scenario
The notebook includes a new diagnostic scenario using sample measurements from the dataset. The trained model predicts whether the case is likely to be malignant or benign and provides a probability score for interpretation.

## How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open the notebook:
   ```bash
   jupyter notebook crisp_dm_breast_cancer_analysis.ipynb
   ```
4. Run all cells from top to bottom.

## Acknowledgments
- Dataset: Breast Cancer Wisconsin diagnostic dataset, available through `scikit-learn`.
- CRISP-DM framework for structuring the end-to-end analytics process.
- This project template was created for learning and portfolio demonstration purposes.
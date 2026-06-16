# Can Diagnostic Measurements Help Predict Breast Cancer Risk?

![Illustration of data-driven healthcare decision support](https://images.unsplash.com/photo-1579154204601-01588f351e67)

Healthcare decisions are complex, and final diagnosis should always remain with qualified medical professionals. However, data can help us understand patterns, prioritize review, and support faster decision-making. In this project, I explored whether machine learning can use diagnostic measurements to predict whether a breast tumor is likely to be malignant or benign.

The analysis follows a structured data science approach called **CRISP-DM**, which starts with understanding the business question, explores the data, prepares it for analysis, builds a model, evaluates the outcome, and communicates the findings in a practical way.

## Questions I Wanted to Answer

### 1. Are there visible differences between malignant and benign cases?
The first step was to explore the dataset and compare measurements across diagnosis groups. Several measurements, such as radius, perimeter, area, concavity, and concave points, showed noticeable separation between malignant and benign cases.

This means that the dataset contains meaningful signals that a machine learning model can learn from. These signals are not perfect on their own, but together they help create a stronger prediction.

### 2. Did the data need cleaning?
The data was checked for missing values, duplicate records, unusual distributions, and feature scaling needs. The dataset did not require heavy cleaning, but the features were scaled before training models because some machine learning algorithms perform better when numeric inputs are on a similar scale.

This step matters because even a strong model can give poor results if the data preparation stage is skipped.

### 3. Which model performed better?
Two models were compared: Logistic Regression and Random Forest. The evaluation used accuracy, precision, recall, F1-score, and ROC-AUC.

For this type of problem, **recall** is especially important. Recall tells us how well the model identifies malignant cases. In a medical screening-style problem, missing a serious case can be more harmful than raising an additional alert.

The final notebook compares the models and selects the one with the best balance of performance measures.

### 4. What does a model prediction look like in practice?
To make the analysis more practical, the project includes a new diagnostic scenario. The model receives a set of diagnostic measurements and predicts whether the case is more likely to be malignant or benign. It also provides a probability score, which helps readers understand the model's confidence.

The key takeaway is that machine learning can support pattern recognition, but the prediction should be treated as decision support rather than a replacement for medical judgment.

## Key Takeaways

- Diagnostic measurements contain meaningful patterns that can help distinguish malignant and benign cases.
- Exploratory data analysis is essential before modeling because it reveals distribution patterns, class balance, and feature relationships.
- Data cleaning was minimal, but feature scaling was important for reliable modeling.
- Model evaluation should go beyond accuracy. Recall, precision, F1-score, and ROC-AUC provide a fuller picture.
- A prediction is most useful when explained in plain language and connected to a realistic scenario.

## Final Thoughts

This project shows how a structured machine learning workflow can turn raw diagnostic measurements into practical insights. The most valuable part of the process is not only building a model, but explaining what the model learned, how well it performs, and how its prediction should be interpreted by non-technical readers.
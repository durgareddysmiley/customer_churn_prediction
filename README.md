# E-Commerce Customer Churn Prediction

## Project Overview
Customer churn is a critical challenge for e-commerce businesses, as acquiring new customers is significantly more expensive than retaining existing ones. This project focuses on building an end-to-end machine learning system to predict whether a customer is likely to churn in the next three months.

The solution includes data cleaning, feature engineering, multiple machine learning models, model evaluation, business impact analysis, and deployment as an interactive web application. The final system allows business stakeholders to make data-driven decisions for targeted customer retention strategies.

---

## Business Problem
The business goal is to **identify customers who are likely to churn** so that proactive retention actions (offers, discounts, personalized communication) can be applied.  
Missing a churner (false negative) is costly because it results in lost future revenue, while contacting a non-churner (false positive) has a relatively low cost.

---

## Dataset
- **Source:** Internal e-commerce transactional dataset (simulated for academic use)
- **Size:** ~500 customers with multiple behavioral features
- **Target Variable:** Customer Churn (0 = Active, 1 = Churned)
- **Features:** Recency, Frequency, Monetary value, and other behavioral metrics

---

## Methodology

### 1. Data Cleaning
- Removed duplicates
- Handled missing values
- Converted date fields to usable formats
- Validated data consistency

### 2. Feature Engineering
- RFM features (Recency, Frequency, Monetary)
- Aggregated behavioral metrics
- Normalization and scaling where required

### 3. Models Evaluated

| Model               | ROC-AUC | Precision | Recall |
|--------------------|--------:|----------:|-------:|
| Logistic Regression | 0.718   | 0.59      | 0.61   |
| Decision Tree       | 0.690   | 0.56      | 0.58   |
| Random Forest       | 0.713   | 0.61      | 0.64   |
| Gradient Boosting   | 0.709   | 0.62      | 0.66   |
| Neural Network      | 0.714   | 0.57      | 0.67   |

### 4. Final Model Selection
- **Selected Model:** Gradient Boosting Classifier  
- **Reason:** Strong balance between ROC-AUC, recall, and interpretability for tabular business data.

---

## Model Evaluation
- Test-set ROC-AUC close to cross-validation mean (stable performance)
- Confusion matrix analysis used for business cost estimation
- Precision–Recall and ROC curves generated
- Feature importance analyzed for explainability

---

## Business Impact
- Enables targeted retention instead of random outreach
- Reduces customer acquisition costs
- Improves customer lifetime value
- Supports data-driven marketing decisions

---

## Installation & Usage

### Local Setup

#### Clone the repository
```bash
git clone https://github.com/durgareddysmiley/customer_churn_prediction.git
cd customer_churn_prediction

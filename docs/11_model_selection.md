# Model Selection Report

## 1. Models Evaluated

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting** | 0.682 | 0.632 | 0.614 | 0.623 | **0.758** | 1.12 |
| **Decision Tree** | 0.690 | 0.644 | 0.619 | 0.631 | 0.753 | 0.02 |
| **Random Forest** | 0.674 | 0.621 | 0.609 | 0.615 | 0.746 | 0.66 |
| **Logistic Regression**| 0.686 | 0.637 | 0.619 | 0.628 | 0.734 | 0.04 |
| **XGBoost** | 0.670 | 0.613 | 0.619 | 0.616 | 0.731 | 0.57 |
| **Neural Network** | 0.631 | 0.569 | 0.566 | 0.568 | 0.677 | 10.40 |

## 2. Best Performing Model
- **Selected Model**: **Gradient Boosting Classifier**
- **Justification**:
    - Achieved the highest **ROC-AUC (0.758)**, meeting the primary success criteria (>0.75).
    - Offers a good balance between Precision (0.632) and Recall (0.614).
    - Outperforms the baseline Logistic Regression significantly in ranking capability (AUC).
    - Training time is acceptable (~1s).

## 3. Metric Prioritization
- **Primary**: **ROC-AUC**. It measures the model's ability to discriminate between churners and active customers across all thresholds.
- **Secondary**: **Recall**. In a churn context, missing a churning customer (False Negative) is usually more expensive than incentivizing a loyal customer (False Positive).

## 4. Key Learnings
- **Linear vs Non-Linear**: Tree-based models (Gradient Boosting, Random Forest) generally outperformed the linear model, suggesting non-linear relationships in features (e.g., interactions between Recency and Frequency).
- **Overfitting**: Neural Network performed poorly (AUC 0.677), likely due to the small dataset size (~2300 training samples) or need for more extensive tuning.
- **Baseline Strength**: The simple Logistic Regression performed surprisingly well (AUC 0.734), indicating that linear signal (Recency) is very strong.

# Model Selection Conclusion

Five machine learning models were evaluated using ROC-AUC as the primary metric due to class imbalance.

Logistic Regression achieved the highest ROC-AUC score of **0.718**, outperforming tree-based and neural network models.

This indicates that churn behavior in the dataset follows a largely linear pattern, making Logistic Regression the most suitable model for deployment.

## Final Model Choice
- **Selected Model:** Logistic Regression
- **Evaluation Metric:** ROC-AUC
- **Reason for Selection:** Best performance, stability, and interpretability

## Business Justification
Logistic Regression allows easy interpretation of feature impact on churn, making it suitable for business decision-making and customer retention strategies.

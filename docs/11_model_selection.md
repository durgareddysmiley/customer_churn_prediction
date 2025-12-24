# Model Selection Report

## Models Evaluated

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
|------|----------|-----------|--------|----------|---------|---------------|
| Logistic Regression | 0.6548 | 0.5922 | 0.6073 | 0.5996 | 0.7182 | 0.6 sec |
| Decision Tree | 0.6300 | 0.5600 | 0.5800 | 0.5700 | 0.6898 | 0.2 sec |
| Random Forest | 0.6700 | 0.6100 | 0.6400 | 0.6250 | 0.7134 | 1.2 sec |
| Gradient Boosting (XGBoost) | 0.6800 | 0.6200 | 0.6600 | 0.6400 | 0.7086 | 1.8 sec |
| Neural Network | 0.6467 | 0.5720 | 0.6748 | 0.6192 | 0.7137 | 0.65 sec |

---

## Performance Analysis

### Best Performing Model

**Model:** Gradient Boosting (XGBoost)

**Justification:**  
Although Logistic Regression achieved the highest ROC-AUC, Gradient Boosting provided the best overall balance of Accuracy, Recall, and F1-Score.  
Since churn prediction focuses on identifying churn-prone customers, higher recall and balanced performance make Gradient Boosting the most suitable model.

---

## Metric Prioritization

**Most Important Metric:** Recall

**Why:**  
In churn prediction, missing a churned customer (false negative) is more costly than incorrectly flagging an active customer.

**Trade-offs:**  
Maximizing recall may reduce precision, but this trade-off is acceptable because retention campaigns are cheaper than losing customers.

---

## Model Selection Decision

**Selected Model:** Gradient Boosting (XGBoost)

### Reasons:

- **Performance:** Highest Accuracy, Recall, and F1-Score
- **Interpretability:** Feature importance helps identify churn drivers
- **Deployment Complexity:** Easily deployable using Python, joblib, Streamlit, and Docker
- **Training Time:** Acceptable compared to ensemble models

---

## What I Learned

### Key Takeaways:
- Logistic Regression provides a strong baseline for churn prediction.
- Decision Trees tend to overfit without depth control.
- Random Forest improves stability but increases training time.
- Gradient Boosting offers the best bias–variance trade-off.
- Neural Networks require careful tuning for tabular data.

### Challenges Faced:
- Selecting the most business-relevant evaluation metric
- Balancing recall and precision

### How I Solved Them:
- Focused on Recall and F1-Score instead of accuracy alone
- Compared models using multiple metrics

---

## Mistakes Made & Corrections

- Initially focused mainly on ROC-AUC
- Corrected by prioritizing Recall based on business impact

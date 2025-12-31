# Business Impact Analysis

## 1. Model Performance (Test Set)
- **ROC-AUC**: **0.70** (Good, but slightly below 0.75 target).
- **Precision**: **0.59**. For every 100 customers we predict as "Churning", 59 actually churn.
- **Recall**: **0.60**. We catch 60% of all churners.

## 2. Business Cost Analysis
**Assumptions**:
- **Cost of Retention Offer**: £10 / customer.
- **Value of Retained Customer (CLV)**: £500.
- **Retention Success Rate**: 20% (if we contact a churner, we save them 20% of the time).

### Scenario A: No Model (Random Targeting)
- If we target 100 random customers, 42 will be churners (based on 42% churn rate).
- **Cost**: £1,000 (100 * £10).
- **Saved**: 20% of 42 = 8.4 customers.
- **Value Saved**: 8.4 * £500 = £4,200.
- **Net Profit**: £3,200.
- **ROI**: 320%.

### Scenario B: Targeted with Our Model
- If we target 100 predicted churners.
- **Precision is 59%**: So 59 are actual churners.
- **Cost**: £1,000.
- **Saved**: 20% of 59 = 11.8 customers.
- **Value Saved**: 11.8 * £500 = £5,900.
- **Net Profit**: £4,900.
- **ROI**: **490%**.

## 3. Conclusion
Using the model improves ROI from 320% to 490%, representing a significant financial gain despite the model's modest accuracy.

## 4. Recommendations
- **Target High Value**: Prioritize customers with high `TotalSpent` who are flagged as churners.
- **Intervention**: Send personalized emails ("We miss you") rather than deep discounts to high-probability churners to protect margins.
- **Monitor**: The model performance (AUC 0.70) suggests there is noise in the data. Retrain monthly.

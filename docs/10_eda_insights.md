# EDA Key Insights

## 1. Churn Patterns Discovered

1. Recency is the strongest churn indicator.
   Churned customers show significantly higher recency values.
   Statistical test confirms p < 0.001.

2. Customers with no purchases in the last 30 days are highly likely to churn.

3. Frequency is negatively correlated with churn.
   High-frequency customers churn less.

4. TotalSpent shows that high-value customers are less likely to churn.

5. PurchaseVelocity is significantly lower for churned customers.

6. Customers with low RFM scores have the highest churn rate.

7. At Risk and Lost segments show the highest churn proportions.

8. Champions and Loyal segments have very low churn rates.

9. Customers with low product diversity churn faster.

10. Customers with long inactive periods (>90 days) show extreme churn probability.

---

## 2. Customer Segment Analysis

- Champions: Lowest churn, highest value
- Loyal: Stable purchasing, moderate churn
- At Risk: High churn risk, need retention campaigns
- Lost: Already churned, low engagement

---

## 3. Feature Recommendations for Modeling

Based on EDA, the most important features are:
- Recency
- Purchases_Last30Days
- Frequency
- PurchaseVelocity
- RFM_Score
- TotalSpent

---

## 4. Hypotheses for Testing

H1: Customers with recency > 90 days are significantly more likely to churn  
H2: High-frequency customers (>10 purchases) rarely churn  
H3: Customers with recent activity in last 30 days have low churn probability  
H4: Purchase velocity is negatively correlated with churn  

---

## Conclusion

EDA clearly shows that customer engagement and recent activity are the strongest predictors of churn. These insights will guide feature selection and model optimization.

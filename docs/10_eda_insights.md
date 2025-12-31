# EDA Key Insights

## 1. Churn Patterns Discovered
- **Finding 1: Recency is the strongest indicator**.
    - **Evidence**: Churned customers have a significantly higher Recency (days since last purchase) compared to active customers. T-test p-value < 0.0001.
    - **Business Implication**: Customers who haven't purchased in the last 60-90 days are at extreme risk. Immediate re-engagement is needed.
- **Finding 2: High frequency reduces churn risk**.
    - **Evidence**: Active customers have a much higher purchase frequency. There is a long tail of one-time buyers who churn (leave) after a single purchase.
- **Finding 3: Monetary value correlates with retention**.
    - **Evidence**: Higher `TotalSpent` is associated with lower churn rates. High-value customers tend to be more loyal.
- **Finding 4: Irregular purchase intervals signal churn**.
    - **Evidence**: `AvgDaysBetweenPurchases` difference is significant (p ~ 0.01). Irregular patterns often precede churn.

## 2. Customer Segments Analysis
- **Champions & Loyal**: Lowest churn rates. These customers buy frequently and recently.
- **At Risk**: High churn rate. These are customers who *used* to buy frequently but haven't bought recently.
- **Lost**: Highest churn rate. Low frequency, high recency.

## 3. Feature Recommendations for Modeling
Based on EDA, the following features are critical:
1.  **Recency**: Primary predictor.
2.  **Frequency**: Secondary predictor.
3.  **CustomerLifetimeDays**: Indicates relationship maturity.
4.  **AvgDaysBetweenPurchases**: Behavioral signal.
5.  **TotalSpent**: Value signal.

## 4. Hypotheses for Testing
- **H1**: A decision tree will split primarily on `Recency`.
- **H2**: Gradient Boosting will outperform Logistic Regression by capturing non-linear relationships between Frequency and Recency.

# Business Problem Statement

## 1. Business Context
In the highly competitive e-commerce landscape, customer acquisition costs are rising, often costing 5-25 times more than retaining existing customers. "RetailCo Analytics" faces the challenge of identifying customers at risk of leaving (churning) to proactively engage them. By understanding customer behavior and purchase patterns, the company aims to optimize marketing spend and increase customer lifetime value (CLV).

## 2. Problem Definition
We define **Customer Churn** using a temporal split approach:
- **Target Definition**: A customer is considered churned if they do not make any purchase in the **observation period (next 3 months)** after the training period.
- **Goal**: Predict the probability of a customer churning in the next 3 months based on their historical transaction data.

## 3. Stakeholders
- **Marketing Team**: Needs to identify at-risk customers to target with retention campaigns and personalized offers.
- **Sales Team**: Needs insights into high-value customers who might be churning to intervene personally.
- **Product Team**: Can use insights to improve product offerings or user experience.
- **Executive Team**: Interested in the overall ROI of the retention strategy and projected revenue impact.

## 4. Business Impact
- **Primary Goal**: Reduce customer churn rate by 15-20% through targeted interventions.
- **Revenue Impact**: Retaining high-value customers significantly boosts monthly revenue.
- **Cost Savings**: More efficient allocation of marketing budget by focusing on customers most likely to be saved/churn.

## 5. Success Metrics
### Primary Metric
- **ROC-AUC Score > 0.75**: Ensures the model minimizes false positives and false negatives effectively across different thresholds.

### Secondary Metrics
- **Precision > 0.70**: critical to minimize the cost of sending retention offers to customers who were not actually going to churn (False Positives).
- **Recall > 0.65**: Critical to capture as many actual churners as possible (preventing False Negatives).
- **F1-Score**: A balance between Precision and Recall.

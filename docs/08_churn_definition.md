# Churn Definition

## Problem Statement
The objective of this project is to predict customer churn for an e-commerce business.
Churn refers to customers who stop making purchases for a significant period of time.
A clear, time-based churn definition is required to build a reliable supervised machine learning model.

---

## Time-Based Approach
A temporal observation window approach is used to define churn.
This method prevents data leakage and reflects real-world customer purchasing behavior.

---

## Training and Observation Periods

The dataset spans from **2009-12-01 to 2011-12-09**.

It is divided into two non-overlapping periods:

### Training Period
- Used to calculate customer-level features (RFM and behavioral features)
- Only customers with at least one purchase in this period are considered

### Observation Period (90 Days)
- Used only to determine churn
- Checks whether the customer made any purchase again

---

## Churn Definition Logic

Only customers who made **at least one purchase during the training period** are included in churn analysis.

A customer is labeled as **Churned (1)** if:
- The customer made at least one purchase in the training period, AND
- The customer made **zero purchases** during the observation period (next 90 days)

A customer is labeled as **Active (0)** if:
- The customer made at least one purchase in the training period, AND
- The customer made **at least one purchase** during the observation period

---

## Implementation Logic (Conceptual)

Customers are first filtered to those who purchased during the training period.
Among them, customers who did not make any purchase during the observation period are labeled as churned.
All remaining customers are labeled as active.

This ensures churn is calculated only for previously active customers.

---

## Expected Distribution

Based on e-commerce industry standards:
- Expected churn rate: **20–40%**
- If churn rate is below 10% or above 60%, the churn logic should be reviewed

In this project, the observed churn rate is approximately **33%**, which lies within the expected range.

---

## Justification

### Why a 3-Month Observation Window?
- Industry standard for e-commerce churn analysis
- Avoids very short windows that capture seasonal inactivity
- Avoids very long windows that result in too few churned customers
- Aligns with quarterly business planning cycles

---

## Validation Criteria
- Churn rate between 20–40%
- No data leakage (features derived only from training period)
- Clear temporal separation between training and observation periods

---

## Conclusion
This churn definition follows industry best practices, avoids data leakage, and aligns with real-world business behavior.
It provides a reliable and interpretable target variable for churn prediction modeling.

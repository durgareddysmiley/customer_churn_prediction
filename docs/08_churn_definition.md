# Churn Definition

## 1. Problem Statement
In a non-contractual setting like e-commerce, "churn" is not explicitly defined (unlike cancelling a subscription). We must infer churn based on a period of inactivity. We define a customer as **churned** if they stop purchasing for a specific observation period.

## 2. Approach: Observation Window Method
We use a **Temporal Split** to create a labeled dataset without data leakage.

### Time Windows
- **Total Data Period**: 2010-12-01 to 2011-12-09
- **Training Period (Features)**: Data **before** the cutoff date.
- **Observation Period (Labels)**: Data **after** the cutoff date.

### Cutoff Logic
- **Cutoff Date**: `2011-09-09` (90 days before the last date in the dataset).
- **Observation Window**: 90 Days (3 months).

## 3. Churn Definition Rule
- **Target Variable**: `Churn` (Binary: 1 or 0)
- **Condition**:
    - **Churn = 1**: Customer made a purchase in the *Training Period* but **NO** purchase in the *Observation Period*.
    - **Churn = 0 (Active)**: Customer made a purchase in the *Training Period* **AND** made at least one purchase in the *Observation Period*.

## 4. Justification
- **90 Days**: A standard quarter. E-commerce customers who haven't bought in 3 months are at significant risk of being lost.
- **Leakage Prevention**: Features (like Recency) are calculated relative to the *Cutoff Date*, using only Training data. Future data (Observation period) is strictly reserved for generating the label.

## 5. Expected Distribution
- **Churn Rate**: We anticipate a churn rate between **20% and 40%**.
- If the rate is too low (<10%), the window might be too short (everyone buys in 3 months).
- If the rate is too high (>60%), the window might be too long or the business has a retention problem.

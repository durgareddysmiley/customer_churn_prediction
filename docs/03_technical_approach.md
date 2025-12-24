# Technical Approach

## Classification Approach

Customer churn prediction is treated as a **classification problem** rather than a regression problem because the business goal is to determine whether a customer will churn or not within the next 90 days.

The output required by business stakeholders is a clear decision or probability of churn, which naturally fits a binary classification setup (churn = yes or no). Regression would not directly align with this decision-making requirement.

---

## Feature Engineering Strategy

Transaction-level data is transformed into customer-level features using:
- RFM (Recency, Frequency, Monetary) analysis
- Behavioral patterns such as purchase frequency, basket size, and spending trends
- Temporal features capturing customer activity over time

These engineered features help capture customer behavior more effectively than raw transaction data.

---

## Model Selection Strategy

Multiple classification algorithms are tested to compare performance, including:
- Logistic Regression
- Tree-based models

Different models capture different data patterns, and testing multiple algorithms helps identify the best-performing and most stable model for churn prediction.

---

## Deployment Strategy Overview

The final trained model is deployed using a Streamlit web application.  
The application allows users to access churn predictions through a simple interface, and the solution is containerized using Docker to ensure reproducibility and consistent deployment across environments.

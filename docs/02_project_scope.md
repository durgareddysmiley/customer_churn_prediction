# Project Scope

## In Scope
- **Data Processing**: transform raw transaction-level data into a clean, customer-level dataset.
- **Feature Engineering**: Create RFM (Recency, Frequency, Monetary), behavioral, and temporal features.
- **Modeling**: Train and evaluate 5 different classification algorithms (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, Neural Network).
- **Evaluation**: Rigorous testing using a hold-out test set and cross-validation.
- **Deployment**: Interactive Streamlit web application for real-time and batch predictions.
- **Documentation**: Comprehensive technical and business documentation.

## Out of Scope
- **Real-time Streaming**: The solution will be batch-based, not processing transactions in real-time as they happen.
- **Product Recommendations**: The focus is solely on *churn prediction*, not recommending specific products.
- **Inventory Management**: No forecasting of stock levels.

## Analysis Timeline
- **Duration**: 8 Weeks (simulated).
- **Phases**:
    1.  Business Understanding
    2.  Data Acquisition & Cleaning
    3.  Feature Engineering
    4.  Modeling & Evaluation
    5.  Deployment & Reporting

## Constraints
- **Tools**: Open-source Python libraries (pandas, sklearn, streamlit) only.
- **Deployment**: Free tier platforms (Streamlit Cloud).
- **Data**: Determining churn based solely on the provided transactional data (no demographic data available).

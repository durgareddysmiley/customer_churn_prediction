# Technical Documentation

## System Architecture
Raw CSV -> Cleaning (Pandas) -> Feature Engineering (RFM/Temporal) -> Preprocessing (Sklearn Pipeline) -> Model (XGBoost/GradientBoosting) -> Streamlit App.

## Data Pipeline
1.  **Acquisition**: Downloads from UCI.
2.  **Cleaning**: Removes cancellations ('C' invoices), negative quantities, and missing CustomerIDs.
3.  **Features**:
    - Aggregates by `CustomerID`.
    - Computes Recency (days since last buy), Frequency (count), Monetary (sum).
    - segments customers into "Champions", "Loyal", etc.

## Model
- **Algorithm**: Gradient Boosting Classifier.
- **Hyperparameters**: Default sklearn settings (n_estimators=100, learning_rate=0.1).
- **Validation**: 5-Fold Stratified Cross-Validation.

## Deployment
- **Frontend**: Streamlit.
- **Backend**: Python inference using `joblib` loaded models.

# Technical Approach

## 1. Classification Approach
We are framing this as a **binary classification problem** (Churn vs. Active).
- **Why Classification?**: We need to make a distinct decision (Churn/No Churn) to trigger specific business actions. Probability outputs from classification models allow us to rank customers by risk.

## 2. Feature Engineering Strategy
Since the raw data is transactional (one row per item purchased), we must aggregate it to the customer level.
- **RFM Analysis**: Core metrics defining customer value.
- **Behavioral Features**: Inter-purchase time, basket size, return rate.
- **Temporal Features**: Evolution of purchase behavior over time (e.g., trend in spend).
- **One-Hot Encoding**: For categorical variables like customer segments.

## 3. Modeling Strategy
We will implement and compare multiple algorithms to find the best balance of performance and interpretability:
1.  **Logistic Regression**: Baseline model, highly interpretable.
2.  **Decision Tree**: Captures non-linear relationships, easy to visualize.
3.  **Random Forest**: Robust to overfitting, handles high dimensionality well.
4.  **Gradient Boosting (XGBoost)**: Often state-of-the-art for tabular data, handles class imbalance well.
5.  **Neural Network**: To capture complex, non-linear interactions.

## 4. Deployment Strategy
- **Web App**: Built with Streamlit for ease of use by non-technical stakeholders.
- **Model Serialization**: Models saved as `.pkl` files using `joblib`.
- **Dockerization**: Containerized environment to ensure reproducibility.

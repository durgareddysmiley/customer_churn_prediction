import pandas as pd
import joblib


MODEL_PATH = "models/gradient_boosting.pkl"
SCALER_PATH = "models/scaler.pkl"


def load_model():
    """
    Load the trained churn prediction model and feature scaler.

    Returns:
        tuple: Trained model and fitted scaler
    """
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def preprocess_input(input_df, scaler):
    """
    Scale input features using the trained scaler.

    Args:
        input_df (pd.DataFrame): Raw input feature DataFrame
        scaler (StandardScaler): Fitted feature scaler

    Returns:
        np.ndarray: Scaled feature array
    """
    return scaler.transform(input_df)


def predict_churn(input_df):
    """
    Predict churn class and probability for given customer data.

    Args:
        input_df (pd.DataFrame): Customer feature data

    Returns:
        tuple:
            np.ndarray: Churn predictions (0 = Active, 1 = Churn)
            np.ndarray: Churn probabilities
    """
    model, scaler = load_model()
    X_scaled = preprocess_input(input_df, scaler)

    churn_prob = model.predict_proba(X_scaled)[:, 1]
    churn_pred = (churn_prob >= 0.5).astype(int)

    return churn_pred, churn_prob

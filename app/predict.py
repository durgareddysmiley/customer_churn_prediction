import joblib
import pandas as pd
import numpy as np

# Paths
MODEL_PATH = "models/gradient_boosting.pkl"
SCALER_PATH = "models/scaler.pkl"
FEATURES_PATH = "data/processed/feature_names.json"


def load_model():
    """
    Load trained churn prediction model
    """
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")


def load_scaler():
    """
    Load feature scaler
    """
    try:
        scaler = joblib.load(SCALER_PATH)
        return scaler
    except Exception as e:
        raise RuntimeError(f"Error loading scaler: {e}")


def preprocess_input(data):
    """
    Preprocess input data (single or batch)
    """
    try:
        # Convert single dict to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise ValueError("Input must be dict or DataFrame")

        # Fill missing values safely
        df = df.fillna(df.median(numeric_only=True))

        scaler = load_scaler()
        X_scaled = scaler.transform(df)

        return X_scaled

    except Exception as e:
        raise RuntimeError(f"Error in preprocessing: {e}")


def predict(data):
    """
    Return churn prediction (0 or 1)
    """
    model = load_model()
    X = preprocess_input(data)
    preds = model.predict(X)
    return preds


def predict_proba(data):
    """
    Return churn probability (0–1)
    """
    model = load_model()
    X = preprocess_input(data)
    probs = model.predict_proba(X)[:, 1]
    return probs

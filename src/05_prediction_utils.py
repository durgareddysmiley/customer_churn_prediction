import pandas as pd
import joblib

MODEL_PATH = "models/gradient_boosting.pkl"
SCALER_PATH = "models/scaler.pkl"
FEATURES_PATH = "data/processed/feature_names.json"

def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def preprocess_input(df, scaler):
    df_scaled = scaler.transform(df)
    return df_scaled

def predict_churn(input_df):
    model, scaler = load_model()
    X = preprocess_input(input_df, scaler)

    churn_prob = model.predict_proba(X)[:, 1]
    churn_pred = (churn_prob >= 0.5).astype(int)

    return churn_pred, churn_prob

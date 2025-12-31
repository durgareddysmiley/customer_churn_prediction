import joblib
import pandas as pd
import numpy as np

MODEL_PATH = 'models/best_model.pkl'
PREPROCESSOR_PATH = 'models/preprocessor.pkl' # This acts as our scaler/encoder

def load_model():
    """Load the trained model and preprocessor"""
    try:
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        return model, preprocessor
    except FileNotFoundError:
        return None, None

def preprocess_input(data: dict, preprocessor):
    """
    Preprocess input dictionary to match training format
    """
    # specific columns expected by the model
    # Recency, Frequency, TotalSpent, TotalItems, UniqueProducts, AvgOrderValue,
    # AvgDaysBetweenPurchases, StdDaysBetweenPurchases, AvgBasketSize, MaxBasketSize,
    # CustomerLifetimeDays, R_Score, F_Score, M_Score, RFM_Score, prev_date, DaysBetween ??
    
    # We need to construct a DataFrame with the exact columns used in training (X_train)
    # Let's assume the user passes raw RFM values or we calculate scores on fly?
    # For simplicity, the app usually asks for the features directly.
    
    df = pd.DataFrame([data])
    
    # Transform using the saved preprocessor pipeline
    processed_array = preprocessor.transform(df)
    
    return processed_array

def make_prediction(input_data: dict):
    model, preprocessor = load_model()
    if not model or not preprocessor:
        return {"error": "Model not loaded"}
        
    try:
        processed_data = preprocess_input(input_data, preprocessor)
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0][1]
        
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "status": "Churn" if prediction == 1 else "Active"
        }
    except Exception as e:
        return {"error": str(e)}

def batch_predict(df):
    model, preprocessor = load_model()
    if not model or not preprocessor:
        return None
        
    processed_data = preprocessor.transform(df)
    predictions = model.predict(processed_data)
    probs = model.predict_proba(processed_data)[:, 1]
    
    return predictions, probs

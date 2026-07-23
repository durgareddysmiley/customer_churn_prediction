import pandas as pd
import joblib ## it is mainly used to save trained models so you don't have to train them every time. 

## Without Joblib:

## Train the model.
## Close Python.
## Next time, train the model again.
## This wastes time.

## With Joblib:

## Train the model once.
## Save it using Joblib.
## Next time, simply load the saved model.
## No retraining is needed.


MODEL_PATH = "models/gradient_boosting.pkl"
SCALER_PATH = "models/scaler.pkl"


def load_model():
    """
    Load the trained churn prediction model and feature scaler.

    Returns:
        tuple: Trained model and fitted scaler
    """
    model = joblib.load(MODEL_PATH)         ## joblib.load() reads a previously saved object from a file.
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

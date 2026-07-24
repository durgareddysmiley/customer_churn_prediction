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

    ## Earlier you saved 
    ## model.pkl
    ## scaler.pkl Now they are loaded into memory.
    X_scaled = preprocess_input(input_df, scaler)

    churn_prob = model.predict_proba(X_scaled)[:, 1]
    
    ## Suppose the model internally predicts
    ## model.predict_proba(X_scaled)
     ## [[0.25, 0.75]]
    ## This means:
    ## 0.25 (25%) → Probability the customer is Active (Class 0).
     ## 0.75 (75%) → Probability the customer will Churn (Class 1).
    ## Notice that the two probabilities always add up to 100%.
    ## 25% + 75% = 100%

    ## [:, 1]
     +## means:
     ## : → Select all rows
     ## 1 → Select only column 1 (the second column)
    churn_pred = (churn_prob >= 0.5).astype(int)
    ## So,
    ## .astype(int)
     ## converts them.
    ## Before	After
      False	     0
      True	      1

    return churn_pred, churn_prob

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import json

# Setup page config
st.set_page_config(page_title="Churn Predictor", layout="wide")

# Load Assets
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('models/best_model.pkl')
        preprocessor = joblib.load('models/preprocessor.pkl')
        feature_names = json.load(open('data/processed/feature_names.json'))
        return model, preprocessor, feature_names
    except:
        return None, None, None

model, preprocessor, feature_names = load_assets()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Single Prediction", "Batch Prediction", "Dashboard"])

if page == "Home":
    st.title("Customer Churn Prediction System")
    st.markdown("""
    Welcome to RetailCo Analytics Churn Predictor.
    
    ### How to use:
    1. **Single Prediction**: Enter customer details to get a real-time churn risk score.
    2. **Batch Prediction**: Upload a CSV of customers to score them all at once.
    3. **Dashboard**: View model performance metrics.
    """)
    
    st.info("Model Status: " + ("Loaded ✅" if model else "Not Loaded ❌"))

elif page == "Single Prediction":
    st.header("Single Customer Prediction")
    
    if not model:
        st.error("Model not found. Please train the model first.")
        st.stop()
        
    col1, col2 = st.columns(2)
    
    with col1:
        recency = st.number_input("Recency (Days since last buy)", min_value=0, value=30)
        frequency = st.number_input("Frequency (Total transactions)", min_value=1, value=5)
        total_spent = st.number_input("Total Spent (£)", min_value=0.0, value=500.0)
        lifetime = st.number_input("Customer Lifetime (Days)", min_value=0, value=100)

    with col2:
        avg_days = st.number_input("Avg Days Between Purchases", min_value=0.0, value=20.0)
        total_items = st.number_input("Total Items Purchased", min_value=1, value=50)
        unique_products = st.number_input("Unique Products", min_value=1, value=10)
        
    # Derived inputs rough estimation for demo
    input_data = {
        'Recency': recency,
        'Frequency': frequency,
        'TotalSpent': total_spent,
        'TotalItems': total_items,
        'UniqueProducts': unique_products,
        'AvgOrderValue': total_spent / frequency if frequency > 0 else 0,
        'AvgDaysBetweenPurchases': avg_days,
        'StdDaysBetweenPurchases': 0, # Default
        'AvgBasketSize': total_items / frequency if frequency > 0 else 0,
        'MaxBasketSize': total_items / frequency if frequency > 0 else 0, # Approx
        'CustomerLifetimeDays': lifetime,
        'R_Score': 4 if recency < 30 else (3 if recency < 60 else 1), # Approx
        'F_Score': 4 if frequency > 10 else 2,
        'M_Score': 4 if total_spent > 1000 else 2,
        'RFM_Score': 8, # Dummy
        # Add other cols if needed by preprocessor
    }
    
    # We need to match the feature set exactly. 
    # This is tricky with OneHotEncoding if we don't present the category.
    # The cleaned data had 'CustomerSegment' which was OHE.
    # We should let user select segment or infer it.
    segment = st.selectbox("Customer Segment", ["Champions", "Loyal", "Potential", "At Risk", "Lost"])
    input_data['CustomerSegment'] = segment
    
    if st.button("Predict"):
        df_input = pd.DataFrame([input_data])
        
        try:
            X_processed = preprocessor.transform(df_input)
            prob = model.predict_proba(X_processed)[0][1]
            pred = model.predict(X_processed)[0]
            
            st.metric("Churn Probability", f"{prob:.2%}")
            
            if prob > 0.7:
                st.error("High Churn Risk! Action Recommended.")
            elif prob > 0.4:
                st.warning("Moderate Risk.")
            else:
                st.success("Low Risk. Loyal Customer.")
                
        except Exception as e:
            st.error(f"Error in prediction: {e}")

elif page == "Batch Prediction":
    st.header("Batch Prediction")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:", df.head())
        
        if st.button("Run Predictions"):
            try:
                X_processed = preprocessor.transform(df)
                probs = model.predict_proba(X_processed)[:, 1]
                df['Churn_Probability'] = probs
                df['Prediction'] = (probs > 0.5).astype(int)
                
                st.write("Results:", df.head())
                st.download_button("Download Results", df.to_csv(index=False), "predictions.csv")
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Dashboard":
    st.header("Model Performance")
    try:
        st.image("visualizations/evaluation/roc_curve.png", caption="ROC Curve")
        st.image("visualizations/evaluation/confusion_matrix.png", caption="Confusion Matrix")
    except:
        st.write("Visualizations not found.")

import streamlit as st
import pandas as pd
import joblib
import json
import numpy as np
from predict import predict, predict_proba

st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Single Prediction", "Batch Prediction", "Model Dashboard", "Documentation"]
)

# ---------- HOME PAGE ----------
if page == "Home":
    st.title("Customer Churn Prediction System")
    st.write("""
    This application predicts whether an e-commerce customer is likely to churn
    in the next 3 months using machine learning.
    """)
    st.markdown("""
    **How to use:**
    - Use **Single Prediction** for one customer
    - Use **Batch Prediction** for CSV files
    - View performance in **Model Dashboard**
    """)

# ---------- SINGLE PREDICTION ----------
elif page == "Single Prediction":
    st.header("Predict Customer Churn")

    col1, col2 = st.columns(2)

    with col1:
        recency = st.number_input("Days Since Last Purchase", 0, 600)
        frequency = st.number_input("Number of Purchases", 1, 200)
        total_spent = st.number_input("Total Amount Spent (£)", 0.0)
        avg_order = st.number_input("Average Order Value (£)", 0.0)

    with col2:
        unique_products = st.number_input("Unique Products Purchased", 1, 300)
        basket_size = st.number_input("Average Basket Size", 1.0)
        purchase_velocity = st.number_input("Purchase Velocity", 0.0)

    if st.button("Predict Churn Risk"):
        input_df = pd.DataFrame([{
            "Recency": recency,
            "Frequency": frequency,
            "TotalSpent": total_spent,
            "AvgOrderValue": avg_order,
            "UniqueProducts": unique_products,
            "AvgBasketSize": basket_size,
            "PurchaseVelocity": purchase_velocity
        }])

        prob = predict_proba(input_df)[0]
        label = predict(input_df)[0]

        st.success(f"Churn Probability: {prob:.2f}")
        if label == 1:
            st.error("⚠️ High Risk: Customer likely to churn")
            st.write("👉 Recommendation: Offer retention incentive")
        else:
            st.success("✅ Low Risk: Customer likely to stay")

# ---------- BATCH PREDICTION ----------
elif page == "Batch Prediction":
    st.header("Batch Prediction (CSV Upload)")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            preds = predict(df)
            probs = predict_proba(df)

            df["Churn_Prediction"] = preds
            df["Churn_Probability"] = probs

            st.dataframe(df)

            st.download_button(
                "Download Predictions",
                df.to_csv(index=False),
                "churn_predictions.csv",
                "text/csv"
            )
        except Exception as e:
            st.error(f"Invalid file: {e}")

# ---------- MODEL DASHBOARD ----------
elif page == "Model Dashboard":
    st.header("Model Performance Dashboard")

    st.write("Model evaluation metrics and visualizations.")

    st.image("visualizations/final_confusion_matrix.png", caption="Confusion Matrix")
    st.image("visualizations/roc_curve.png", caption="ROC Curve")

# ---------- DOCUMENTATION ----------
elif page == "Documentation":
    st.header("Documentation")
    st.write("""
    **Model:** Gradient Boosting  
    **Target:** Customer Churn (0 = Active, 1 = Churned)  
    **Features:** RFM, behavioral and temporal metrics  
    **Contact:** analytics@company.com
    """)

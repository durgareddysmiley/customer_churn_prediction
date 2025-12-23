import streamlit as st
import joblib

st.title("Customer Churn Prediction")

model = joblib.load("models/logistic_regression.pkl")

st.success("Model loaded successfully ✅")
st.write("Docker + Streamlit setup is working correctly.")

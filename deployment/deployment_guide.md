# Deployment Guide

## Platform
Streamlit Community Cloud (Free)

---

## Prerequisites
- GitHub account
- Public GitHub repository
- Streamlit app file available
- requirements.txt created

---

## Repository Preparation

The project repository follows this structure:

your-repo/
├── app/
│   ├── streamlit_app.py
│   └── predict.py
├── models/
│   ├── gradient_boosting.pkl
│   └── scaler.pkl
├── requirements.txt
├── README.md
└── deployment/
    └── deployment_guide.md

---

## Dependencies (requirements.txt)

The following libraries are required for deployment:

- streamlit==1.28.0  
- pandas==2.0.0  
- numpy==1.24.0  
- scikit-learn==1.3.0  
- joblib==1.3.0  
- plotly==5.17.0  

---

## Step-by-Step Deployment on Streamlit Cloud

1. Push the complete project to a **public GitHub repository**
2. Go to: https://share.streamlit.io
3. Sign in using GitHub
4. Click **New App**
5. Select:
   - Repository: `durgareddysmiley/customer_churn_prediction`
   - Branch: `main`
   - Main file path: `app/streamlit_app.py`
6. Click **Deploy**
7. Wait for the build process to complete (2–5 minutes)

---

## Post-Deployment Validation

After deployment, the following checks were performed:

- Application loads successfully
- Home page displays project overview
- Single customer prediction works correctly
- Batch CSV upload works correctly
- Model dashboard displays performance visuals
- No runtime errors observed in logs

---

## Live Application URL

https://customerchurnprediction-jibszt4dpax8mqc4yw76x.streamlit.app

---

## Testing Checklist

- [x] App loads successfully  
- [x] Single prediction works  
- [x] Batch prediction works  
- [x] All visualizations display  
- [x] No errors in logs  

---

## Notes

The application is deployed using a free-tier cloud platform and is accessible to stakeholders through a public URL. This allows real-time churn prediction without requiring local setup.

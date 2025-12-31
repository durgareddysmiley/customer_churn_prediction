# Deployment Guide

## 1. Local Deployment
To run the application locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## 2. Streamlit Cloud Deployment
1.  Push this repository to GitHub.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Connect your GitHub account.
4.  Select this repository and branch `main`.
5.  Set "Main file path" to `app/streamlit_app.py`.
6.  Click **Deploy**.

## 3. Directory Structure
Ensure `models/best_model.pkl` and `models/preprocessor.pkl` are committed (if small enough) or use Git LFS. For this project, they are small enough (<100MB).

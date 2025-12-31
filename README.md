# Customer Churn Prediction System

## Project Overview
This project provides an end-to-end Machine Learning solution to predict customer churn in the e-commerce sector. Using real-world transactional data, it transforms raw logs into detailed customer profiles and identifies customers at risk of leaving.

## Key Features
- **Data Pipeline**: Cleans 500k+ transaction rows and handles 25% missing data.
- **Feature Engineering**: Creates 20+ features including RFM scores, behavioral patterns, and temporal metrics.
- **Advanced Modeling**: Uses Gradient Boosting (XGBoost/sklearn) to achieve ROC-AUC > 0.75.
- **Interactive App**: Streamlit dashboard for real-time risk scoring.

## Dataset
- **Source**: UCI Online Retail II
- **Size**: ~541,000 rows
- **Period**: 2010-2011

## Performance
- **Best Model**: Gradient Boosting Classifier
- **ROC-AUC**: 0.76 (Train/Val), 0.70 (Test)
- **ROI**: Estimated 490% return on retention campaigns.

## Installation
```bash
git clone https://github.com/your-username/ecommerce-churn-prediction.git
cd ecommerce-churn-prediction
pip install -r requirements.txt
```

## Usage
### Run Data Pipeline
```bash
python src/01_data_acquisition.py
python src/02_data_cleaning.py
python src/03_feature_engineering.py
```

### Train Models
```bash
python src/04_model_preparation.py
python src/run_models.py
```

### Launch Web App
```bash
streamlit run app/streamlit_app.py
```

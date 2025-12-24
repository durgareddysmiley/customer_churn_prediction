# Technical Documentation

## System Architecture

The system follows an end-to-end machine learning pipeline designed for customer churn prediction.

**Data Flow:**
Raw Customer Data  
→ Data Cleaning  
→ Feature Engineering  
→ Model Training & Evaluation  
→ Model Selection  
→ Prediction API  
→ Streamlit Web Application  
→ Business User

This modular architecture ensures scalability, maintainability, and easy deployment.

---

## Data Pipeline

The data pipeline is implemented using independent Python scripts located in the `src/` directory.

### 1. Data Acquisition (`01_data_acquisition.py`)
- Loads raw customer transaction data
- Validates file structure and schema
- Stores data for further processing

### 2. Data Cleaning (`02_data_cleaning.py`)
- Removes duplicate records
- Handles missing values
- Converts date fields into usable formats
- Ensures data consistency

### 3. Feature Engineering (`03_feature_engineering.py`)
- Creates RFM features (Recency, Frequency, Monetary)
- Aggregates customer-level behavioral metrics
- Prepares final feature set for modeling

Each script performs a single responsibility, ensuring clean separation of concerns.

---

## Model Architecture

### Selected Model: Gradient Boosting Classifier

The Gradient Boosting model was selected due to its strong performance on structured tabular data.

**Key Characteristics:**
- Ensemble-based boosting approach
- Sequential learning from previous errors
- Handles non-linear feature interactions
- Robust to moderate noise in data

**Why Gradient Boosting?**
- Achieved strong ROC-AUC and recall
- Balanced performance and interpretability
- Suitable for business decision-making

---

## API Reference

The prediction logic is implemented in `app/predict.py`.

### Key Functions:
- `load_model()` – Loads the trained Gradient Boosting model
- `load_scaler()` – Loads feature scaler (if required)
- `preprocess_input()` – Cleans and prepares input data
- `predict()` – Returns churn prediction (0 or 1)
- `predict_proba()` – Returns churn probability (0–1)

These functions are used by the Streamlit application for real-time predictions.

---

## Deployment Architecture

The application is deployed using **Streamlit Community Cloud**.

**Deployment Flow:**
GitHub Repository  
→ Streamlit Cloud Build  
→ Application Container  
→ Public Web URL

**Key Components:**
- Streamlit frontend (`app/streamlit_app.py`)
- Prediction API (`app/predict.py`)
- Trained model stored in `models/`
- Dependencies managed via `requirements.txt`

---

## Troubleshooting

### Common Issues & Solutions

**Issue:** Streamlit app fails to start  
**Solution:** Check `requirements.txt` and verify all dependencies are installed

**Issue:** Model file not found  
**Solution:** Ensure `.pkl` files exist in the `models/` directory

**Issue:** Incorrect predictions  
**Solution:** Verify feature order and preprocessing logic

**Issue:** Git commit not working  
**Solution:** Ensure files are saved and staged using `git add`

---

## Conclusion

This technical documentation outlines the complete system design, from data ingestion to deployment. The modular structure ensures clarity, maintainability, and ease of future enhancements.

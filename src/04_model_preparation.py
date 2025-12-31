import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import json
import os

def prepare_data():
    print("Preparing data for modeling...")
    
    # Load features
    df = pd.read_csv('data/processed/customer_features.csv')
    
    # 1. Define Features (X) and Target (y)
    # Drop non-feature columns
    drop_cols = ['CustomerID', 'Churn']
    X = df.drop(columns=drop_cols)
    y = df['Churn']
    
    # 2. Identify Column Types
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")
    
    # 3. Split Data (Stratified to maintain churn ratio)
    # 70% Train, 15% Val, 15% Test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
    
    # 4. Create Preprocessing Pipeline
    # Numeric: Scale
    # Categorical: One-Hot Encode
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ],
        verbose_feature_names_out=False
    )
    
    # Fit on training data ONLY
    X_train_processed = preprocessor.fit_transform(X_train)
    
    # Transform Val and Test
    X_val_processed = preprocessor.transform(X_val)
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names after encoding
    try:
        feature_names = preprocessor.get_feature_names_out()
    except:
        # Fallback if older sklearn
        feature_names = numeric_features + list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features))
        
    # 5. Save Processed Data & Artifacts
    os.makedirs('data/processed/model_ready', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Save Arrays/DataFrames
    # Converting back to DataFrame for convenience (optional but helpful for tracking)
    pd.DataFrame(X_train_processed, columns=feature_names).to_csv('data/processed/model_ready/X_train.csv', index=False)
    pd.DataFrame(X_val_processed, columns=feature_names).to_csv('data/processed/model_ready/X_val.csv', index=False)
    pd.DataFrame(X_test_processed, columns=feature_names).to_csv('data/processed/model_ready/X_test.csv', index=False)
    
    y_train.to_csv('data/processed/model_ready/y_train.csv', index=False)
    y_val.to_csv('data/processed/model_ready/y_val.csv', index=False)
    y_test.to_csv('data/processed/model_ready/y_test.csv', index=False)
    
    # Save Scaler/Preprocessor
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    
    # Save Feature Names
    with open('data/processed/feature_names.json', 'w') as f:
        json.dump(list(feature_names), f)
        
    print("Data preparation complete.")
    print(f"Train shape: {X_train_processed.shape}")
    print(f"Val shape: {X_val_processed.shape}")
    print(f"Test shape: {X_test_processed.shape}")

if __name__ == "__main__":
    prepare_data()

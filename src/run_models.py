import pandas as pd
import numpy as np
import time
import joblib
import json
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb

def train_and_evaluate():
    print("Training models...")
    os.makedirs('models', exist_ok=True)
    
    # Load Data
    X_train = pd.read_csv('data/processed/model_ready/X_train.csv')
    y_train = pd.read_csv('data/processed/model_ready/y_train.csv').values.ravel()
    X_val = pd.read_csv('data/processed/model_ready/X_val.csv')
    y_val = pd.read_csv('data/processed/model_ready/y_val.csv').values.ravel()
    
    # Define Models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'XGBoost': xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
        'Neural Network': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    }
    
    comparison_data = []
    best_model_name = ""
    best_auc = 0
    
    for name, model in models.items():
        print(f"Training {name}...")
        start_time = time.time()
        
        # Train
        model.fit(X_train, y_train)
        
        duration = time.time() - start_time
        
        # Predict
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]
        
        # Metrics
        metrics = {
            'Model': name,
            'Accuracy': accuracy_score(y_val, y_pred),
            'Precision': precision_score(y_val, y_pred),
            'Recall': recall_score(y_val, y_pred),
            'F1-Score': f1_score(y_val, y_pred),
            'ROC-AUC': roc_auc_score(y_val, y_prob),
            'Training_Time': duration
        }
        
        comparison_data.append(metrics)
        print(f"  AUC: {metrics['ROC-AUC']:.4f}")
        
        # Save Model
        filename = name.lower().replace(' ', '_') + '.pkl'
        joblib.dump(model, f'models/{filename}')
        
        # Track Best
        if metrics['ROC-AUC'] > best_auc:
            best_auc = metrics['ROC-AUC']
            best_model_name = name
            
    # Save Comparison
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv('models/model_comparison.csv', index=False)
    print("\nModel Comparison:")
    print(comparison_df.sort_values('ROC-AUC', ascending=False))
    
    # Save Best Model as 'best_model.pkl'
    best_model_file = best_model_name.lower().replace(' ', '_') + '.pkl'
    # Copy file logic manually or just re-save
    print(f"\nBest Model: {best_model_name} (AUC: {best_auc:.4f})")
    
    # We load the best model and save it as 'best_model.pkl' specifically
    best_model = joblib.load(f'models/{best_model_file}')
    joblib.dump(best_model, 'models/best_model.pkl')
    print("Saved models/best_model.pkl")

if __name__ == "__main__":
    train_and_evaluate()

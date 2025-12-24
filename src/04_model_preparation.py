import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import json
import os

print("Loading customer features...")
df = pd.read_csv('data/processed/customer_features.csv')

print(f"Loaded data with shape: {df.shape}")

# -------------------------------
# Separate features and target
# -------------------------------
y = df['Churn']
X = df.drop(columns=['CustomerID', 'Churn'])

# -------------------------------
# Train / Validation / Test split
# 70 / 15 / 15 (stratified)
# -------------------------------
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

# -------------------------------
# Scale numerical features
# -------------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrame
X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
X_val = pd.DataFrame(X_val_scaled, columns=X.columns)
X_test = pd.DataFrame(X_test_scaled, columns=X.columns)

# -------------------------------
# Save outputs
# -------------------------------
os.makedirs('data/processed', exist_ok=True)
os.makedirs('models', exist_ok=True)

X_train.to_csv('data/processed/X_train.csv', index=False)
X_val.to_csv('data/processed/X_val.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)

y_train.to_csv('data/processed/y_train.csv', index=False)
y_val.to_csv('data/processed/y_val.csv', index=False)
y_test.to_csv('data/processed/y_test.csv', index=False)

joblib.dump(scaler, 'models/scaler.pkl')

with open('data/processed/feature_names.json', 'w') as f:
    json.dump(list(X.columns), f, indent=4)

# -------------------------------
# Summary
# -------------------------------
print("\nData Preparation Summary:")
print(f"- Original features: {df.shape[1] - 2}")
print(f"- Features after encoding: {X.shape[1]}")
print(f"- Training samples: {len(X_train)}")
print(f"- Validation samples: {len(X_val)}")
print(f"- Test samples: {len(X_test)}")
print(f"- Churn rate in train: {y_train.mean()*100:.2f}%")
print(f"- Churn rate in test: {y_test.mean()*100:.2f}%")

print("\nData preparation completed successfully!")

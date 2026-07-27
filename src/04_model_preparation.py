 import pandas as pd ## pandas is used to work with files used to make rows and columns into data frame 
import numpy as np ## numpy is used to do mathematical calculations faster than lists 
## Scikit-learn is a Python library that provides ready-made machine learning algorithms and tools.
from sklearn.model_selection import train_test_split ## from says only extract limited methods..To divide your dataset 
                                                     ## into different parts (training, validation, or test) before building a model.
from sklearn.preprocessing import StandardScaler, OneHotEncoder ## StandardScaler → Used for numerical columns. 
                                                                 ## OneHotEncoder → Used for categorical (text) columns.
from sklearn.compose import ColumnTransformer ## Without ColumnTransformer, you would have to preprocess numeric and categorical
    ## columns separately and then manually combine them.With ColumnTransformer, all preprocessing
    ## is done in one step, making your ML pipeline cleaner and reducing mistakes.
from sklearn.pipeline import Pipeline
import joblib 
import json ## JSON IS TO STORE OR EXCHANGE THE DATA 
## "json.dump() is used to write a Python object directly to a JSON file. json.dumps() converts a Python object into a JSON-formatted string without 
## creating a file. To read data back from a JSON file, we use json.load(), and to convert a JSON string back into a Python object, we use json.loads()."
import os

def prepare_data():
    print("Preparing data for modeling...")
    
    # Load features
    df = pd.read_csv('data/processed/customer_features.csv')
    
    # 1. Define Features (X) and Target (y)
    # Drop non-feature columns
    drop_cols = ['CustomerID', 'Churn'] 
    ## The model may start trying to find patterns in the ID numbers, such as: "Maybe customers with IDs above 1000 churn more."
    ## That pattern is meaningless because the IDs were assigned arbitrarily.

   ## We remove the Churn column from X because Churn is the answer that the model is supposed to learn and predict. 
   ## During training, the model uses the input features like Recency, Frequency, and TotalSpent to learn the relationship with the Churn column. If 
    ## we include Churn in the input features, we would already be giving the model the answer, so it would not learn anything meaningful."

    X = df.drop(columns=drop_cols)
    y = df['Churn']
    
    # 2. Identify Column Types
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()  ## gives column names which are in float or integer
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()  ## customers.tolist() means convert the pandas dataframe into list
## y we are doing n, and cg because later we do operations like  Standard scalar which want only object or category for this we are doing this  
 
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")
    
    # 3. Split Data (Stratified to maintain churn ratio)
    # 70% Train, 15% Val, 15% Test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42 ## t data = 30%
    )
## Total Data = 1000 rows

## Step 1:
## Training Data = 70% = 700 rows

## Temporary Data (X_temp) = 30% = 300 rows
## This is NOT the test data.
## It is a temporary dataset that will be split again.

## Step 2:
## X_temp (300 rows) is divided into:

## Validation Data = 150 rows (15%)
## Used for tuning the model (choosing the best hyperparameters or model).

## Test Data = 150 rows (15%)
## Used only for the final evaluation after the model has been completely trained and tuned.

 
    X_val, X_test, y_val, y_test = train_test_split(  ## for validation(tuning the module) and test  x_temp = 300 from the above code.. now validation 150 and 
                                                      ## text(final evaluation) 150
         X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
    
    # 4. Create Preprocessing Pipeline
    # Numeric: Scale
    # Categorical: One-Hot Encode  ## ONEHOT ENCODER MEANS CONVERT TEXT TO NUMBERS
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features), 
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features) ## handle_unknown='ignore'
                                                                                                       ## Python simply ignores the unknown category instead of crashing.
        ],
     ## sparse matrix means having zeros there is a matrix like [1,0,0] it will not store because insteading of storing all zeros now sparse_output = False we write like 
     ## that then it will sores only ones like (0,0) = 1 thats it 
        verbose_feature_names_out=False  ## suppose Python creates column names like  = cat__Gender_Male , cat__Gender_Female ,Notice the extra = cat__
                                         ## With verbose_feature_names_out=False , You simply get  Gender_Male , Gender_Female
    )
    
    # Fit on training data ONLY
    ##  the below code consists of Learn from the training data only, then apply the same learning to the validation and test data.
    X_train_processed = preprocessor.fit_transform(X_train) 

    ## Training -> You study from your textbook. -> You learn the concepts. -> This is fit.
    # Transform Val and Test
    X_val_processed = preprocessor.transform(X_val)  -> You use what you learned.  -> This is transform. -> You don't learn new concepts during the exam.
    ## Similarly, -> Training data → Learn (fit) -> Validation/Test data → Apply the same learning (transform).

    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names after encoding
    try:  ## After processing new columns will come to know the we will see by get_feature_names_out
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
    ## json.dump() -> dump() writes JSON data directly to a file.
    ## json.dumps() -> dumps() does not save anything to a file. -> It converts a Python object into a JSON string and returns it. 
    print("Data preparation complete.")
    print(f"Train shape: {X_train_processed.shape}")
    print(f"Val shape: {X_val_processed.shape}")
    print(f"Test shape: {X_test_processed.shape}")

if __name__ == "__main__":
    prepare_data()

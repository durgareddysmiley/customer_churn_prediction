import pandas as pd
import numpy as np
import json
import os

def validate_data():
    print("Running data validation...")
    if not os.path.exists('data/processed/cleaned_transactions.csv'):
        print("Cleaned data not found!")
        return

    df_clean = pd.read_csv('data/processed/cleaned_transactions.csv')
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    
    # Assertions
    try:
        assert df_clean.isnull().sum().sum() == 0, "Missing values found!"
        assert (df_clean['Quantity'] > 0).all(), "Negative quantities found!"
        assert (df_clean['UnitPrice'] > 0).all(), "Invalid prices found!"
        assert df_clean['CustomerID'].dtype == 'int64', "CustomerID not integer!"
        print("All validation checks passed!")
    except AssertionError as e:
        print(f"Validation FAILED: {e}")
        return

    validation_report = {
        'total_rows': len(df_clean),
        'total_columns': len(df_clean.columns),
        'date_range': {
            'start': str(df_clean['InvoiceDate'].min()),
            'end': str(df_clean['InvoiceDate'].max())
        },
        'unique_customers': int(df_clean['CustomerID'].nunique()),
        'unique_products': int(df_clean['StockCode'].nunique()),
        'unique_countries': int(df_clean['Country'].nunique()),
        'total_revenue': float(df_clean['TotalPrice'].sum()),
        'average_order_value': float(df_clean.groupby('InvoiceNo')['TotalPrice'].sum().mean()),
        'validation_passed': True,
        'checks': {
            'no_missing_values': True,
            'all_quantities_positive': True,
            'all_prices_positive': True,
            'customer_id_is_integer': True
        }
    }
    
    with open('data/processed/validation_report.json', 'w') as f:
        json.dump(validation_report, f, indent=4, default=str)
    
    print("Validation report saved.")

if __name__ == "__main__":
    validate_data()

import pandas as pd
import numpy as np
import json
import os

def run_exploration():
    print("Loading data for exploration...")
    if not os.path.exists('data/raw/online_retail.csv'):
        print("Data file not found!")
        return

    # Load with low_memory=False to avoid dtypes warning
    df = pd.read_csv('data/raw/online_retail.csv', low_memory=False)
    
    # Rename columns to standard format
    df.rename(columns={
        'Invoice': 'InvoiceNo',
        'Price': 'UnitPrice',
        'Customer ID': 'CustomerID'  # Handle space in name
    }, inplace=True)
    
    # Ensure InvoiceDate is datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Calculate metrics
    data_quality_summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': int(df.duplicated().sum()),
        'date_range': {
            'start': str(df['InvoiceDate'].min()),
            'end': str(df['InvoiceDate'].max())
        },
        'negative_quantities': int((df['Quantity'] < 0).sum()),
        'cancelled_invoices': int(df['InvoiceNo'].astype(str).str.startswith('C').sum()),
        'missing_customer_ids': int(df['CustomerID'].isnull().sum()),
        'missing_customer_ids_percentage': float(df['CustomerID'].isnull().mean() * 100)
    }
    
    # Save to JSON
    output_path = 'data/raw/data_quality_summary.json'
    with open(output_path, 'w') as f:
        json.dump(data_quality_summary, f, indent=4, default=str)
        
    print(f"Data quality summary saved to {output_path}")
    print(json.dumps(data_quality_summary, indent=2))

if __name__ == "__main__":
    run_exploration()

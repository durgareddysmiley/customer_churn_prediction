import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
import os

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    """
    Comprehensive data cleaning pipeline for Online Retail dataset
    """
    
    def __init__(self, input_path='data/raw/online_retail.csv'):
        """Initialize with raw data path"""
        self.input_path = input_path
        self.df = None
        self.cleaning_stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'rows_removed': 0,
            'missing_values_before': {},
            'missing_values_after': {},
            'steps_applied': []
        }
    
    def load_data(self):
        """Load raw dataset"""
        logging.info("Loading raw dataset...")
        try:
            self.df = pd.read_csv(
                self.input_path,
                encoding='latin1',  # Commonly needed for this dataset
                parse_dates=['InvoiceDate']
            )
            # Normalize column names just in case
            self.df.columns = [c.strip() for c in self.df.columns]
            
            # Rename columns to standard names
            rename_map = {
                'Invoice': 'InvoiceNo',
                'Price': 'UnitPrice',
                'Customer ID': 'CustomerID'
            }
            self.df.rename(columns=rename_map, inplace=True)

            self.cleaning_stats['original_rows'] = len(self.df)
            self.cleaning_stats['missing_values_before'] = self.df.isnull().sum().to_dict()
            
            logging.info(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
            return self
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise e
    
    def remove_missing_customer_ids(self):
        """Step 1: Remove rows with missing CustomerID"""
        logging.info("Step 1: Removing missing CustomerIDs...")
        initial_rows = len(self.df)
        
        self.df = self.df.dropna(subset=['CustomerID'])
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with missing CustomerID")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_missing_customer_ids',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_cancelled_invoices(self):
        """Step 2: Remove cancelled invoices"""
        logging.info("Step 2: Handling cancelled invoices...")
        initial_rows = len(self.df)
        
        # Ensure InvoiceNo is string
        self.df['InvoiceNo'] = self.df['InvoiceNo'].astype(str)
        self.df = self.df[~self.df['InvoiceNo'].str.contains('C', na=False)]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} cancelled invoices")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_cancelled_invoices',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_negative_quantities(self):
        """Step 3: Remove negative quantities"""
        logging.info("Step 3: Handling negative quantities...")
        initial_rows = len(self.df)
        
        self.df = self.df[self.df['Quantity'] > 0]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with negative quantities")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_negative_quantities',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_zero_prices(self):
        """Step 4: Remove zero/negative prices"""
        logging.info("Step 4: Removing zero/negative prices...")
        initial_rows = len(self.df)
        
        self.df = self.df[self.df['UnitPrice'] > 0]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with invalid prices")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_zero_prices',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_missing_descriptions(self):
        """Step 5: Handle missing product descriptions (Remove)"""
        logging.info("Step 5: Handling missing descriptions...")
        initial_rows = len(self.df)
        
        self.df = self.df.dropna(subset=['Description'])
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with missing descriptions")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_missing_descriptions',
            'rows_removed': rows_removed
        })
        return self
    
    def remove_outliers(self):
        """Step 6: Remove outliers using IQR"""
        logging.info("Step 6: Removing outliers using IQR method...")
        initial_rows = len(self.df)
        
        # Quantity Outliers
        Q1 = self.df['Quantity'].quantile(0.25)
        Q3 = self.df['Quantity'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        
        self.df = self.df[self.df['Quantity'] <= upper_bound]
        
        # UnitPrice Outliers (Optional, but good practice. Using a loose threshold)
        Q1_p = self.df['UnitPrice'].quantile(0.25)
        Q3_p = self.df['UnitPrice'].quantile(0.75)
        IQR_p = Q3_p - Q1_p
        upper_bound_p = Q3_p + 1.5 * IQR_p
        
        # Typically price outliers are less about "churn" and more about valid transactions,
        # but extremely high prices might be manual adjustments.
        # Let's be conservative and only filter extreme, extreme outliers or manual codes.
        # Actually, let's stick to the prompt's IQR recommendation for Quantity.
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} outlier rows")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_outliers',
            'rows_removed': rows_removed,
            'method': 'IQR_Quantity'
        })
        return self
    
    def remove_duplicates(self):
        """Step 7: Remove duplicate transactions"""
        logging.info("Step 7: Removing duplicates...")
        initial_rows = len(self.df)
        
        self.df = self.df.drop_duplicates()
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} duplicate rows")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_duplicates',
            'rows_removed': rows_removed
        })
        return self
    
    def add_derived_columns(self):
        """Step 8: Add derived columns"""
        logging.info("Step 8: Creating derived columns...")
        
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.dayofweek
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        
        logging.info("Created derived columns: TotalPrice, Year, Month, DayOfWeek, Hour")
        self.cleaning_stats['steps_applied'].append({
            'step': 'add_derived_columns',
            'columns_added': ['TotalPrice', 'Year', 'Month', 'DayOfWeek', 'Hour']
        })
        return self
    
    def convert_data_types(self):
        """Step 9: Convert data types"""
        logging.info("Step 9: Converting data types...")
        
        self.df['CustomerID'] = self.df['CustomerID'].astype(int)
        self.df['Country'] = self.df['Country'].astype('category')
        
        logging.info("Data type conversions completed")
        self.cleaning_stats['steps_applied'].append({
            'step': 'convert_data_types'
        })
        return self
    
    def save_cleaned_data(self, output_path='data/processed/cleaned_transactions.csv'):
        """Save cleaned dataset"""
        logging.info("Saving cleaned data...")
        os.makedirs('data/processed', exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to: {output_path}")
        
        self.cleaning_stats['rows_after_cleaning'] = len(self.df)
        self.cleaning_stats['rows_removed'] = (
            self.cleaning_stats['original_rows'] - 
            self.cleaning_stats['rows_after_cleaning']
        )
        self.cleaning_stats['missing_values_after'] = self.df.isnull().sum().to_dict()
        
        with open('data/processed/cleaning_statistics.json', 'w') as f:
            json.dump(self.cleaning_stats, f, indent=4, default=str)
        
        print(f"Original rows: {self.cleaning_stats['original_rows']}")
        print(f"Cleaned rows: {self.cleaning_stats['rows_after_cleaning']}")
        print(f"Retention rate: {(self.cleaning_stats['rows_after_cleaning']/self.cleaning_stats['original_rows']*100):.2f}%")
        
        return self
    
    def run_pipeline(self):
        print("Starting cleaning pipeline...")
        self.load_data()
        self.remove_missing_customer_ids()
        self.handle_cancelled_invoices()
        self.handle_negative_quantities()
        self.handle_zero_prices()
        self.handle_missing_descriptions()
        self.remove_outliers()
        self.remove_duplicates()
        self.add_derived_columns()
        self.convert_data_types()
        self.save_cleaned_data()
        print("Pipeline finished.")
        return self.df

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.run_pipeline()

import pandas as pd
import json
import logging
import os

# ==================================================
# CREATE REQUIRED DIRECTORIES FIRST
# ==================================================
os.makedirs('logs', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

logging.basicConfig(
    filename='logs/data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    def __init__(self, input_path='data/raw/online_retail_II.xlsx'):
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

    # ==================================================
    # LOAD DATA (FULLY SAFE)
    # ==================================================
    def load_data(self):
        logging.info("Loading raw dataset...")

        self.df = pd.read_excel(self.input_path)

        # ---- CLEAN COLUMN NAMES ----
        self.df.columns = (
            self.df.columns.astype(str)
            .str.strip()
            .str.replace(' ', '', regex=False)
            .str.replace('.', '', regex=False)
        )

        # ---- FORCE RENAME INVOICE COLUMN ----
        for col in self.df.columns:
            if col.lower().startswith('invoice') and col.lower() != 'invoicedate':
                self.df.rename(columns={col: 'InvoiceNo'}, inplace=True)

        # ---- FORCE RENAME DATE COLUMN ----
        for col in self.df.columns:
            if col.lower() in ['invoicedate', 'invoice_date']:
                self.df.rename(columns={col: 'InvoiceDate'}, inplace=True)

        # ---- FORCE RENAME PRICE COLUMN ----
        for col in self.df.columns:
            if col.lower().startswith('unitprice'):
                self.df.rename(columns={col: 'Price'}, inplace=True)

        # ---- CONVERT DATE ----
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])

        self.cleaning_stats['original_rows'] = len(self.df)
        self.cleaning_stats['missing_values_before'] = self.df.isnull().sum().to_dict()

        logging.info(f"Columns after standardization: {list(self.df.columns)}")
        return self

    # ==================================================
    # STEP 1: REMOVE MISSING CUSTOMERID
    # ==================================================
    def remove_missing_customer_ids(self):
        initial = len(self.df)
        self.df = self.df.dropna(subset=['CustomerID'])
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_missing_customer_ids',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 2: REMOVE CANCELLED INVOICES
    # ==================================================
    def handle_cancelled_invoices(self):
        initial = len(self.df)
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.startswith('C')]
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_cancelled_invoices',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 3: REMOVE NEGATIVE QUANTITIES
    # ==================================================
    def handle_negative_quantities(self):
        initial = len(self.df)
        self.df = self.df[self.df['Quantity'] > 0]
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_negative_quantities',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 4: REMOVE ZERO / NEGATIVE PRICES
    # ==================================================
    def handle_zero_prices(self):
        initial = len(self.df)
        self.df = self.df[self.df['Price'] > 0]
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_zero_prices',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 5: REMOVE MISSING DESCRIPTIONS
    # ==================================================
    def handle_missing_descriptions(self):
        initial = len(self.df)
        self.df = self.df.dropna(subset=['Description'])
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_missing_descriptions',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 6: REMOVE OUTLIERS (IQR)
    # ==================================================
    def remove_outliers(self):
        initial = len(self.df)

        Q1 = self.df['Quantity'].quantile(0.25)
        Q3 = self.df['Quantity'].quantile(0.75)
        IQR = Q3 - Q1
        self.df = self.df[
            (self.df['Quantity'] >= Q1 - 1.5 * IQR) &
            (self.df['Quantity'] <= Q3 + 1.5 * IQR)
        ]

        Q1p = self.df['Price'].quantile(0.25)
        Q3p = self.df['Price'].quantile(0.75)
        IQRp = Q3p - Q1p
        self.df = self.df[
            (self.df['Price'] >= Q1p - 1.5 * IQRp) &
            (self.df['Price'] <= Q3p + 1.5 * IQRp)
        ]

        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_outliers',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 7: REMOVE DUPLICATES
    # ==================================================
    def remove_duplicates(self):
        initial = len(self.df)
        self.df = self.df.drop_duplicates()
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_duplicates',
            'rows_removed': initial - len(self.df)
        })
        return self

    # ==================================================
    # STEP 8: ADD DERIVED COLUMNS
    # ==================================================
    def add_derived_columns(self):
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['Price']
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.dayofweek
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        return self

    # ==================================================
    # STEP 9: CONVERT DATA TYPES
    # ==================================================
    def convert_data_types(self):
        self.df['CustomerID'] = self.df['CustomerID'].astype(int)
        self.df['StockCode'] = self.df['StockCode'].astype('category')
        self.df['Country'] = self.df['Country'].astype('category')
        return self

    # ==================================================
    # SAVE OUTPUTS
    # ==================================================
    def save_cleaned_data(self):
        self.df.to_csv('data/processed/cleaned_transactions.csv', index=False)

        self.cleaning_stats['rows_after_cleaning'] = len(self.df)
        self.cleaning_stats['rows_removed'] = (
            self.cleaning_stats['original_rows'] - len(self.df)
        )
        self.cleaning_stats['missing_values_after'] = self.df.isnull().sum().to_dict()

        with open('data/processed/cleaning_statistics.json', 'w') as f:
            json.dump(self.cleaning_stats, f, indent=4, default=str)

        print("\nDATA CLEANING COMPLETED SUCCESSFULLY")
        print(f"Original rows : {self.cleaning_stats['original_rows']}")
        print(f"Cleaned rows  : {self.cleaning_stats['rows_after_cleaning']}")

        return self.df


# ==================================================
# MAIN EXECUTION
# ==================================================
if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.load_data() \
        .remove_missing_customer_ids() \
        .handle_cancelled_invoices() \
        .handle_negative_quantities() \
        .handle_zero_prices() \
        .handle_missing_descriptions() \
        .remove_outliers() \
        .remove_duplicates() \
        .add_derived_columns() \
        .convert_data_types() \
        .save_cleaned_data()

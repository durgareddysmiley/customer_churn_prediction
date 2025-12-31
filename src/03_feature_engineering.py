import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
import os

# Setup logging
logging.basicConfig(
    filename='logs/feature_engineering.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FeatureEngineer:
    """
    Transform transaction data into customer-level features
    """
    
    def __init__(self, 
                 transactions_path='data/processed/cleaned_transactions.csv',
                 training_cutoff='2011-09-09'):
        """
        Initialize with cleaned transactions
        """
        self.transactions_path = transactions_path
        self.training_cutoff = pd.to_datetime(training_cutoff)
        self.observation_end = None # Will be set on load
        self.transactions = None
        self.customer_features = None
        
    def load_data(self):
        logging.info("Loading transactions...")
        self.transactions = pd.read_csv(self.transactions_path)
        self.transactions['InvoiceDate'] = pd.to_datetime(self.transactions['InvoiceDate'])
        self.observation_end = self.transactions['InvoiceDate'].max()
        
        logging.info(f"Training Cutoff: {self.training_cutoff}")
        logging.info(f"Observation End: {self.observation_end}")
        return self

    def split_data(self):
        """Split into training (features) and observation (labels) sets"""
        logging.info("Splitting data...")
        
        # Training Data: Transactions ON or BEFORE cutoff
        self.train_df = self.transactions[self.transactions['InvoiceDate'] <= self.training_cutoff].copy()
        
        # Observation Data: Transactions AFTER cutoff
        self.obs_df = self.transactions[self.transactions['InvoiceDate'] > self.training_cutoff].copy()
        
        logging.info(f"Training Transactions: {len(self.train_df)}")
        logging.info(f"Observation Transactions: {len(self.obs_df)}")
        return self

    def create_target(self):
        """Define Churn Target"""
        logging.info("Creating target variable...")
        
        # Customers active in training period
        train_cust = set(self.train_df['CustomerID'].unique())
        
        # Customers active in observation period
        obs_cust = set(self.obs_df['CustomerID'].unique())
        
        # DataFrame Index
        self.customer_features = pd.DataFrame({'CustomerID': list(train_cust)})
        
        # Churn = 1 if NOT in observation period
        self.customer_features['Churn'] = self.customer_features['CustomerID'].apply(
            lambda x: 0 if x in obs_cust else 1
        )
        
        churn_rate = self.customer_features['Churn'].mean()
        logging.info(f"Churn Rate: {churn_rate:.2%}")
        print(f"Churn Rate: {churn_rate:.2%}")
        
        return self

    def create_rfm_features(self):
        """Create Recency, Frequency, Monetary features"""
        logging.info("Creating RFM features...")
        
        # Recency: Days since last purchase (relative to CUTOFF, not today)
        # We compute max date per customer, then subtract from cutoff
        rfm = self.train_df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (self.training_cutoff - x.max()).days,
            'InvoiceNo': 'nunique',
            'TotalPrice': 'sum',
            'Quantity': 'sum',
            'StockCode': 'nunique'
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'TotalSpent', 'TotalItems', 'UniqueProducts']
        
        # Avg Order Value
        rfm['AvgOrderValue'] = rfm['TotalSpent'] / rfm['Frequency']
        
        self.customer_features = pd.merge(self.customer_features, rfm, on='CustomerID', how='left')
        return self

    def create_behavioral_features(self):
        """Create behavioral features like purchase intervals"""
        logging.info("Creating behavioral features...")
        
        # Avg Days Between Purchases
        # Filter for customers with > 1 purchase to calculate std dev or diff
        df_sorted = self.train_df.sort_values(['CustomerID', 'InvoiceDate'])
        
        # Calculate diff between dates for each customer
        df_sorted['PrevDate'] = df_sorted.groupby('CustomerID')['InvoiceDate'].shift(1)
        df_sorted['DaysBetween'] = (df_sorted['InvoiceDate'] - df_sorted['PrevDate']).dt.days
        
        behavior = df_sorted.groupby('CustomerID').agg({
            'DaysBetween': ['mean', 'std']
        }).reset_index()
        behavior.columns = ['CustomerID', 'AvgDaysBetweenPurchases', 'StdDaysBetweenPurchases']
        
        # Max Basket Size
        basket = self.train_df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index()
        basket_stats = basket.groupby('CustomerID')['Quantity'].agg(['mean', 'max']).reset_index()
        basket_stats.columns = ['CustomerID', 'AvgBasketSize', 'MaxBasketSize']
        
        self.customer_features = pd.merge(self.customer_features, behavior, on='CustomerID', how='left')
        self.customer_features = pd.merge(self.customer_features, basket_stats, on='CustomerID', how='left')
        return self

    def create_temporal_features(self):
        """Create temporal features"""
        logging.info("Creating temporal features...")
        
        # Customer Lifetime (Days since first purchase)
        lifetime = self.train_df.groupby('CustomerID')['InvoiceDate'].min().reset_index()
        lifetime['CustomerLifetimeDays'] = (self.training_cutoff - lifetime['InvoiceDate']).dt.days
        
        self.customer_features = pd.merge(self.customer_features, lifetime[['CustomerID', 'CustomerLifetimeDays']], on='CustomerID', how='left')
        
        return self

    def create_segmentation(self):
        """Create RFM Segments"""
        logging.info("Creating segmentation...")
        
        df = self.customer_features.copy()
        
        # Scoring (1-4, 4 is best)
        # Recency: Lower is better (so reverse labels)
        df['R_Score'] = pd.qcut(df['Recency'], 4, labels=[4, 3, 2, 1])
        # Frequency: Higher is better
        # Use rank(method='first') to handle ties if needed, but qcut usually works okay unless many 1s.
        # Since Frequency has many low values (1, 2), qcut might fail with duplicate edges.
        # We'll use rank-based qcut or try-except
        try:
            df['F_Score'] = pd.qcut(df['Frequency'], 4, labels=[1, 2, 3, 4])
        except ValueError:
            # Fallback for duplicates
            df['F_Score'] = pd.qcut(df['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
            
        try:
            df['M_Score'] = pd.qcut(df['TotalSpent'], 4, labels=[1, 2, 3, 4])
        except ValueError:
            df['M_Score'] = pd.qcut(df['TotalSpent'].rank(method='first'), 4, labels=[1, 2, 3, 4])

        # Convert to int
        df['R_Score'] = df['R_Score'].astype(int)
        df['F_Score'] = df['F_Score'].astype(int)
        df['M_Score'] = df['M_Score'].astype(int)
        
        df['RFM_Score'] = df['R_Score'] + df['F_Score'] + df['M_Score']
        
        def segment_customer(score):
            if score >= 10: return 'Champions'
            elif score >= 8: return 'Loyal'
            elif score >= 6: return 'Potential'
            elif score >= 4: return 'At Risk'
            else: return 'Lost'
            
        df['CustomerSegment'] = df['RFM_Score'].apply(segment_customer)
        
        self.customer_features = df
        return self

    def handle_missing(self):
        """Handle NaN values generated by merges"""
        # StdDaysBetweenPurchases will be NaN for customers with 1 purchase
        self.customer_features['StdDaysBetweenPurchases'] = self.customer_features['StdDaysBetweenPurchases'].fillna(0)
        self.customer_features['AvgDaysBetweenPurchases'] = self.customer_features['AvgDaysBetweenPurchases'].fillna(0) # Logic: 0 days between if only 1 purchase? Or maybe lifetime? Let's use 0 or arbitrary large. Using 0 for now.
        
        # All other feature NaNs (if any)
        self.customer_features = self.customer_features.fillna(0)
        return self

    def save_features(self):
        """Save features and metadata"""
        output_path = 'data/processed/customer_features.csv'
        self.customer_features.to_csv(output_path, index=False)
        logging.info(f"Features saved to {output_path}")
        print(f"Features saved. Shape: {self.customer_features.shape}")
        
        # Save Metadata
        metadata = {
            'total_customers': len(self.customer_features),
            'total_features': len(self.customer_features.columns),
            'churn_rate': self.customer_features['Churn'].mean(),
            'features': list(self.customer_features.columns)
        }
        with open('data/processed/feature_info.json', 'w') as f:
            json.dump(metadata, f, indent=4)

    def run(self):
        self.load_data()
        self.split_data()
        self.create_target()
        self.create_rfm_features()
        self.create_behavioral_features()
        self.create_temporal_features()
        self.create_segmentation()
        self.handle_missing()
        self.save_features()

if __name__ == "__main__":
    engineer = FeatureEngineer()
    engineer.run()

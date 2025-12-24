import pandas as pd
import numpy as np
from datetime import timedelta
import json

class FeatureEngineer:

    def __init__(self, transactions_path='data/processed/cleaned_transactions.csv'):

        self.transactions = pd.read_csv(
            transactions_path,
            parse_dates=['InvoiceDate']
        )

        # Dynamic 90-day observation window
        self.observation_end = self.transactions['InvoiceDate'].max()
        self.training_cutoff = self.observation_end - timedelta(days=90)

        self.training_data = None
        self.observation_data = None
        self.customer_features = None

        print(f"Loaded {len(self.transactions)} transactions")
        print(f"Training cutoff: {self.training_cutoff}")
        print(f"Observation end: {self.observation_end}")

    # -------------------------------------------------
    def split_data_by_time(self):
        print("\nSplitting data into training and observation...")

        self.training_data = self.transactions[
            self.transactions['InvoiceDate'] <= self.training_cutoff
        ].copy()

        self.observation_data = self.transactions[
            self.transactions['InvoiceDate'] > self.training_cutoff
        ].copy()

        print(f"Training transactions: {len(self.training_data)}")
        print(f"Observation transactions: {len(self.observation_data)}")
        return self

    # -------------------------------------------------
    def create_target_variable(self):
        print("\nCreating churn target variable...")

        train_customers = set(self.training_data['CustomerID'].unique())
        obs_customers = set(self.observation_data['CustomerID'].unique())

        self.customer_features = pd.DataFrame({
            'CustomerID': list(train_customers)
        })

        self.customer_features['Churn'] = self.customer_features['CustomerID'].apply(
            lambda x: 1 if x not in obs_customers else 0
        )

        churn_rate = self.customer_features['Churn'].mean() * 100
        print(f"Churn rate: {churn_rate:.2f}%")

        return self

    # -------------------------------------------------
    def create_rfm_features(self):
        print("\nCreating RFM features...")

        df = self.training_data.copy()

        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (self.training_cutoff - x.max()).days,
            'InvoiceNo': 'nunique',
            'TotalPrice': ['sum', 'mean'],
            'StockCode': 'nunique',
            'Quantity': 'sum'
        }).reset_index()

        rfm.columns = [
            'CustomerID',
            'Recency',
            'Frequency',
            'TotalSpent',
            'AvgOrderValue',
            'UniqueProducts',
            'TotalItems'
        ]

        self.customer_features = self.customer_features.merge(
            rfm, on='CustomerID', how='left'
        )
        return self

    # -------------------------------------------------
    def create_behavioral_features(self):
        print("\nCreating behavioral features...")

        df = self.training_data.copy()

        gap = df.sort_values('InvoiceDate').groupby('CustomerID').agg({
            'InvoiceDate': lambda x: x.diff().dt.days.mean()
        }).reset_index()

        gap.columns = ['CustomerID', 'AvgDaysBetweenPurchases']

        basket = df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index()
        basket_stats = basket.groupby('CustomerID')['Quantity'].agg(
            ['mean', 'std', 'max']
        ).reset_index()

        basket_stats.columns = ['CustomerID', 'AvgBasketSize', 'StdBasketSize', 'MaxBasketSize']

        time_pref = df.groupby('CustomerID').agg({
            'DayOfWeek': lambda x: x.mode()[0],
            'Hour': lambda x: x.mode()[0]
        }).reset_index()

        time_pref.columns = ['CustomerID', 'PreferredDay', 'PreferredHour']

        country_div = df.groupby('CustomerID')['Country'].nunique().reset_index()
        country_div.columns = ['CustomerID', 'CountryDiversity']

        self.customer_features = (
            self.customer_features
            .merge(gap, on='CustomerID', how='left')
            .merge(basket_stats, on='CustomerID', how='left')
            .merge(time_pref, on='CustomerID', how='left')
            .merge(country_div, on='CustomerID', how='left')
        )
        return self

    # -------------------------------------------------
    def create_temporal_features(self):
        print("\nCreating temporal features...")

        df = self.training_data.copy()

        life = df.groupby('CustomerID')['InvoiceDate'].agg(['min', 'max']).reset_index()
        life.columns = ['CustomerID', 'FirstPurchase', 'LastPurchase']

        life['CustomerLifetimeDays'] = (
            life['LastPurchase'] - life['FirstPurchase']
        ).dt.days

        life = life.merge(
            self.customer_features[['CustomerID', 'Frequency']],
            on='CustomerID', how='left'
        )

        life['PurchaseVelocity'] = life['Frequency'] / (life['CustomerLifetimeDays'] + 1)

        self.customer_features = self.customer_features.merge(
            life[['CustomerID', 'CustomerLifetimeDays', 'PurchaseVelocity']],
            on='CustomerID', how='left'
        )

        for d in [30, 60, 90]:
            cutoff = self.training_cutoff - timedelta(days=d)
            recent = df[df['InvoiceDate'] > cutoff].groupby(
                'CustomerID'
            )['InvoiceNo'].nunique().reset_index()

            recent.columns = ['CustomerID', f'Purchases_Last{d}Days']
            self.customer_features = self.customer_features.merge(
                recent, on='CustomerID', how='left'
            )

        self.customer_features.fillna(0, inplace=True)
        return self

    # -------------------------------------------------
    def create_product_features(self):
        print("\nCreating product features...")

        df = self.training_data.copy()

        diversity = df.groupby('CustomerID')['StockCode'].agg(
            lambda x: x.nunique() / len(x)
        ).reset_index()

        diversity.columns = ['CustomerID', 'ProductDiversityScore']

        price_stats = df.groupby('CustomerID')['Price'].agg(
            ['mean', 'std', 'min', 'max']
        ).reset_index()

        price_stats.columns = [
            'CustomerID',
            'AvgPricePreference',
            'StdPricePreference',
            'MinPrice',
            'MaxPrice'
        ]

        self.customer_features = (
            self.customer_features
            .merge(diversity, on='CustomerID', how='left')
            .merge(price_stats, on='CustomerID', how='left')
        )
        return self

    # -------------------------------------------------
    def create_rfm_segments(self):
        print("\nCreating RFM segments...")

        # Rank-based qcut (bulletproof fix)
        self.customer_features['RecencyScore'] = pd.qcut(
            self.customer_features['Recency'].rank(method='first'),
            4, labels=[4, 3, 2, 1]
        ).astype(int)

        self.customer_features['FrequencyScore'] = pd.qcut(
            self.customer_features['Frequency'].rank(method='first'),
            4, labels=[1, 2, 3, 4]
        ).astype(int)

        self.customer_features['MonetaryScore'] = pd.qcut(
            self.customer_features['TotalSpent'].rank(method='first'),
            4, labels=[1, 2, 3, 4]
        ).astype(int)

        self.customer_features['RFM_Score'] = (
            self.customer_features['RecencyScore'] +
            self.customer_features['FrequencyScore'] +
            self.customer_features['MonetaryScore']
        )
        return self

    # -------------------------------------------------
    def save_features(self):
        print("\nSaving customer features...")

        self.customer_features.to_csv(
            'data/processed/customer_features.csv', index=False
        )

        info = {
            'total_customers': int(len(self.customer_features)),
            'total_features': int(len(self.customer_features.columns)),
            'churn_rate': float(self.customer_features['Churn'].mean())
        }

        with open('data/processed/feature_info.json', 'w') as f:
            json.dump(info, f, indent=4)

        print("Feature engineering completed successfully!")
        return self

    # -------------------------------------------------
    def run_pipeline(self):
        self.split_data_by_time()
        self.create_target_variable()
        self.create_rfm_features()
        self.create_behavioral_features()
        self.create_temporal_features()
        self.create_product_features()
        self.create_rfm_segments()
        self.save_features()

        print("\nFinal dataset shape:", self.customer_features.shape)
        return self.customer_features


if __name__ == "__main__":
    engineer = FeatureEngineer(
        transactions_path='data/processed/cleaned_transactions.csv'
    )
    engineer.run_pipeline()

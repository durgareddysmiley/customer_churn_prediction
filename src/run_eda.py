import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

def run_eda():
    print("Running EDA...")
    
    # Check data
    if not os.path.exists('data/processed/customer_features.csv'):
        print("Feature data not found!")
        return
        
    df = pd.read_csv('data/processed/customer_features.csv')
    os.makedirs('visualizations/eda', exist_ok=True)
    
    # 1. Churn Distribution
    plt.figure(figsize=(6,4))
    sns.countplot(data=df, x='Churn')
    plt.title("Churn Distribution")
    plt.savefig('visualizations/eda/churn_distribution.png')
    plt.close()
    
    # 2. RFM vs Churn
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.boxplot(data=df, x='Churn', y='Recency', ax=axes[0])
    axes[0].set_title("Recency vs Churn")
    
    sns.boxplot(data=df, x='Churn', y='Frequency', ax=axes[1])
    axes[1].set_title("Frequency vs Churn (Log Scale)")
    axes[1].set_yscale('log')
    
    sns.boxplot(data=df, x='Churn', y='TotalSpent', ax=axes[2])
    axes[2].set_title("TotalSpent vs Churn (Log Scale)")
    axes[2].set_yscale('log')
    
    plt.savefig('visualizations/eda/rfm_vs_churn.png')
    plt.close()
    
    # 3. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=False, cmap='coolwarm')
    plt.title("Feature Correlation Heatmap")
    plt.savefig('visualizations/eda/correlation_heatmap.png')
    plt.close()
    
    # 4. Statistical Tests
    churned = df[df['Churn'] == 1]
    active = df[df['Churn'] == 0]
    
    print("\nFeature Significance (T-Test):")
    for col in ['Recency', 'Frequency', 'TotalSpent', 'AvgDaysBetweenPurchases', 'CustomerLifetimeDays']:
        t_stat, p_val = stats.ttest_ind(churned[col], active[col], equal_var=False)
        sig = "Significant" if p_val < 0.05 else "Not Significant"
        print(f"{col}: p-value={p_val:.5f} ({sig})")
        
    print("\nEDA completed. Visualizations saved to visualizations/eda/")

if __name__ == "__main__":
    run_eda()

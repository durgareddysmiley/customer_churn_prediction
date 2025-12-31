# Data Cleaning Report

## Executive Summary
- **Original rows**: 541,910
- **Cleaned rows**: 367,077
- **Retention rate**: 67.74%
- **Data Quality Score**: High (Zero missing values in critical columns)

## Cleaning Steps Applied
1.  **Missing CustomerID Removal**: Removed ~135k rows (25%). Essential for customer-level analysis.
2.  **Cancelled Invoices**: Removed ~9k rows. Focus on positive purchase behavior.
3.  **Negative Quantities**: Removed ~10k rows (redundant with variations of cancellations/errors).
4.  **Unit Price Errors**: Removed rows with Price <= 0.
5.  **Outliers**: Removed extreme quantity outliers using IQR method.

## Data Quality Improvements

| Metric | Before | After | Improvement |
| :--- | :--- | :--- | :--- |
| **Missing CustomerID** | 135,080 | 0 | 100% |
| **Missing Description** | 1,454 | 0 | 100% |
| **Negative Values** | ~10k | 0 | 100% |

## Challenges Faced
- **Challenge**: High percentage of missing customer IDs.
- **Solution**: Accepted the data loss (25%) as these records are unusable for churn prediction.
- **Lesson**: Real-world data often contains anonymous transactions.

## Final Dataset Characteristics
- **Rows**: 367,077
- **Columns**: 13 (Including derived features: TotalPrice, Year, Month, etc.)
- **Date Range**: 2010-12-01 to 2011-12-09

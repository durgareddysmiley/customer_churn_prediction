# Data Cleaning Report

## Executive Summary
- **Original dataset size:** 525,461 rows  
- **Cleaned dataset size:** 342,273 rows  
- **Rows removed:** 183,188  
- **Retention rate:** 65.14%  
- **Data quality score:** 100% completeness (no missing values in final dataset)

The data cleaning process successfully transformed a noisy transactional dataset into a high-quality, analysis-ready dataset suitable for customer-level feature engineering and churn modeling.

---

## Cleaning Steps Applied

### Step 1: Missing CustomerID Removal
- **Rows removed:** ~131,000  
- **Reasoning:** CustomerID is mandatory for customer-level churn prediction and cannot be imputed.
- **Impact:** Reduced dataset size but ensured valid customer tracking.

---

### Step 2: Cancelled Invoice Removal
- **Rows removed:** ~9,000  
- **Reasoning:** Invoices starting with ‘C’ represent cancellations and do not reflect actual purchases.
- **Impact:** Improved accuracy of revenue and frequency calculations.

---

### Step 3: Negative Quantity Removal
- **Rows removed:** ~8,000  
- **Reasoning:** Negative quantities indicate product returns, which distort churn-related behavioral metrics.
- **Impact:** Ensured all transactions represent successful purchases.

---

### Step 4: Zero / Negative Price Removal
- **Rows removed:** ~1,500  
- **Reasoning:** Zero or negative prices are data errors or special cases not relevant to churn analysis.
- **Impact:** Improved monetary feature reliability.

---

### Step 5: Missing Description Removal
- **Rows removed:** ~1,000  
- **Reasoning:** Missing product descriptions add limited analytical value and may affect downstream analysis.
- **Impact:** Minor data loss with improved consistency.

---

### Step 6: Outlier Removal (IQR Method)
- **Rows removed:** ~30,000  
- **Reasoning:** Extremely high quantities or prices skew RFM and behavioral metrics.
- **Impact:** Stabilized statistical distributions and improved model robustness.

---

### Step 7: Duplicate Removal
- **Rows removed:** ~700  
- **Reasoning:** Duplicate transactions artificially inflate purchase counts and revenue.
- **Impact:** Ensured accurate transaction counts.

---

### Step 8: Derived Feature Creation
- **Columns added:** TotalPrice, Year, Month, DayOfWeek, Hour  
- **Impact:** Enabled temporal and monetary feature engineering.

---

### Step 9: Data Type Conversion
- **Actions:**  
  - CustomerID → Integer  
  - StockCode, Country → Category  
- **Impact:** Reduced memory usage and improved processing efficiency.

---

## Data Quality Improvements

| Metric | Before Cleaning | After Cleaning | Improvement |
|------|----------------|---------------|-------------|
| Missing Values | Present | 0 | 100% |
| Duplicate Rows | Present | 0 | 100% |
| Invalid Prices | Present | 0 | 100% |
| Negative Quantities | Present | 0 | 100% |

---

## Challenges Faced

### Challenge 1: High Percentage of Missing CustomerIDs
- **Solution:** Removed all records with missing CustomerID.
- **Lesson:** Identifier fields must be treated strictly in customer-level modeling.

### Challenge 2: Inconsistent Column Names from Excel Source
- **Solution:** Standardized column names programmatically.
- **Lesson:** Always normalize schema before applying transformations.

### Challenge 3: Extreme Outliers in Quantity and Price
- **Solution:** Applied IQR-based outlier removal.
- **Lesson:** Statistical outliers can significantly degrade model performance if not handled.

---

## Final Dataset Characteristics
- **Rows:** 342,273  
- **Columns:** 13  
- **Approx. memory usage:** ~35–40 MB  
- **Date range:** December 2009 – December 2011  
- **Countries:** 38  

---

## Recommendations for Future Work
- Retain cancellation and return data as separate behavioral features.
- Apply advanced anomaly detection methods for outlier handling.
- Automate data validation checks as part of a CI pipeline.

---

## Conclusion
The cleaning pipeline achieved a balance between data retention and quality, producing a reliable dataset for churn prediction and downstream machine learning tasks.

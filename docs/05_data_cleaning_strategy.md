# Data Cleaning Strategy

## 1. Missing Values Strategy

### CustomerID (Missing: ~25%)
**Decision:** DROP  
**Reasoning:**  
CustomerID is essential for customer-level churn analysis. Records without CustomerID cannot be attributed to any customer and therefore cannot be used for feature engineering or churn prediction. Imputing CustomerID is not meaningful because it is an identifier, not a measurable attribute.

**Impact:**  
Approximately 25% of rows will be removed. This is acceptable and expected for the Online Retail dataset.

---

### Description (Missing: <1%)
**Decision:** IMPUTE / DROP  
**Reasoning:**  
Product description is not critical for churn modeling. Missing descriptions are very few and can either be filled with a placeholder value like `"Unknown"` or removed without significant data loss.

---

## 2. Handling Cancellations

**Issue:**  
Invoices starting with the letter `'C'` represent cancelled transactions.

**Options Considered:**  
- **Option A:** Remove all cancelled invoices  
- **Option B:** Keep cancellations as features  

**Chosen Strategy:** Option A – Remove all cancellations  

**Reasoning:**  
Cancelled invoices do not represent completed purchases and negatively impact revenue, quantity, and frequency calculations. Removing them ensures that customer behavior is based only on successful transactions.

---

## 3. Negative Quantities

**Issue:**  
Negative quantities indicate product returns or data entry errors.

**Strategy:**  
Remove rows with negative quantities.

**Reasoning:**  
Negative quantities distort purchase frequency and monetary value metrics, which are critical for RFM feature engineering.

---

## 4. Outliers

### Quantity Outliers
**Detection Method:** IQR (Interquartile Range)  
**Threshold:**  
Values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR

**Action:** Remove extreme outliers

---

### Price Outliers
**Strategy:**  
Remove rows with zero or negative prices and cap extremely high prices using the IQR method.

**Reasoning:**  
Prices must be positive to correctly calculate revenue-based features.

---

## 5. Data Type Conversions

- **InvoiceDate:** Convert to datetime format for temporal analysis  
- **CustomerID:** Convert to integer after removing missing values  
- **UnitPrice / Price:** Already numeric, ensure positivity  

---

## 6. Duplicate Handling

**Strategy:**  
Identify duplicate rows based on all columns. Remove exact duplicates while keeping the first occurrence.

**Reasoning:**  
Duplicate transactions artificially inflate purchase counts and revenue, leading to incorrect feature values.

---

## Summary
This cleaning strategy prioritizes data quality while retaining sufficient data volume (expected retention: 60–70%). All decisions are aligned with the goal of accurate customer-level churn prediction.

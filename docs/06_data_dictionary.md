# Data Dictionary

**Raw Dataset:** Online Retail II (Excel)

---

## Column Descriptions

| Column Name   | Data Type | Description | Example Values | Missing % | Notes |
|--------------|----------|-------------|----------------|-----------|-------|
| Invoice | String | Invoice number for each transaction. Invoices starting with 'C' indicate cancellations | 536365, C536365 | 0% | Used to identify cancelled transactions |
| StockCode | String | Product (item) code | 85123A | 0% | Some non-standard codes exist |
| Description | String | Product name | WHITE HANGING HEART T-LIGHT HOLDER | ~0.3% | Requires cleaning or placeholder |
| Quantity | Integer | Quantity of products per transaction | 6, -1 | 0% | Negative values indicate returns |
| InvoiceDate | DateTime | Date and time of transaction | 2010-12-01 08:26:00 | 0% | Date range: 2009–2011 |
| Price | Float | Unit price of product in GBP (£) | 2.55 | 0% | Some zero or negative values exist |
| CustomerID | Float | Unique customer identifier | 17850.0 | ~25% | High missing rate |
| Country | String | Customer country | United Kingdom | 0% | 38 unique countries |

---

## Data Quality Issues Identified

- Missing values in **CustomerID (~25%)**
- Missing values in **Description (<1%)**
- Cancelled invoices identified by `'C'` prefix
- Negative quantities indicating product returns
- Zero or negative prices
- Presence of duplicate rows
- Extremely high quantity values (potential outliers)

---

## Data Cleaning Required

- Remove rows with missing **CustomerID**
- Handle missing **Description** values (impute or drop)
- Remove cancelled invoices
- Remove rows with negative quantities
- Remove or cap outliers in **Quantity** and **Price**
- Convert **InvoiceDate** to datetime
- Remove duplicate records
- Ensure all numeric values are valid and positive where required

---

## Summary

This data dictionary documents all raw dataset columns, their data types, missing value percentages, and known data quality issues. It serves as a reference for the data cleaning and feature engineering phases.

# Data Dictionary

**Raw Dataset**: `online_retail.csv`

| Column Name | Data Type | Description | Example Values | Missing % (Approx) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **InvoiceNo** | String | 6-digit invoice number. If it starts with 'C', it indicates a cancellation. | 536365, C536365 | 0% | Unique identifier for the transaction/invoice. |
| **StockCode** | String | 5-digit product code. | 85123A, 22423 | 0% | Some non-standard codes (e.g., 'POST', 'D') exist. |
| **Description** | String | Product name. | WHITE HANGING HEART T-LIGHT HOLDER | ~0.2% | Text cleaning required (case, whitespace). |
| **Quantity** | Integer | Quantity of each product per transaction. | 6, -1 | 0% | Negative values typically indicate returns/cancellations. |
| **InvoiceDate** | DateTime | The day and time when each transaction was generated. | 2010-12-01 08:26:00 | 0% | Range: 2009-2011 (depending on specific dataset version). |
| **UnitPrice** | Float | Product price per unit in sterling (£). | 2.55, 0.0 | 0% | Zero values might indicate errors or gifts. |
| **CustomerID** | Float/Int | 5-digit customer identifier. | 17850.0 | ~25% | Key for customer-level aggregation. Missing values must be handled (removed). |
| **Country** | String | The name of the country where each customer resides. | United Kingdom | 0% | 38+ unique countries. |

## Data Quality Issues Identified
- **Missing CustomerID**: Significant portion of the data (~25%) has no CustomerID, making it unusable for churn prediction.
- **Cancellations**: Invoices starting with 'C' needs handling (removal or separate feature).
- **Negative Quantities**: Correspond to cancellations or errors.
- **StockCode Anomalies**: Manual codes like 'POSTAGE', 'DOT', 'M' (Manual).

## Data Cleaning Required
1.  **Drop Correlation**: Remove rows with missing `CustomerID`.
2.  **Handle Cancellations**: Remove invoices starting with 'C'.
3.  **Handle Returns**: Filter out negative quantities.
4.  **Type Conversion**: Convert `InvoiceDate` to datetime, `CustomerID` to integer.

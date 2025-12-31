# Data Cleaning Strategy

## 1. Missing Values Strategy
### CustomerID (Expected Missing: ~25%)
- **Decision**: **REMOVE (DROP)**
- **Reasoning**: `CustomerID` is the primary key for aggregating transactions into customer profiles. Without it, we cannot calculate churn or customer-level features. Imputation is not possible as it represents a unique individual identity.
- **Impact**: We expect to lose approximately 25% of the transaction rows, but these are essentially anonymous transactions not useful for this specific task.

### Description (Expected Missing: ~0.2%)
- **Decision**: **Keep/Ignore** (if row has CustomerID)
- **Reasoning**: Description is useful for text analysis but not strictly required for RFM or core Churn prediction. If the row has a valid CustomerID, we keep it. If we need to process text, we can fill missing with "Unknown".

## 2. Handling Cancellations
- **Issue**: Invoices starting with 'C' indicate cancellations.
- **Strategy**: **REMOVE**
- **Reasoning**: For the purpose of simplified churn prediction, we want to focus on positive purchase behavior. Including cancellations complicates the logic (e.g., negative monetary value). While sophisticated models might use "Return Rate" as a feature, for this baseline we will exclude them to ensure clean RFM calculations.

## 3. Negative Quantities
- **Issue**: Negative values usually accompany cancellations or adjustments.
- **Strategy**: **REMOVE**
- **Reasoning**: Consistent with removing cancellations. We only want valid, positive purchases.

## 4. Outliers
### Quantity Outliers
- **Detection Method**: **IQR (Interquartile Range)**
- **Threshold**: Remove records where Quantity > Q3 + 1.5 * IQR.
- **Action**: **REMOVE**
- **Reasoning**: Bulk orders by wholesalers can skew the model. We want to predict behavior of typical retail customers.

### Price Outliers
- **Detection Method**: Domain Knowledge & IQR.
- **Action**: Remove records with `UnitPrice` <= 0 (errors/gifts) and extremely high prices if they don't look like valid products (e.g., manual entries).

## 5. Duplicate Handling
- **Strategy**: **Deduplicate exact matches**.
- **Reasoning**: System errors might generate duplicate records. We will drop rows where all columns are identical.

## 6. Type Conversions
- **InvoiceDate**: Convert to datetime object for temporal features.
- **CustomerID**: Convert to Integer (remove decimals).

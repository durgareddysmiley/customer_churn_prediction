# Feature Dictionary

## Target Variable
| Feature | Type | Description | Values |
| :--- | :--- | :--- | :--- |
| **Churn** | Binary | 1 = Churned (No purchase in observation period), 0 = Active. | 0, 1 |

## RFM Features
| Feature | Type | Description | Business Meaning |
| :--- | :--- | :--- | :--- |
| **Recency** | Integer | Days since last purchase relative to training cutoff. | Lower `Recency` indicates a more engaged customer. High recency is a strong churn signal. |
| **Frequency** | Integer | Total number of unique invoices (purchases). | Higher `Frequency` indicates loyalty. |
| **TotalSpent** | Float | Total monetary value (Sum of `TotalPrice`). | Customer Lifetime Value proxy. |
| **AvgOrderValue** | Float | Average spend per transaction (`TotalSpent` / `Frequency`). | Indicates spending power per visit. |
| **TotalItems** | Integer | Total quantity of items purchased. | Volume of purchases. |
| **UniqueProducts**| Integer | Number of unique `StockCode`s bought. | Indicates product variety/exploration. |

## Behavioral features
| Feature | Type | Description | Business Meaning |
| :--- | :--- | :--- | :--- |
| **AvgDaysBetweenPurchases** | Float | Average number of days between consecutive purchases. | Regularity metric. High values indicate infrequent buying. |
| **StdDaysBetweenPurchases** | Float | Standard deviation of purchase intervals. | Consistency metric. High variance means irregular behavior. |
| **AvgBasketSize** | Float | Average quantity of items per invoice. | Size of typical cart. |
| **MaxBasketSize** | Integer | Maximum quantity in a single invoice. | Peak purchasing event. |

## Temporal Features
| Feature | Type | Description | Business Meaning |
| :--- | :--- | :--- | :--- |
| **CustomerLifetimeDays** | Integer | Days between first purchase and training cutoff. | Relationship duration ("Tenure"). |

## Segmentation
| Feature | Type | Description | Business Meaning |
| :--- | :--- | :--- | :--- |
| **R_Score** | Integer | Quartile score for Recency (4=Best/Recent, 1=Worst/Old). | Segment component. |
| **F_Score** | Integer | Quartile score for Frequency (4=Best/High, 1=Worst/Low). | Segment component. |
| **M_Score** | Integer | Quartile score for Monetary (4=Best/High, 1=Worst/Low). | Segment component. |
| **RFM_Score** | Integer | Sum of R, F, M scores (3 to 12). | Overall customer value score. |
| **CustomerSegment** | String | Category based on RFM Score (Champions, Loyal, etc.). | interpretable customer bucket for marketing. |

# Feature Dictionary

This document describes all customer-level features engineered for the churn prediction model, including their definitions, data types, ranges, and business meaning.

---

## Target Variable

| Feature | Type | Description | Example | Business Meaning |
|------|------|-----------|--------|------------------|
| Churn | Binary | 1 = Churned, 0 = Active | 1 | Customer did not make any purchase in the next 3 months |

---

## RFM Features

| Feature | Type | Description | Range | Business Meaning |
|-------|------|------------|-------|------------------|
| Recency | Integer | Days since last purchase (from training cutoff) | 0–600 | Lower value = customer purchased recently |
| Frequency | Integer | Number of unique purchase invoices | 1–200+ | Higher value = more loyal customer |
| TotalSpent | Float | Total money spent (£) | 0–50,000+ | Customer lifetime value |
| AvgOrderValue | Float | Average spend per order (£) | 0–5,000 | Indicates spending behavior |
| UniqueProducts | Integer | Number of unique products purchased | 1–1,000 | Higher = broader interest |
| TotalItems | Integer | Total quantity purchased | 1–10,000+ | Measures buying volume |

---

## Behavioral Features

| Feature | Type | Description | Business Meaning |
|-------|------|------------|------------------|
| AvgDaysBetweenPurchases | Float | Average days between purchases | Lower = frequent shopper |
| AvgBasketSize | Float | Average items per order | Larger baskets = bulk buyer |
| StdBasketSize | Float | Variability in basket size | Indicates inconsistent buying |
| MaxBasketSize | Integer | Maximum items bought in one order | Bulk purchase behavior |
| PreferredDay | Integer | Most common shopping weekday (0=Mon) | Shopping habit |
| PreferredHour | Integer | Most common shopping hour | Time preference |
| CountryDiversity | Integer | Number of countries purchased from | Cross-border behavior |

---

## Temporal Features

| Feature | Type | Description | Business Meaning |
|-------|------|------------|------------------|
| CustomerLifetimeDays | Integer | Days between first and last purchase | Longer = stronger relationship |
| PurchaseVelocity | Float | Purchases per day | Buying intensity |
| Purchases_Last30Days | Integer | Purchases in last 30 days | Recent engagement |
| Purchases_Last60Days | Integer | Purchases in last 60 days | Medium-term activity |
| Purchases_Last90Days | Integer | Purchases in last 90 days | Churn indicator |

---

## Product Features

| Feature | Type | Description | Business Meaning |
|-------|------|------------|------------------|
| ProductDiversityScore | Float | Unique products / total purchases | Variety-seeking behavior |
| AvgPricePreference | Float | Average unit price preferred (£) | Price sensitivity |
| StdPricePreference | Float | Price variation | Discount sensitivity |
| MinPrice | Float | Minimum unit price purchased | Budget threshold |
| MaxPrice | Float | Maximum unit price purchased | Premium affinity |

---

## RFM Segmentation Features

| Feature | Type | Description | Business Meaning |
|-------|------|------------|------------------|
| RecencyScore | Integer | Quartile-based recency score (1–4) | Higher = more recent |
| FrequencyScore | Integer | Quartile-based frequency score | Higher = loyal |
| MonetaryScore | Integer | Quartile-based spending score | Higher = high value |
| RFM_Score | Integer | Sum of R, F, M scores | Overall customer value |

---

## Feature Engineering Decisions

### Why these features?
- RFM features are industry-standard for customer behavior analysis
- Behavioral features capture shopping patterns and habits
- Temporal features detect engagement decline
- Product features reveal preferences and sensitivity
- Combined features improve churn prediction accuracy

---

## Feature Interactions

- High Recency + Low Purchases_Last30Days → Strong churn signal
- High Frequency + High TotalSpent → Loyal customer
- Low PurchaseVelocity + High Recency → At-risk customer

---

## Feature Importance Hypothesis

Based on business knowledge, the most important predictors of churn are expected to be:
1. Recency (strongest predictor)
2. Purchases_Last30Days
3. Frequency
4. PurchaseVelocity
5. TotalSpent

---

## Conclusion

The engineered features comprehensively represent customer value, behavior, engagement, and preferences, providing a strong foundation for churn prediction modeling.

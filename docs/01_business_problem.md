# Business Problem Statement

## 1. Business Context

The e-commerce industry is highly competitive, with multiple platforms offering similar products and prices. Customers can easily switch between platforms, which makes customer retention a critical challenge.

Customer retention is very important because acquiring a new customer costs 5 to 25 times more than retaining an existing one. Loyal customers also tend to purchase more frequently and generate higher lifetime value.

RetailCo Analytics is currently facing difficulty in identifying customers who are likely to stop purchasing and lacks insights into customer purchasing behavior.

---

## 2. Problem Definition

Customer churn is defined as:

**A customer who has not made a purchase in the last 90 days (3 months).**

The business problem is to predict customer churn in advance so that proactive retention strategies can be applied before customers are lost.

---

## 3. Stakeholders

- **Marketing Team**  
  Needs customer segments and churn predictions to run targeted retention campaigns.

- **Sales Team**  
  Needs churn probability scores to prioritize high-risk customers.

- **Product Team**  
  Needs insights into purchasing patterns and product preferences.

- **Executive Team**  
  Needs churn metrics and ROI projections to guide strategic decisions.

---

## 4. Business Impact

By accurately predicting customer churn, RetailCo Analytics expects:

- A **15–20% reduction in customer churn rate**
- Increase in overall revenue through improved customer retention
- Cost savings by avoiding unnecessary marketing spend
- Better personalization of marketing campaigns

---

## 5. Success Metrics

### Primary Metric
- **ROC-AUC Score > 0.78**

### Secondary Metrics
- **Precision > 0.75** (to minimize false positives)
- **Recall > 0.70** (to correctly identify actual churners)
- **F1-Score > 0.72**

These metrics ensure the model aligns with business goals by balancing accuracy and practical usability.

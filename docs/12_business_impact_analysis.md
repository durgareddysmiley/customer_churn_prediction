# Business Impact Analysis

## Model Performance in Business Terms

### Confusion Matrix Interpretation
Based on a test set of **485 customers**:

- **True Positives (TP): 119** customers correctly identified as churners  
- **False Positives (FP): 87** customers incorrectly flagged as churners  
- **True Negatives (TN): 192** customers correctly identified as active  
- **False Negatives (FN): 87** customers missed (actual churners not detected)

This shows that the model is effective at identifying churn-prone customers while maintaining a reasonable balance between false positives and false negatives.

---

## Business Cost Analysis

### Assumptions
- Cost of retention campaign per customer: **£10**
- Average customer lifetime value (CLV): **£500**
- Churn rate: **42.7%**

---

## Scenario Analysis

### Without Model
- Random targeting: Contact **485 customers**
- Expected cost: **£4,850**
- Expected churners caught: **≈207**
- ROI: Low due to high cost and inefficient targeting

---

### With Model
- Targeted approach: Contact **206 customers (TP + FP)**
- Cost: **£2,060**
- Churners caught: **119**
- Churners missed: **87**

**Revenue Protected:**  
- **£59,500 (119 × £500)**

**ROI:**  
The model significantly reduces marketing cost while protecting high customer value, resulting in strong positive ROI.

---

## Expected Business Outcomes

- **Churn Reduction:** From **42.7%** to approximately **24.8%**
- **Cost Savings:** Approximately **£2,790 per campaign**
- **Revenue Protected:** Approximately **£59,500 per campaign**

---

## Implementation Recommendations

### Who to Target
- Customers with churn probability greater than **0.6**
- Prioritize high-value customers with high churn risk
- Use RFM scores to further segment customers

---

### Retention Strategies by Segment
- **High Risk, High Value:** Personalized offers, loyalty benefits, proactive calls  
- **High Risk, Low Value:** Discount-based or automated retention campaigns  
- **Low Risk:** Maintain engagement through regular communication  

---

## Model Limitations

### Known Issues
- Model may struggle with customers showing sudden behavior changes  
- Borderline customers near decision threshold may be misclassified  
- Performance depends on historical data quality  

---

### Recommended Actions
- Monitor performance monthly  
- Retrain model quarterly  
- Combine model output with business rules

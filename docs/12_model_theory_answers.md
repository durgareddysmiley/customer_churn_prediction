# Model Theory & Research Answers

## Decision Tree

### Q1: What is max_depth?
max_depth controls how deep the decision tree can grow. A higher depth allows the model to learn complex patterns.

### Q2: What happens if max_depth is too large?
If max_depth is too large, the model overfits by memorizing training data and performs poorly on new data.

### Q3: How do you prevent overfitting in decision trees?
- Limit max_depth
- Increase min_samples_split
- Use pruning techniques

---

## Random Forest

### Q1: What is an ensemble method?
An ensemble method combines predictions from multiple models to improve performance and reduce overfitting.

### Q2: How many trees should you use?
Typically 100–300 trees provide good performance without excessive computation.

### Q3: Why is Random Forest better than a single Decision Tree?
Random Forest reduces variance by averaging many trees trained on random subsets of data.

---

## Gradient Boosting

### Q1: Difference between boosting and bagging?
- Bagging (Random Forest): models are trained independently.
- Boosting: models are trained sequentially, correcting previous errors.

### Q2: What is learning_rate?
learning_rate controls how much each new tree contributes. Smaller values improve generalization.

### Q3: How to tune n_estimators?
Use more trees with a lower learning rate to avoid overfitting.

---

## Neural Network

### Q1: What is a hidden layer?
A hidden layer transforms inputs using weights and activation functions to learn complex patterns.

### Q2: What happens if too many layers are used?
Too many layers can cause overfitting and slow training.

### Q3: How do you prevent overfitting in neural networks?
- Regularization
- Early stopping
- Dropout
- Proper architecture design

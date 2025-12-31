import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import *
import os
import json

def evaluate_model():
    print("Evaluating best model...")
    os.makedirs('visualizations/evaluation', exist_ok=True)
    
    # Load
    X_test = pd.read_csv('data/processed/model_ready/X_test.csv')
    y_test = pd.read_csv('data/processed/model_ready/y_test.csv').values.ravel()
    model = joblib.load('models/best_model.pkl')
    
    # Predict
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        'test_accuracy': accuracy_score(y_test, y_pred),
        'test_precision': precision_score(y_test, y_pred),
        'test_recall': recall_score(y_test, y_pred),
        'test_f1': f1_score(y_test, y_pred),
        'test_roc_auc': roc_auc_score(y_test, y_prob)
    }
    
    print("Test Metrics:")
    print(json.dumps(metrics, indent=4))
    
    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % metrics['test_roc_auc'])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.savefig('visualizations/evaluation/roc_curve.png')
    plt.close()
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig('visualizations/evaluation/confusion_matrix.png')
    plt.close()
    
    # Precision-Recall Curve (Extra)
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    plt.figure()
    plt.plot(recall, precision, marker='.')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.savefig('visualizations/evaluation/precision_recall_curve.png')
    plt.close()

if __name__ == "__main__":
    evaluate_model()

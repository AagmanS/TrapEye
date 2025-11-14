import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
import joblib

def evaluate_model(model_path='models/phish_model.joblib', test_data_path=None):
    """Evaluate the trained model"""
    
    # Load model
    try:
        model_data = joblib.load(model_path)
        model = model_data['model']
        feature_names = model_data['feature_names']
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Load or generate test data
    if test_data_path:
        df = pd.read_csv(test_data_path)
    else:
        # Generate synthetic test data
        from train import PhishingDetectorTrainer
        trainer = PhishingDetectorTrainer()
        df = trainer.create_synthetic_dataset(500)
    
    X_test = df[feature_names]
    y_test = df['label']
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print("="*60)
    print("MODEL EVALUATION METRICS")
    print("="*60)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['benign', 'phishing']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Feature importance
    print("\nTop 10 Feature Importances:")
    feature_imp = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_imp.head(10))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc
    }

if __name__ == "__main__":
    evaluate_model()
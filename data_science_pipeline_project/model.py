"""
Model training and evaluation for StyleSense Fashion Review recommendations
"""

import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns


class RecommendationModel:
    """
    Machine Learning model for predicting product recommendations
    """
    
    def __init__(self, model_type='random_forest', random_state=42):
        """
        Initialize the recommendation model
        
        Args:
            model_type: Type of model ('random_forest', 'gradient_boosting', 'logistic_regression')
            random_state: Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = self._create_model()
        self.metrics = None
    
    def _create_model(self):
        """Create the specified model"""
        if self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=self.random_state,
                n_jobs=-1,
                class_weight='balanced'
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=self.random_state
            )
        elif self.model_type == 'logistic_regression':
            return LogisticRegression(
                random_state=self.random_state,
                max_iter=1000,
                class_weight='balanced'
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train, y_train):
        """
        Train the model
        
        Args:
            X_train: Training features (preprocessed)
            y_train: Training target variable
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        print("Model training completed!")
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Features to predict on
            
        Returns:
            np.array: Predictions (0 or 1)
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Get prediction probabilities
        
        Args:
            X: Features to predict on
            
        Returns:
            np.array: Prediction probabilities
        """
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test target variable
            
        Returns:
            dict: Dictionary of evaluation metrics
        """
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)[:, 1]
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred, zero_division=0)
        }
        
        return self.metrics
    
    def print_evaluation_report(self):
        """Print evaluation metrics"""
        if self.metrics is None:
            print("No evaluation metrics available. Run evaluate() first.")
            return
        
        print("\n" + "="*60)
        print(f"MODEL EVALUATION REPORT: {self.model_type.upper()}")
        print("="*60)
        print(f"Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1-Score:  {self.metrics['f1']:.4f}")
        print(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        print("\nConfusion Matrix:")
        print(self.metrics['confusion_matrix'])
        print("\nClassification Report:")
        print(self.metrics['classification_report'])
        print("="*60)
    
    def save_model(self, filepath):
        """
        Save trained model to file
        
        Args:
            filepath: Path to save the model
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load_model(filepath):
        """
        Load trained model from file
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            Loaded model
        """
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        print(f"Model loaded from {filepath}")
        return model


class ModelComparison:
    """Compare multiple models"""
    
    def __init__(self, random_state=42):
        self.models = {}
        self.results = {}
        self.random_state = random_state
    
    def train_models(self, X_train, y_train, model_types=None):
        """
        Train multiple models
        
        Args:
            X_train: Training features
            y_train: Training target
            model_types: List of model types to train
        """
        if model_types is None:
            model_types = ['random_forest', 'gradient_boosting', 'logistic_regression']
        
        for model_type in model_types:
            print(f"\n{'='*50}")
            model = RecommendationModel(model_type=model_type, random_state=self.random_state)
            model.train(X_train, y_train)
            self.models[model_type] = model
    
    def evaluate_all(self, X_test, y_test):
        """
        Evaluate all trained models
        
        Args:
            X_test: Test features
            y_test: Test target
        """
        for model_type, model in self.models.items():
            print(f"\nEvaluating {model_type}...")
            metrics = model.evaluate(X_test, y_test)
            self.results[model_type] = metrics
            model.print_evaluation_report()
    
    def compare_results(self):
        """Compare results across models"""
        comparison_df = pd.DataFrame({
            model_type: {
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1-Score': metrics['f1'],
                'ROC-AUC': metrics['roc_auc']
            }
            for model_type, metrics in self.results.items()
        }).T
        
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        print(comparison_df.round(4))
        print("="*60)
        
        # Find best model
        best_model = comparison_df['F1-Score'].idxmax()
        print(f"\nBest model (by F1-Score): {best_model}")
        print(f"F1-Score: {comparison_df.loc[best_model, 'F1-Score']:.4f}")
        
        return comparison_df
    
    def get_best_model(self, metric='f1'):
        """Get the best performing model"""
        best_model_name = max(
            self.results.keys(),
            key=lambda x: self.results[x][metric]
        )
        return self.models[best_model_name], best_model_name


def visualize_confusion_matrix(metrics, model_name, save_path=None):
    """Visualize confusion matrix"""
    cm = metrics['confusion_matrix']
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['No Recommendation', 'Recommended'],
                yticklabels=['No Recommendation', 'Recommended'])
    plt.title(f'Confusion Matrix: {model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

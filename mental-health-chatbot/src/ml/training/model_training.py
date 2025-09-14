"""
Model Training for Machine Learning Models
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

class ModelTrainer:
    """Model training utilities for mental health models"""
    
    def __init__(self):
        """Initialize model trainer"""
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
            'svm': SVC(probability=True, random_state=42)
        }
        self.trained_models = {}
        self.model_scores = {}
    
    def train_model(self, 
                   X: np.ndarray, 
                   y: np.ndarray, 
                   model_name: str = 'random_forest',
                   test_size: float = 0.2,
                   random_state: int = 42) -> Dict[str, Any]:
        """Train a machine learning model"""
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not supported")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Get model
        model = self.models[model_name]
        
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        # Store trained model
        self.trained_models[model_name] = model
        self.model_scores[model_name] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        return {
            'model': model,
            'accuracy': accuracy,
            'cv_scores': cv_scores,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    def train_all_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Train all available models and return results"""
        results = {}
        
        for model_name in self.models.keys():
            try:
                result = self.train_model(X, y, model_name)
                results[model_name] = result
            except Exception as e:
                print(f"Error training {model_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        return results
    
    def get_best_model(self) -> Tuple[str, Any]:
        """Get the best performing model"""
        if not self.model_scores:
            raise ValueError("No models have been trained yet")
        
        best_model_name = max(self.model_scores.keys(), 
                            key=lambda x: self.model_scores[x]['accuracy'])
        
        return best_model_name, self.trained_models[best_model_name]
    
    def save_model(self, model_name: str, filepath: str):
        """Save a trained model to file"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} has not been trained")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.trained_models[model_name], filepath)
    
    def load_model(self, model_name: str, filepath: str):
        """Load a trained model from file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file {filepath} not found")
        
        self.trained_models[model_name] = joblib.load(filepath)
    
    def predict(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """Make predictions using a trained model"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} has not been trained")
        
        return self.trained_models[model_name].predict(X)
    
    def predict_proba(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities using a trained model"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} has not been trained")
        
        return self.trained_models[model_name].predict_proba(X)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about trained models"""
        return {
            'trained_models': list(self.trained_models.keys()),
            'model_scores': self.model_scores
        }


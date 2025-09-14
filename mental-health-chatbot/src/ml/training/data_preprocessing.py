"""
Data Preprocessing for Machine Learning Models
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import re

class DataPreprocessor:
    """Data preprocessing utilities for mental health models"""
    
    def __init__(self):
        """Initialize data preprocessor"""
        self.text_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text data"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def preprocess_mental_health_data(self, data: List[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess mental health data for training"""
        if not data:
            return np.array([]), np.array([])
        
        # Extract features
        text_features = []
        numerical_features = []
        labels = []
        
        for item in data:
            # Text features
            text = item.get('text', '')
            processed_text = self.preprocess_text(text)
            text_features.append(processed_text)
            
            # Numerical features
            numerical = [
                item.get('mood_score', 5),
                item.get('stress_level', 5),
                item.get('sleep_hours', 8),
                item.get('energy_level', 5),
                item.get('social_activity', 5),
                item.get('physical_activity', 5)
            ]
            numerical_features.append(numerical)
            
            # Labels
            labels.append(item.get('label', 'healthy'))
        
        # Vectorize text features
        text_vectorized = self.text_vectorizer.fit_transform(text_features)
        
        # Scale numerical features
        numerical_scaled = self.scaler.fit_transform(numerical_features)
        
        # Encode labels
        labels_encoded = self.label_encoder.fit_transform(labels)
        
        # Combine features
        combined_features = np.hstack([text_vectorized.toarray(), numerical_scaled])
        
        self.is_fitted = True
        
        return combined_features, labels_encoded
    
    def transform_new_data(self, data: List[Dict[str, Any]]) -> np.ndarray:
        """Transform new data using fitted preprocessors"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transforming new data")
        
        text_features = []
        numerical_features = []
        
        for item in data:
            # Text features
            text = item.get('text', '')
            processed_text = self.preprocess_text(text)
            text_features.append(processed_text)
            
            # Numerical features
            numerical = [
                item.get('mood_score', 5),
                item.get('stress_level', 5),
                item.get('sleep_hours', 8),
                item.get('energy_level', 5),
                item.get('social_activity', 5),
                item.get('physical_activity', 5)
            ]
            numerical_features.append(numerical)
        
        # Transform using fitted preprocessors
        text_vectorized = self.text_vectorizer.transform(text_features)
        numerical_scaled = self.scaler.transform(numerical_features)
        
        # Combine features
        combined_features = np.hstack([text_vectorized.toarray(), numerical_scaled])
        
        return combined_features
    
    def get_feature_names(self) -> List[str]:
        """Get feature names"""
        if not self.is_fitted:
            return []
        
        text_features = self.text_vectorizer.get_feature_names_out()
        numerical_features = ['mood_score', 'stress_level', 'sleep_hours', 
                            'energy_level', 'social_activity', 'physical_activity']
        
        return list(text_features) + numerical_features
    
    def get_class_names(self) -> List[str]:
        """Get class names"""
        if not self.is_fitted:
            return []
        
        return list(self.label_encoder.classes_)


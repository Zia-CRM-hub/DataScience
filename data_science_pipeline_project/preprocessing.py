"""
Data preprocessing pipeline for StyleSense Fashion Review dataset
Handles numerical, categorical, and text features
"""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer

class PreprocessingPipeline:
    """
    Complete preprocessing pipeline for mixed data types
    Handles numerical, categorical, and text features
    """
    
    def __init__(self):
        self.pipeline = None
        self.feature_names = None
    
    def build_pipeline(self):
        """
        Build a preprocessing pipeline that handles:
        - Numerical features: age, rating
        - Categorical features: category, price_range
        - Text features: review_text
        """
        
        # Define feature groups
        numerical_features = ['age', 'rating']
        categorical_features = ['category', 'price_range']
        text_feature = 'review_text'
        
        # Numerical preprocessing
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        # Categorical preprocessing
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
        ])
        
        # Text preprocessing using TF-IDF
        text_transformer = Pipeline(steps=[
            ('tfidf', TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2)))
        ])
        
        # Combine all transformers
        self.pipeline = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features),
                # Pass a single column label so TfidfVectorizer receives a 1D sequence.
                ('text', text_transformer, text_feature)
            ],
            remainder='drop'
        )
        
        return self.pipeline
    
    def fit_transform(self, X):
        """Fit pipeline and transform data"""
        if self.pipeline is None:
            self.build_pipeline()
        
        transformed_data = self.pipeline.fit_transform(X)
        return transformed_data
    
    def transform(self, X):
        """Transform data using fitted pipeline"""
        if self.pipeline is None:
            raise ValueError("Pipeline not fitted. Call fit_transform first.")
        
        return self.pipeline.transform(X)
    
    def get_feature_names(self):
        """Get feature names after transformation"""
        if self.pipeline is None:
            raise ValueError("Pipeline not fitted. Call fit_transform first.")
        
        try:
            feature_names = self.pipeline.get_feature_names_out()
            self.feature_names = feature_names
            return feature_names
        except AttributeError:
            return None


def create_train_test_split(df, test_size=0.2, random_state=42):
    """
    Split data into train and test sets
    
    Args:
        df: DataFrame with target variable 'recommend'
        test_size: Proportion of test data
        random_state: Random seed
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    from sklearn.model_selection import train_test_split
    
    # Separate features and target
    X = df.drop('recommend', axis=1)
    y = df['recommend']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test


def preprocess_data(df, test_size=0.2, random_state=42):
    """
    Complete preprocessing workflow
    
    Args:
        df: Raw DataFrame
        test_size: Proportion of test data
        random_state: Random seed
        
    Returns:
        dict: Dictionary containing preprocessed data and pipeline
    """
    
    # Split data
    X_train, X_test, y_train, y_test = create_train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    
    # Create and fit preprocessing pipeline
    pipeline = PreprocessingPipeline()
    X_train_processed = pipeline.fit_transform(X_train)
    X_test_processed = pipeline.transform(X_test)
    
    return {
        'X_train': X_train_processed,
        'X_test': X_test_processed,
        'y_train': y_train,
        'y_test': y_test,
        'pipeline': pipeline,
        'X_train_raw': X_train,
        'X_test_raw': X_test
    }

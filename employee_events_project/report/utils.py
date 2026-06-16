"""
Utility functions for the report module
"""

import pickle
from pathlib import Path

# Set project paths using pathlib
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "model.pkl"

def load_model():
    """
    Load the machine learning model from model.pkl file.
    
    Returns:
        The unpickled model object
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    return model

def get_project_root():
    """Get the root directory of the project"""
    return PROJECT_ROOT

def get_model_path():
    """Get the path to the model.pkl file"""
    return MODEL_PATH

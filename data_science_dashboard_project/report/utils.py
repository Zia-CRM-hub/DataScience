"""
Utility functions for the report module
"""

import pickle
from pathlib import Path

# Set project paths using pathlib
PROJECT_ROOT = Path(__file__).resolve().parent.parent
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


def try_load_model():
    """Load model if available, otherwise return None."""
    if not MODEL_PATH.exists():
        return None
    try:
        return load_model()
    except Exception:
        return None


def _fallback_recruitment_likelihood(positive_events, negative_events):
    """Heuristic fallback when model.pkl is unavailable."""
    positive = max(float(positive_events), 0.0)
    negative = max(float(negative_events), 0.0)
    total = positive + negative
    if total <= 0:
        return 0.5

    negative_ratio = negative / total
    activity_factor = min(total / 10.0, 1.0)
    probability = 0.15 + (0.75 * negative_ratio) + (0.10 * (1.0 - activity_factor))
    return min(max(probability, 0.0), 1.0)


def predict_recruitment_likelihood(positive_events, negative_events, model=None):
    """Predict recruitment likelihood for one employee event profile."""
    if model is not None and hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba([[positive_events, negative_events]])
            return float(probs[0][1])
        except Exception:
            pass
    return _fallback_recruitment_likelihood(positive_events, negative_events)


def average_team_recruitment_likelihood(events, model=None):
    """Compute average recruitment likelihood for a team event list."""
    if not events:
        return 0.0

    scores = []
    for event in events:
        score = predict_recruitment_likelihood(event[3], event[4], model=model)
        scores.append(score)

    return sum(scores) / len(scores)

"""
Main training script for StyleSense Fashion Review Recommendation System
Brings together data generation, preprocessing, model training, and evaluation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from data_generation import load_or_create_dataset
from preprocessing import preprocess_data
from model import RecommendationModel, ModelComparison

def main():
    """Main training pipeline"""
    
    print("="*70)
    print("STYLESENSE FASHION REVIEW RECOMMENDATION SYSTEM")
    print("="*70)
    
    # 1. Load or create dataset
    print("\n[Step 1] Loading dataset...")
    data_dir = Path(__file__).parent / "data"
    df = load_or_create_dataset(data_dir, n_samples=1000)
    
    print(f"Dataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nTarget distribution:")
    print(df['recommend'].value_counts())
    print(f"Recommendation rate: {df['recommend'].mean():.2%}")
    
    # 2. Preprocess data
    print("\n[Step 2] Preprocessing data...")
    print("Handling numerical features: age, rating")
    print("Handling categorical features: category, price_range")
    print("Handling text features: review_text")
    
    preprocessed = preprocess_data(df, test_size=0.2, random_state=42)
    
    X_train = preprocessed['X_train']
    X_test = preprocessed['X_test']
    y_train = preprocessed['y_train']
    y_test = preprocessed['y_test']
    
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    print(f"Number of features after preprocessing: {X_train.shape[1]}")
    
    # 3. Train and evaluate single model
    print("\n[Step 3] Training Random Forest model...")
    model = RecommendationModel(model_type='random_forest', random_state=42)
    model.train(X_train, y_train)
    
    print("\n[Step 4] Evaluating model...")
    metrics = model.evaluate(X_test, y_test)
    model.print_evaluation_report()
    
    # 4. Save model
    print("\n[Step 5] Saving model...")
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    model.save_model(models_dir / "stylesense_model.pkl")
    
    # 5. Compare multiple models
    print("\n[Step 6] Comparing multiple models...")
    comparison = ModelComparison(random_state=42)
    comparison.train_models(X_train, y_train)
    comparison.evaluate_all(X_test, y_test)
    comparison.compare_results()
    
    # Get and save best model
    best_model, best_model_name = comparison.get_best_model(metric='f1')
    best_model.save_model(models_dir / "best_stylesense_model.pkl")
    
    print("\n[Step 7] Making predictions on sample data...")
    
    # Create a sample review for prediction
    sample_reviews = [
        {
            'age': 28,
            'category': 'Dresses',
            'price_range': 'Mid-Range',
            'rating': 5,
            'review_text': 'Amazing quality and perfect fit! Love this dress, would definitely recommend!'
        },
        {
            'age': 35,
            'category': 'Tops',
            'price_range': 'Budget',
            'rating': 2,
            'review_text': 'Poor quality, material is thin and cheap. Disappointed with this purchase.'
        }
    ]
    
    sample_df = pd.DataFrame(sample_reviews)
    sample_processed = preprocessed['pipeline'].transform(sample_df)
    
    predictions = best_model.predict(sample_processed)
    probabilities = best_model.predict_proba(sample_processed)
    
    print("\nSample Predictions:")
    for i, (review, pred, prob) in enumerate(zip(sample_reviews, predictions, probabilities)):
        rec_text = "RECOMMEND" if pred == 1 else "NOT RECOMMEND"
        confidence = prob[pred] * 100
        print(f"\nSample {i+1}:")
        print(f"  Review: {review['review_text'][:50]}...")
        print(f"  Prediction: {rec_text} (Confidence: {confidence:.2f}%)")
    
    print("\n" + "="*70)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    
    return {
        'model': best_model,
        'preprocessing_pipeline': preprocessed['pipeline'],
        'metrics': metrics,
        'comparison_results': comparison.results
    }


if __name__ == "__main__":
    results = main()

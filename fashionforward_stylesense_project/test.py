"""
Test suite for StyleSense Fashion Review Recommendation System
Tests data generation, preprocessing, and model training
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_generation import generate_stylesense_dataset, load_or_create_dataset
from preprocessing import PreprocessingPipeline, create_train_test_split, preprocess_data
from model import RecommendationModel, ModelComparison


class TestDataGeneration:
    """Tests for data generation module"""
    
    def test_generate_dataset_shape(self):
        """Test that generated dataset has correct shape"""
        df = generate_stylesense_dataset(n_samples=100)
        assert df.shape[0] == 100
        assert df.shape[1] == 6  # age, category, price_range, rating, review_text, recommend
    
    def test_generated_data_has_required_columns(self):
        """Test that generated dataset has all required columns"""
        df = generate_stylesense_dataset(n_samples=50)
        required_columns = ['age', 'category', 'price_range', 'rating', 'review_text', 'recommend']
        assert all(col in df.columns for col in required_columns)
    
    def test_generated_data_types(self):
        """Test that generated data has correct data types"""
        df = generate_stylesense_dataset(n_samples=50)
        assert pd.api.types.is_numeric_dtype(df['age'])
        assert pd.api.types.is_numeric_dtype(df['rating'])
        assert pd.api.types.is_object_dtype(df['review_text'])
        assert pd.api.types.is_object_dtype(df['category'])
        assert df['recommend'].dtype in [np.int64, np.int32, int]
    
    def test_generated_data_value_ranges(self):
        """Test that generated data values are in expected ranges"""
        df = generate_stylesense_dataset(n_samples=100)
        
        assert df['age'].min() >= 18 and df['age'].max() <= 75
        assert df['rating'].min() >= 1 and df['rating'].max() <= 5
        assert df['recommend'].isin([0, 1]).all()
        assert df['category'].isin(['Dresses', 'Tops', 'Pants', 'Outerwear', 'Shoes', 'Accessories']).all()
    
    def test_no_missing_values(self):
        """Test that generated dataset has no missing values"""
        df = generate_stylesense_dataset(n_samples=100)
        assert not df.isnull().any().any()


class TestPreprocessing:
    """Tests for preprocessing module"""
    
    def test_preprocessing_pipeline_creation(self):
        """Test that preprocessing pipeline is created correctly"""
        pipeline = PreprocessingPipeline()
        pipeline.build_pipeline()
        assert pipeline.pipeline is not None
    
    def test_preprocessing_pipeline_transforms_data(self):
        """Test that preprocessing pipeline transforms data"""
        df = generate_stylesense_dataset(n_samples=100)
        X = df.drop('recommend', axis=1)
        
        pipeline = PreprocessingPipeline()
        X_transformed = pipeline.fit_transform(X)
        
        # Check that output is array-like
        assert hasattr(X_transformed, 'shape')
        assert X_transformed.shape[0] == 100
        # Output should have more features due to one-hot encoding and TF-IDF
        assert X_transformed.shape[1] > X.shape[1]
    
    def test_train_test_split(self):
        """Test train-test split functionality"""
        df = generate_stylesense_dataset(n_samples=100)
        X_train, X_test, y_train, y_test = create_train_test_split(df, test_size=0.2)
        
        assert len(X_train) == 80
        assert len(X_test) == 20
        assert len(y_train) == 80
        assert len(y_test) == 20
    
    def test_preprocess_data_complete_workflow(self):
        """Test complete preprocessing workflow"""
        df = generate_stylesense_dataset(n_samples=100)
        result = preprocess_data(df, test_size=0.2)
        
        assert 'X_train' in result
        assert 'X_test' in result
        assert 'y_train' in result
        assert 'y_test' in result
        assert 'pipeline' in result
        
        assert result['X_train'].shape[0] == 80
        assert result['X_test'].shape[0] == 20
    
    def test_pipeline_transform_consistency(self):
        """Test that pipeline transform is consistent"""
        df = generate_stylesense_dataset(n_samples=100)
        X_train, X_test, y_train, y_test = create_train_test_split(df, test_size=0.2)
        
        pipeline = PreprocessingPipeline()
        X_train_1 = pipeline.fit_transform(X_train)
        X_train_2 = pipeline.transform(X_train)
        
        # Should be identical when transforming same data
        np.testing.assert_array_almost_equal(X_train_1, X_train_2)


class TestModel:
    """Tests for model training and evaluation"""
    
    @pytest.fixture
    def preprocessed_data(self):
        """Fixture providing preprocessed data"""
        df = generate_stylesense_dataset(n_samples=200)
        return preprocess_data(df, test_size=0.2)
    
    def test_model_creation(self):
        """Test that models can be created"""
        for model_type in ['random_forest', 'gradient_boosting', 'logistic_regression']:
            model = RecommendationModel(model_type=model_type)
            assert model.model is not None
    
    def test_model_training(self, preprocessed_data):
        """Test that model can be trained"""
        model = RecommendationModel(model_type='random_forest')
        model.train(preprocessed_data['X_train'], preprocessed_data['y_train'])
        # Training should not raise an exception
        assert model.model is not None
    
    def test_model_prediction(self, preprocessed_data):
        """Test that trained model can make predictions"""
        model = RecommendationModel(model_type='random_forest')
        model.train(preprocessed_data['X_train'], preprocessed_data['y_train'])
        
        predictions = model.predict(preprocessed_data['X_test'])
        assert predictions.shape[0] == preprocessed_data['X_test'].shape[0]
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_model_predict_proba(self, preprocessed_data):
        """Test that model can output prediction probabilities"""
        model = RecommendationModel(model_type='random_forest')
        model.train(preprocessed_data['X_train'], preprocessed_data['y_train'])
        
        probabilities = model.predict_proba(preprocessed_data['X_test'])
        assert probabilities.shape[0] == preprocessed_data['X_test'].shape[0]
        assert probabilities.shape[1] == 2
        assert np.allclose(probabilities.sum(axis=1), 1.0)
    
    def test_model_evaluation(self, preprocessed_data):
        """Test model evaluation metrics"""
        model = RecommendationModel(model_type='random_forest')
        model.train(preprocessed_data['X_train'], preprocessed_data['y_train'])
        
        metrics = model.evaluate(preprocessed_data['X_test'], preprocessed_data['y_test'])
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 'roc_auc' in metrics
        assert 'confusion_matrix' in metrics
        
        # Check metric ranges
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['f1'] <= 1
        assert 0 <= metrics['roc_auc'] <= 1
    
    def test_model_save_and_load(self, preprocessed_data):
        """Test model saving and loading"""
        with tempfile.TemporaryDirectory() as tmpdir:
            model = RecommendationModel(model_type='random_forest')
            model.train(preprocessed_data['X_train'], preprocessed_data['y_train'])
            
            # Save model
            save_path = Path(tmpdir) / "test_model.pkl"
            model.save_model(save_path)
            
            assert save_path.exists()
            
            # Load model
            loaded_model = RecommendationModel.load_model(save_path)
            
            # Loaded model should make same predictions
            original_pred = model.predict(preprocessed_data['X_test'])
            loaded_pred = loaded_model.predict(preprocessed_data['X_test'])
            np.testing.assert_array_equal(original_pred, loaded_pred)
    
    def test_model_comparison(self, preprocessed_data):
        """Test model comparison functionality"""
        comparison = ModelComparison()
        comparison.train_models(
            preprocessed_data['X_train'],
            preprocessed_data['y_train'],
            model_types=['random_forest', 'logistic_regression']
        )
        comparison.evaluate_all(preprocessed_data['X_test'], preprocessed_data['y_test'])
        
        assert len(comparison.models) == 2
        assert len(comparison.results) == 2
        
        # Should be able to get best model
        best_model, best_name = comparison.get_best_model()
        assert best_model is not None
        assert best_name in ['random_forest', 'logistic_regression']


class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline from data generation to model evaluation"""
        # Generate data
        df = generate_stylesense_dataset(n_samples=100)
        
        # Preprocess
        result = preprocess_data(df, test_size=0.2)
        
        # Train model
        model = RecommendationModel(model_type='random_forest')
        model.train(result['X_train'], result['y_train'])
        
        # Evaluate
        metrics = model.evaluate(result['X_test'], result['y_test'])
        
        # Check that we have reasonable metrics
        assert metrics['accuracy'] > 0.5  # Better than random
        assert metrics['f1'] > 0
    
    def test_multiple_model_types_on_same_data(self):
        """Test that different model types work on same data"""
        df = generate_stylesense_dataset(n_samples=100)
        result = preprocess_data(df, test_size=0.2)
        
        model_types = ['random_forest', 'gradient_boosting', 'logistic_regression']
        results = {}
        
        for model_type in model_types:
            model = RecommendationModel(model_type=model_type)
            model.train(result['X_train'], result['y_train'])
            metrics = model.evaluate(result['X_test'], result['y_test'])
            results[model_type] = metrics['f1']
        
        # All models should produce some results
        assert len(results) == 3
        assert all(score > 0 for score in results.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

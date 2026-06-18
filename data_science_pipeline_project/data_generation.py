"""
Data generation script for StyleSense Fashion Review dataset
Creates a synthetic dataset with review text, numerical, and categorical features
"""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_stylesense_dataset(n_samples=1000, random_state=42):
    """
    Generate a synthetic StyleSense customer review dataset
    
    Features:
    - age: Customer age (numerical)
    - category: Product category (categorical)
    - price_range: Product price range (categorical)
    - rating: Review rating 1-5 (numerical)
    - review_text: Customer review text (text)
    - recommend: Whether customer recommends product (target, binary)
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Generated dataset
    """
    np.random.seed(random_state)
    
    categories = ['Dresses', 'Tops', 'Pants', 'Outerwear', 'Shoes', 'Accessories']
    price_ranges = ['Budget', 'Mid-Range', 'Premium', 'Luxury']
    
    # Sample review templates
    positive_reviews = [
        "This dress fits perfectly and looks amazing! Highly recommend.",
        "Great quality for the price. Very happy with my purchase.",
        "Love the style and the material is so comfortable.",
        "Excellent clothing, fast delivery, very satisfied.",
        "Perfect fit and beautiful color. Will buy again!",
        "Amazing product, exceeded my expectations.",
        "Best purchase I've made recently. Looks great!",
        "Super comfortable and stylish. Great value for money.",
        "The quality is excellent. Highly recommend to friends.",
        "Love it! Perfect for everyday wear."
    ]
    
    negative_reviews = [
        "Disappointed with the quality. Not as described.",
        "Poor fit and the material is uncomfortable.",
        "The color is different from the picture.",
        "Not worth the price. Quality is mediocre.",
        "Returned it. Doesn't fit as expected.",
        "Cheap materials and poor stitching.",
        "Very disappointed. Will not buy again.",
        "The fabric is too thin and feels cheap.",
        "Not flattering and poor quality.",
        "Waste of money. Very disappointed."
    ]
    
    neutral_reviews = [
        "It's okay. Nothing special but decent.",
        "Average quality for the price.",
        "Nice design but could be better quality.",
        "Acceptable but has some flaws.",
        "Not bad, but not great either."
    ]
    
    data = {
        'age': np.random.randint(18, 75, n_samples),
        'category': np.random.choice(categories, n_samples),
        'price_range': np.random.choice(price_ranges, n_samples),
        'rating': np.random.randint(1, 6, n_samples),
    }
    
    # Generate reviews and recommendations based on rating
    reviews = []
    recommendations = []
    
    for rating in data['rating']:
        if rating >= 4:
            reviews.append(np.random.choice(positive_reviews))
            # Higher probability of recommendation for high ratings
            recommendation = np.random.choice([1, 0], p=[0.85, 0.15])
        elif rating == 3:
            reviews.append(np.random.choice(neutral_reviews))
            recommendation = np.random.choice([1, 0], p=[0.5, 0.5])
        else:
            reviews.append(np.random.choice(negative_reviews))
            # Higher probability of no recommendation for low ratings
            recommendation = np.random.choice([1, 0], p=[0.1, 0.9])
        
        recommendations.append(recommendation)
    
    data['review_text'] = reviews
    data['recommend'] = recommendations
    
    return pd.DataFrame(data)


def save_dataset(df, filepath):
    """Save dataset to CSV"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to {filepath}")
    return filepath


def load_or_create_dataset(data_dir, n_samples=1000):
    """Load existing dataset or create new one"""
    csv_path = Path(data_dir) / "stylesense_reviews.csv"
    
    if csv_path.exists():
        print(f"Loading existing dataset from {csv_path}")
        return pd.read_csv(csv_path)
    else:
        print(f"Creating new dataset with {n_samples} samples...")
        df = generate_stylesense_dataset(n_samples)
        save_dataset(df, csv_path)
        return df


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Generate and save dataset
    df = generate_stylesense_dataset(1000)
    save_dataset(df, data_dir / "stylesense_reviews.csv")
    
    print("\nDataset Overview:")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nRecommendation distribution:\n{df['recommend'].value_counts()}")

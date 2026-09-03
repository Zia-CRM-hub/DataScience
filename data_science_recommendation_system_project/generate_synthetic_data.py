"""
Generate synthetic data for the recommendation system notebook.
Creates realistic user interaction and article data for demonstration.
"""

import os
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Create data directory if it doesn't exist
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ==============================================================================
# 1. Generate Articles
# ==============================================================================
n_articles = 150

article_topics = [
    "Machine Learning", "Deep Learning", "Data Science", "Python", "Statistics",
    "Natural Language Processing", "Computer Vision", "Cloud Computing", "Big Data",
    "Database Management", "Web Development", "DevOps", "Security", "IoT",
    "Blockchain", "Time Series", "Recommendation Systems", "Neural Networks"
]

article_data = {
    'article_id': range(1, n_articles + 1),
    'title': [f"{np.random.choice(article_topics)} Article {i}" for i in range(1, n_articles + 1)],
    'author': [f"Author_{np.random.randint(1, 30)}" for _ in range(n_articles)],
    'publish_date': pd.date_range(start='2022-01-01', periods=n_articles, freq='D'),
    'views': np.random.exponential(100, n_articles).astype(int) + 10
}

articles_df = pd.DataFrame(article_data)
articles_df.to_csv(os.path.join(DATA_DIR, 'articles.csv'), index=False)
print(f"✓ Generated {len(articles_df)} articles")

# ==============================================================================
# 2. Generate User-Item Interactions
# ==============================================================================
n_users = 200
n_interactions = 2500

interactions_data = {
    'user_id': np.random.choice(range(1, n_users + 1), n_interactions),
    'article_id': np.random.choice(range(1, n_articles + 1), n_interactions),
    'interaction_type': np.random.choice(['view', 'like', 'share', 'comment'], n_interactions),
    'timestamp': pd.date_range(start='2023-01-01', periods=n_interactions, freq='H')
}

interactions_df = pd.DataFrame(interactions_data)
interactions_df = interactions_df.drop_duplicates(subset=['user_id', 'article_id'])
interactions_df.to_csv(os.path.join(DATA_DIR, 'user_item_interactions.csv'), index=False)
print(f"✓ Generated {len(interactions_df)} user-article interactions")

# ==============================================================================
# 3. Generate Article Community Data (Tags/Topics/Categories)
# ==============================================================================
categories = [
    "python", "machine learning", "data analysis", "deep learning",
    "statistics", "nlp", "computer vision", "data engineering",
    "visualization", "optimization", "clustering", "classification",
    "regression", "neural networks", "algorithms", "databases"
]

articles_community_data = []
for article_id in range(1, n_articles + 1):
    # Each article gets 2-5 random tags
    n_tags = np.random.randint(2, 6)
    tags = np.random.choice(categories, n_tags, replace=False)
    
    for tag in tags:
        articles_community_data.append({
            'article_id': article_id,
            'tag': tag,
            'community_score': np.random.uniform(0.5, 1.0)
        })

articles_community_df = pd.DataFrame(articles_community_data)
articles_community_df.to_csv(os.path.join(DATA_DIR, 'articles_community.csv'), index=False)
print(f"✓ Generated {len(articles_community_df)} article-tag mappings")

# ==============================================================================
# Print Summary Statistics
# ==============================================================================
print("\n" + "="*60)
print("SYNTHETIC DATA SUMMARY")
print("="*60)
print(f"Users: {interactions_df['user_id'].nunique()}")
print(f"Articles: {len(articles_df)}")
print(f"Total Interactions: {len(interactions_df)}")
print(f"Sparsity: {1 - len(interactions_df)/(interactions_df['user_id'].nunique() * len(articles_df)):.4f}")
print(f"Avg interactions per user: {len(interactions_df) / interactions_df['user_id'].nunique():.2f}")
print(f"Avg interactions per article: {len(interactions_df) / len(articles_df):.2f}")
print(f"Community tags: {len(articles_community_df)}")
print(f"Unique tags: {articles_community_df['tag'].nunique()}")
print("="*60)

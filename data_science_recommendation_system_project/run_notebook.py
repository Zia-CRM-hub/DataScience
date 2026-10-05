"""
Execute the Recommendation System notebook with synthetic data.
Runs all cells and captures output to a results file.
"""

import os
import sys
import subprocess
import json
from datetime import datetime

# Change to project directory
project_dir = "data_science_recommendation_system_project"
os.chdir(project_dir)

print("="*80)
print("RECOMMENDATION SYSTEM NOTEBOOK EXECUTION")
print("="*80)
print(f"Timestamp: {datetime.now().isoformat()}")
print(f"Working Directory: {os.getcwd()}")
print()

# Step 1: Generate synthetic data
print("[STEP 1] Generating synthetic data...")
print("-" * 80)
exec(open('generate_synthetic_data.py').read())
print()

# Step 2: Install requirements if needed
print("[STEP 2] Checking dependencies...")
print("-" * 80)
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.decomposition import TruncatedSVD
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    import matplotlib.pyplot as plt
    import seaborn as sns
    print("✓ All required packages are available")
except ImportError as e:
    print(f"✗ Missing package: {e}")
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
print()

# Step 3: Execute the notebook programmatically
print("[STEP 3] Executing notebook cells...")
print("-" * 80)

# Import after dependencies are confirmed
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set(style="whitegrid")

DATA_DIR = "data"
INTERACTIONS_FILE = os.path.join(DATA_DIR, "user_item_interactions.csv")
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.csv")
ARTICLES_COMMUNITY_FILE = os.path.join(DATA_DIR, "articles_community.csv")

# ============================================================================
# PART I: EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n### PART I: EXPLORATORY DATA ANALYSIS ###\n")

# Load data
interactions = pd.read_csv(INTERACTIONS_FILE)
articles = pd.read_csv(ARTICLES_FILE)
articles_community = pd.read_csv(ARTICLES_COMMUNITY_FILE)

print("Data loaded successfully!")
print(f"  Interactions shape: {interactions.shape}")
print(f"  Articles shape: {articles.shape}")
print(f"  Articles Community shape: {articles_community.shape}")

# Calculate exploration statistics
def calculate_exploration_statistics(interactions_df, articles_df):
    """Calculate fundamental statistics about the dataset."""
    interaction_counts = interactions_df['user_id'].value_counts()
    article_interaction_counts = interactions_df['article_id'].value_counts()
    
    return {
        'unique_users': interactions_df['user_id'].nunique(),
        'unique_articles': interactions_df['article_id'].nunique(),
        'total_articles': len(articles_df),
        'user_article_interactions': len(interactions_df),
        'median_val': interaction_counts.median(),
        'max_views_by_user': interaction_counts.max(),
        'max_views': article_interaction_counts.max(),
        'most_viewed_article_id': article_interaction_counts.idxmax()
    }

sol_1_dict = calculate_exploration_statistics(interactions, articles)

print("\n=== EXPLORATORY DATA ANALYSIS RESULTS ===")
for key, value in sol_1_dict.items():
    print(f"{key}: {value}")

# ============================================================================
# PART II: RANK-BASED RECOMMENDATIONS
# ============================================================================
print("\n\n### PART II: RANK-BASED RECOMMENDATIONS ###\n")

def get_top_article_ids(interactions_df, n=10):
    """Get top N article IDs by interaction count."""
    return interactions_df['article_id'].value_counts().head(n).index.tolist()

def get_top_article_names(interactions_df, articles_df, n=10):
    """Get top N article names by interaction count."""
    top_ids = get_top_article_ids(interactions_df, n)
    top_articles = articles_df[articles_df['article_id'].isin(top_ids)]
    return top_articles.set_index('article_id').loc[top_ids]['title'].tolist()

def get_top_recommendations(interactions_df, articles_df, n=10):
    """Get top articles (fallback for new users)."""
    top_ids = get_top_article_ids(interactions_df, n)
    return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']].head(n)

top_10_ids = get_top_article_ids(interactions, 10)
top_10_names = get_top_article_names(interactions, articles, 10)

print("=== TOP 10 MOST POPULAR ARTICLES ===")
for i, (aid, title) in enumerate(zip(top_10_ids, top_10_names), 1):
    count = interactions[interactions['article_id'] == aid].shape[0]
    print(f"{i}. {title} (Interactions: {count})")

# ============================================================================
# PART III: USER-USER COLLABORATIVE FILTERING
# ============================================================================
print("\n\n### PART III: USER-USER COLLABORATIVE FILTERING ###\n")

def create_user_item_matrix(interactions_df):
    """Create binary user-item interaction matrix."""
    matrix = interactions_df.pivot_table(
        index='user_id', columns='article_id', aggfunc='size', fill_value=0
    )
    return (matrix > 0).astype(int)

user_item_matrix = create_user_item_matrix(interactions)
print(f"User-Item Matrix Shape: {user_item_matrix.shape}")
sparsity = 1 - (user_item_matrix > 0).sum().sum() / (user_item_matrix.shape[0] * user_item_matrix.shape[1])
print(f"Sparsity: {sparsity:.4f}")

def find_similar_users(user_id, user_item_matrix, n_similar=5):
    """Find N most similar users using cosine similarity."""
    if user_id not in user_item_matrix.index:
        return None
    
    user_vector = user_item_matrix.loc[user_id].values.reshape(1, -1)
    similarities = cosine_similarity(user_vector, user_item_matrix.values)[0]
    sim_series = pd.Series(similarities, index=user_item_matrix.index)
    return sim_series.drop(user_id).sort_values(ascending=False).head(n_similar)

def recommend_user_user_collaborative(user_id, interactions_df, user_item_matrix, articles_df, n=10):
    """Generate CF recommendations for a user."""
    if user_id not in user_item_matrix.index:
        return get_top_recommendations(interactions_df, articles_df, n)
    
    similar_users = find_similar_users(user_id, user_item_matrix, 10)
    if similar_users is None:
        return get_top_recommendations(interactions_df, articles_df, n)
    
    similar_user_ids = similar_users.index.tolist()
    sim_interactions = interactions_df[interactions_df['user_id'].isin(similar_user_ids)]
    user_articles = set(interactions_df[interactions_df['user_id'] == user_id]['article_id'])
    
    candidate_articles = sim_interactions['article_id'].value_counts()
    recommended = [aid for aid in candidate_articles.index if aid not in user_articles]
    
    return articles_df[articles_df['article_id'].isin(recommended[:n])][['article_id', 'title']]

test_user = interactions['user_id'].iloc[0]
similar = find_similar_users(test_user, user_item_matrix, 5)

print(f"Similar Users to {test_user}:")
for user, sim in similar.items():
    print(f"  User {user}: {sim:.4f}")

cf_recs = recommend_user_user_collaborative(test_user, interactions, user_item_matrix, articles, 5)
print(f"\nCollaborative Filtering Recommendations for User {test_user}:")
print(cf_recs.to_string())

# ============================================================================
# PART IV: CONTENT-BASED RECOMMENDATIONS
# ============================================================================
print("\n\n### PART IV: CONTENT-BASED RECOMMENDATIONS ###\n")

def prepare_article_content(articles_df, articles_community_df):
    """Combine article content for TF-IDF."""
    merged = articles_df.merge(articles_community_df, on='article_id', how='left')
    text_columns = [col for col in merged.columns if col not in ['article_id', 'user_id']]
    merged['combined_content'] = merged[text_columns].fillna('').agg(' '.join, axis=1)
    merged['combined_content'] = merged['combined_content'].str.lower()
    return merged.drop_duplicates(subset='article_id').reset_index(drop=True)

article_content_df = prepare_article_content(articles, articles_community)
print(f"Articles with content: {len(article_content_df)}")

def create_tfidf_matrix(article_df):
    """Create TF-IDF vectors and similarity matrix."""
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2, max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(article_df['combined_content'].fillna(''))
    similarity = cosine_similarity(tfidf_matrix)
    return vectorizer, tfidf_matrix, similarity

vectorizer, tfidf_matrix, article_similarity = create_tfidf_matrix(article_content_df)
print(f"TF-IDF Matrix Shape: {tfidf_matrix.shape}")
print(f"Features: {tfidf_matrix.shape[1]}")

def find_optimal_clusters(tfidf_matrix, max_k=15):
    """Find optimal number of clusters using silhouette score."""
    silhouette_scores = []
    k_values = range(2, min(max_k, tfidf_matrix.shape[0]))
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tfidf_matrix)
        score = silhouette_score(tfidf_matrix, labels)
        silhouette_scores.append(score)
    
    best_idx = np.argmax(silhouette_scores)
    return list(k_values)[best_idx], silhouette_scores, list(k_values)

best_k, sil_scores, k_vals = find_optimal_clusters(tfidf_matrix)
print(f"\nOptimal Clusters: {best_k}")
print(f"Best Silhouette Score: {max(sil_scores):.4f}")

def recommend_content_based(user_id, interactions_df, article_content_df, similarity_matrix, articles_df, n=10):
    """Generate content-based recommendations."""
    user_articles = interactions_df[interactions_df['user_id'] == user_id]['article_id'].unique()
    
    if len(user_articles) == 0:
        return get_top_recommendations(interactions_df, articles_df, n)
    
    article_ids = article_content_df['article_id'].tolist()
    id_to_idx = {aid: idx for idx, aid in enumerate(article_ids)}
    
    valid_indices = [id_to_idx[aid] for aid in user_articles if aid in id_to_idx]
    if not valid_indices:
        return get_top_recommendations(interactions_df, articles_df, n)
    
    sim_scores = np.zeros(similarity_matrix.shape[0])
    for idx in valid_indices:
        sim_scores += similarity_matrix[idx]
    sim_scores /= len(valid_indices)
    
    ranked = np.argsort(-sim_scores)
    recs = [article_ids[idx] for idx in ranked if article_ids[idx] not in user_articles]
    
    return articles_df[articles_df['article_id'].isin(recs[:n])][['article_id', 'title']]

content_recs = recommend_content_based(test_user, interactions, article_content_df, article_similarity, articles, 5)
print(f"\nContent-Based Recommendations for User {test_user}:")
print(content_recs.to_string())

# ============================================================================
# PART V: MATRIX FACTORIZATION (SVD)
# ============================================================================
print("\n\n### PART V: MATRIX FACTORIZATION (SVD) ###\n")

def perform_svd(user_item_matrix, n_components=20):
    """Perform SVD factorization with safe component bounds."""
    max_components = max(1, min(user_item_matrix.shape) - 1)
    effective_components = min(n_components, max_components)

    svd = TruncatedSVD(n_components=effective_components, random_state=42, n_iter=100)
    U = svd.fit_transform(user_item_matrix)

    return {
        'model': svd,
        'U': U,
        'sigma': svd.singular_values_,
        'vt': svd.components_,
        'variance': np.cumsum(svd.explained_variance_ratio_),
        'n_components': effective_components,
    }

svd_result = perform_svd(user_item_matrix, 20)
print(f"SVD Factorization:")
print(f"  Components used: {svd_result['n_components']}")
print(f"  U shape: {svd_result['U'].shape}")
print(f"  Sigma shape: {svd_result['sigma'].shape}")
print(f"  V^T shape: {svd_result['vt'].shape}")
print(f"  Variance explained: {svd_result['variance'][-1]:.4f}")

def recommend_svd_based(user_id, user_item_matrix, svd_result, articles_df, interactions_df, n=10):
    """Generate SVD-based recommendations."""
    user_ids = user_item_matrix.index.tolist()
    if user_id not in user_ids:
        return get_top_recommendations(interactions_df, articles_df, n)
    
    user_idx = user_ids.index(user_id)
    user_latent = svd_result['U'][user_idx]
    sigma_m = np.diag(svd_result['sigma'])
    pred_scores = user_latent @ sigma_m @ svd_result['vt']
    
    ranked = np.argsort(-pred_scores)
    user_articles = set(interactions_df[interactions_df['user_id'] == user_id]['article_id'])
    article_ids = user_item_matrix.columns.tolist()
    
    recs = [article_ids[idx] for idx in ranked if article_ids[idx] not in user_articles]
    return articles_df[articles_df['article_id'].isin(recs[:n])][['article_id', 'title']]

svd_recs = recommend_svd_based(test_user, user_item_matrix, svd_result, articles, interactions, 5)
print(f"\nSVD-Based Recommendations for User {test_user}:")
print(svd_recs.to_string())

# ============================================================================
# SUMMARY AND COMPARISON
# ============================================================================
print("\n\n### SUMMARY: RECOMMENDATION APPROACHES COMPARISON ###\n")

summary = """
RECOMMENDATION SYSTEM SUMMARY
=============================

1. RANK-BASED: Popular items for all users
   Pros: Simple, handles cold-start
   Cons: Not personalized

2. COLLABORATIVE FILTERING: Similar users -> their items
   Pros: Personalized, discovers new content
   Cons: Cold-start for new users, sparsity

3. CONTENT-BASED: Similar articles to user's history
   Pros: No new-item problem, interpretable
   Cons: Limited by content quality, filter bubble

4. MATRIX FACTORIZATION: Latent user/item factors
   Pros: Powerful predictions, handles sparsity
   Cons: Black-box, cold-start, complex tuning

TESTING METRICS:
- CTR (Click-Through Rate)
- Precision@K, Recall@K
- Coverage, Diversity
- User satisfaction

A/B TESTING STRATEGY:
- Control vs. treatment groups
- 2-4 week duration
- Statistical significance testing
- Success criteria: >5% CTR improvement

NEXT STEPS:
- Hybrid approaches combining methods
- Deep learning embeddings
- Temporal dynamics
- Continuous feedback loops
"""

print(summary)

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n\n### SAVING RESULTS ###\n")

results = {
    'execution_timestamp': datetime.now().isoformat(),
    'data_summary': {
        'unique_users': int(sol_1_dict['unique_users']),
        'unique_articles': int(sol_1_dict['unique_articles']),
        'total_interactions': int(sol_1_dict['user_article_interactions']),
        'sparsity': float(sparsity),
        'median_interactions_per_user': float(sol_1_dict['median_val']),
        'max_interactions_by_user': int(sol_1_dict['max_views_by_user']),
        'max_interactions_on_article': int(sol_1_dict['max_views']),
        'most_viewed_article_id': int(sol_1_dict['most_viewed_article_id'])
    },
    'top_10_articles': [
        {'rank': i+1, 'article_id': int(aid), 'title': name, 'interactions': int(interactions[interactions['article_id'] == aid].shape[0])}
        for i, (aid, name) in enumerate(zip(top_10_ids, top_10_names))
    ],
    'collaborative_filtering': {
        'test_user': int(test_user),
        'similar_users': {int(user): float(sim) for user, sim in similar.items()},
        'recommendations': cf_recs[['article_id', 'title']].to_dict('records')
    },
    'content_based': {
        'test_user': int(test_user),
        'optimal_clusters': int(best_k),
        'silhouette_score': float(max(sil_scores)),
        'tfidf_features': int(tfidf_matrix.shape[1]),
        'recommendations': content_recs[['article_id', 'title']].to_dict('records')
    },
    'matrix_factorization': {
        'test_user': int(test_user),
        'svd_components': int(svd_result['n_components']),
        'variance_explained': float(svd_result['variance'][-1]),
        'recommendations': svd_recs[['article_id', 'title']].to_dict('records')
    }
}

# Save JSON results
output_file = 'notebook_output_results.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"✓ Results saved to: {output_file}")

# Save detailed text report
report_file = 'notebook_execution_report.txt'
with open(report_file, 'w') as f:
    f.write("="*80 + "\n")
    f.write("RECOMMENDATION SYSTEM NOTEBOOK EXECUTION REPORT\n")
    f.write("="*80 + "\n\n")
    f.write(f"Execution Timestamp: {datetime.now().isoformat()}\n\n")
    
    f.write("PART I: EXPLORATORY DATA ANALYSIS\n")
    f.write("-"*80 + "\n")
    for key, value in sol_1_dict.items():
        f.write(f"{key}: {value}\n")
    
    f.write("\n\nPART II: RANK-BASED RECOMMENDATIONS (Top 10)\n")
    f.write("-"*80 + "\n")
    for i, (aid, title) in enumerate(zip(top_10_ids, top_10_names), 1):
        count = interactions[interactions['article_id'] == aid].shape[0]
        f.write(f"{i}. {title} (ID: {aid}, Interactions: {count})\n")
    
    f.write("\n\nPART III: COLLABORATIVE FILTERING\n")
    f.write("-"*80 + "\n")
    f.write(f"Test User: {test_user}\n")
    f.write(f"Similar Users (Top 5):\n")
    for user, sim in similar.items():
        f.write(f"  User {user}: {sim:.4f}\n")
    f.write(f"\nRecommendations:\n")
    f.write(cf_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n\nPART IV: CONTENT-BASED RECOMMENDATIONS\n")
    f.write("-"*80 + "\n")
    f.write(f"Optimal Clusters: {best_k}\n")
    f.write(f"Best Silhouette Score: {max(sil_scores):.4f}\n")
    f.write(f"TF-IDF Features: {tfidf_matrix.shape[1]}\n")
    f.write(f"\nRecommendations for User {test_user}:\n")
    f.write(content_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n\nPART V: MATRIX FACTORIZATION (SVD)\n")
    f.write("-"*80 + "\n")
    f.write(f"SVD Components: {svd_result['n_components']}\n")
    f.write(f"Variance Explained: {svd_result['variance'][-1]:.4f}\n")
    f.write(f"\nRecommendations for User {test_user}:\n")
    f.write(svd_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n" + "="*80 + "\n")
    f.write("SUMMARY: RECOMMENDATION APPROACHES COMPARISON\n")
    f.write("="*80 + "\n")
    f.write(summary)

print(f"✓ Report saved to: {report_file}")

print("\n" + "="*80)
print("NOTEBOOK EXECUTION COMPLETED SUCCESSFULLY")
print("="*80)
print(f"\nOutput Files:")
print(f"  1. {output_file}")
print(f"  2. {report_file}")
print(f"\nData Files Generated:")
print(f"  1. data/articles.csv")
print(f"  2. data/user_item_interactions.csv")
print(f"  3. data/articles_community.csv")

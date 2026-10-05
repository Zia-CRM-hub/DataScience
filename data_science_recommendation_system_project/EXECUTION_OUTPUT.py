"""
RECOMMENDATION SYSTEM - COMPLETE EXECUTION OUTPUT
Synthetic Data Generation + All 5 Recommendation Approaches
Execution Date: 2026-09-03
================================================================================
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

print("="*90)
print("RECOMMENDATION SYSTEM: IBM COMMUNITY - COMPLETE EXECUTION")
print("="*90)
print(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ==============================================================================
# STEP 1: GENERATE SYNTHETIC DATA
# ==============================================================================
print("[STEP 1/6] GENERATING SYNTHETIC DATA")
print("-"*90)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

# Generate Articles
n_articles = 150
article_topics = [
    "Machine Learning", "Deep Learning", "Data Science", "Python", "Statistics",
    "Natural Language Processing", "Computer Vision", "Cloud Computing", "Big Data",
    "Database Management", "Web Development", "DevOps", "Security", "IoT",
    "Blockchain", "Time Series", "Recommendation Systems", "Neural Networks"
]

articles_data = {
    'article_id': range(1, n_articles + 1),
    'title': [f"{np.random.choice(article_topics)} Article {i}" for i in range(1, n_articles + 1)],
    'author': [f"Author_{np.random.randint(1, 30)}" for _ in range(n_articles)],
    'publish_date': pd.date_range(start='2022-01-01', periods=n_articles, freq='D'),
    'views': np.random.exponential(100, n_articles).astype(int) + 10
}

articles = pd.DataFrame(articles_data)
articles.to_csv(os.path.join(DATA_DIR, 'articles.csv'), index=False)

# Generate User-Item Interactions
n_users = 200
n_interactions = 2500

interactions_data = {
    'user_id': np.random.choice(range(1, n_users + 1), n_interactions),
    'article_id': np.random.choice(range(1, n_articles + 1), n_interactions),
    'interaction_type': np.random.choice(['view', 'like', 'share', 'comment'], n_interactions),
    'timestamp': pd.date_range(start='2023-01-01', periods=n_interactions, freq='H')
}

interactions = pd.DataFrame(interactions_data)
interactions = interactions.drop_duplicates(subset=['user_id', 'article_id'])
interactions.to_csv(os.path.join(DATA_DIR, 'user_item_interactions.csv'), index=False)

# Generate Article Community Data
categories = [
    "python", "machine learning", "data analysis", "deep learning",
    "statistics", "nlp", "computer vision", "data engineering",
    "visualization", "optimization", "clustering", "classification",
    "regression", "neural networks", "algorithms", "databases"
]

articles_community_data = []
for article_id in range(1, n_articles + 1):
    n_tags = np.random.randint(2, 6)
    tags = np.random.choice(categories, n_tags, replace=False)
    for tag in tags:
        articles_community_data.append({
            'article_id': article_id,
            'tag': tag,
            'community_score': np.random.uniform(0.5, 1.0)
        })

articles_community = pd.DataFrame(articles_community_data)
articles_community.to_csv(os.path.join(DATA_DIR, 'articles_community.csv'), index=False)

print(f"✓ Articles generated: {len(articles)}")
print(f"✓ User-Article interactions: {len(interactions)}")
print(f"✓ Article-Tag mappings: {len(articles_community)}")
print()

# ==============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS
# ==============================================================================
print("[STEP 2/6] PART I: EXPLORATORY DATA ANALYSIS")
print("-"*90)

def calculate_exploration_statistics(interactions_df, articles_df):
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

print("\n=== EXPLORATION STATISTICS ===")
print(f"Unique Users:                  {sol_1_dict['unique_users']}")
print(f"Unique Articles (interacted):  {sol_1_dict['unique_articles']}")
print(f"Total Articles in Catalog:     {sol_1_dict['total_articles']}")
print(f"Total User-Article Interactions: {sol_1_dict['user_article_interactions']}")
print(f"Median Interactions per User:  {sol_1_dict['median_val']:.0f}")
print(f"Max Interactions by Single User: {sol_1_dict['max_views_by_user']}")
print(f"Max Interactions on Single Article: {sol_1_dict['max_views']}")
print(f"Most Viewed Article ID:        {sol_1_dict['most_viewed_article_id']}")

sparsity = 1 - len(interactions) / (sol_1_dict['unique_users'] * sol_1_dict['unique_articles'])
print(f"Matrix Sparsity:               {sparsity:.4f}")
print()

# ==============================================================================
# STEP 3: RANK-BASED RECOMMENDATIONS
# ==============================================================================
print("[STEP 3/6] PART II: RANK-BASED RECOMMENDATIONS")
print("-"*90)

def get_top_article_ids(interactions_df, n=10):
    return interactions_df['article_id'].value_counts().head(n).index.tolist()

def get_top_article_names(interactions_df, articles_df, n=10):
    top_ids = get_top_article_ids(interactions_df, n)
    top_articles = articles_df[articles_df['article_id'].isin(top_ids)]
    return top_articles.set_index('article_id').loc[top_ids]['title'].tolist()

top_10_ids = get_top_article_ids(interactions, 10)
top_10_names = get_top_article_names(interactions, articles, 10)

print("\n=== TOP 10 MOST POPULAR ARTICLES ===")
print(f"{'Rank':<6} {'Article ID':<12} {'Interactions':<15} {'Title':<50}")
print("-"*90)
for i, (aid, title) in enumerate(zip(top_10_ids, top_10_names), 1):
    count = interactions[interactions['article_id'] == aid].shape[0]
    print(f"{i:<6} {aid:<12} {count:<15} {title[:45]:<50}")
print()

# ==============================================================================
# STEP 4: COLLABORATIVE FILTERING
# ==============================================================================
print("[STEP 4/6] PART III: USER-USER COLLABORATIVE FILTERING")
print("-"*90)

def create_user_item_matrix(interactions_df):
    matrix = interactions_df.pivot_table(
        index='user_id', columns='article_id', aggfunc='size', fill_value=0
    )
    return (matrix > 0).astype(int)

user_item_matrix = create_user_item_matrix(interactions)

print(f"\nUser-Item Matrix Shape: {user_item_matrix.shape}")
print(f"Matrix Sparsity: {(1 - (user_item_matrix > 0).sum().sum() / (user_item_matrix.shape[0] * user_item_matrix.shape[1])):.4f}")

def find_similar_users(user_id, user_item_matrix, n_similar=5):
    if user_id not in user_item_matrix.index:
        return None
    
    user_vector = user_item_matrix.loc[user_id].values.reshape(1, -1)
    similarities = cosine_similarity(user_vector, user_item_matrix.values)[0]
    sim_series = pd.Series(similarities, index=user_item_matrix.index)
    return sim_series.drop(user_id).sort_values(ascending=False).head(n_similar)

def recommend_user_user_collaborative(user_id, interactions_df, user_item_matrix, articles_df, n=10):
    if user_id not in user_item_matrix.index:
        top_ids = get_top_article_ids(interactions_df, n)
        return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']]
    
    similar_users = find_similar_users(user_id, user_item_matrix, 10)
    if similar_users is None or len(similar_users) == 0:
        top_ids = get_top_article_ids(interactions_df, n)
        return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']]
    
    similar_user_ids = similar_users.index.tolist()
    sim_interactions = interactions_df[interactions_df['user_id'].isin(similar_user_ids)]
    user_articles = set(interactions_df[interactions_df['user_id'] == user_id]['article_id'])
    
    candidate_articles = sim_interactions['article_id'].value_counts()
    recommended = [aid for aid in candidate_articles.index if aid not in user_articles]
    
    return articles_df[articles_df['article_id'].isin(recommended[:n])][['article_id', 'title']]

test_user = interactions['user_id'].iloc[0]
similar = find_similar_users(test_user, user_item_matrix, 5)

print(f"\n=== SIMILAR USERS TO USER {test_user} ===")
print(f"{'User ID':<10} {'Similarity Score':<20}")
print("-"*90)
for user, sim in similar.items():
    print(f"{user:<10} {sim:.4f}")

cf_recs = recommend_user_user_collaborative(test_user, interactions, user_item_matrix, articles, 5)

print(f"\n=== COLLABORATIVE FILTERING RECOMMENDATIONS FOR USER {test_user} ===")
print(f"{'Article ID':<12} {'Title':<75}")
print("-"*90)
for idx, row in cf_recs.iterrows():
    print(f"{row['article_id']:<12} {row['title'][:72]:<75}")
print()

# ==============================================================================
# STEP 5: CONTENT-BASED RECOMMENDATIONS
# ==============================================================================
print("[STEP 5/6] PART IV: CONTENT-BASED RECOMMENDATIONS")
print("-"*90)

def prepare_article_content(articles_df, articles_community_df):
    merged = articles_df.merge(articles_community_df, on='article_id', how='left')
    text_columns = [col for col in merged.columns if col not in ['article_id', 'user_id']]
    merged['combined_content'] = merged[text_columns].fillna('').agg(' '.join, axis=1)
    merged['combined_content'] = merged['combined_content'].str.lower()
    return merged.drop_duplicates(subset='article_id').reset_index(drop=True)

article_content_df = prepare_article_content(articles, articles_community)

def create_tfidf_matrix(article_df):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2, max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(article_df['combined_content'].fillna(''))
    similarity = cosine_similarity(tfidf_matrix)
    return vectorizer, tfidf_matrix, similarity

vectorizer, tfidf_matrix, article_similarity = create_tfidf_matrix(article_content_df)

print(f"\nTF-IDF Matrix Shape: {tfidf_matrix.shape}")
print(f"Number of Features: {tfidf_matrix.shape[1]}")

def find_optimal_clusters(tfidf_matrix, max_k=15):
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

print(f"\n=== CLUSTERING ANALYSIS ===")
print(f"Optimal Number of Clusters: {best_k}")
print(f"Best Silhouette Score: {max(sil_scores):.4f}")

print(f"\n=== SILHOUETTE SCORES BY K ===")
print(f"{'K Value':<10} {'Silhouette Score':<20}")
print("-"*90)
for k, score in zip(k_vals[:10], sil_scores[:10]):
    print(f"{k:<10} {score:.4f}")

def recommend_content_based(user_id, interactions_df, article_content_df, similarity_matrix, articles_df, n=10):
    user_articles = interactions_df[interactions_df['user_id'] == user_id]['article_id'].unique()
    
    if len(user_articles) == 0:
        top_ids = get_top_article_ids(interactions_df, n)
        return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']]
    
    article_ids = article_content_df['article_id'].tolist()
    id_to_idx = {aid: idx for idx, aid in enumerate(article_ids)}
    
    valid_indices = [id_to_idx[aid] for aid in user_articles if aid in id_to_idx]
    if not valid_indices:
        top_ids = get_top_article_ids(interactions_df, n)
        return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']]
    
    sim_scores = np.zeros(similarity_matrix.shape[0])
    for idx in valid_indices:
        sim_scores += similarity_matrix[idx]
    sim_scores /= len(valid_indices)
    
    ranked = np.argsort(-sim_scores)
    recs = [article_ids[idx] for idx in ranked if article_ids[idx] not in user_articles]
    
    return articles_df[articles_df['article_id'].isin(recs[:n])][['article_id', 'title']]

content_recs = recommend_content_based(test_user, interactions, article_content_df, article_similarity, articles, 5)

print(f"\n=== CONTENT-BASED RECOMMENDATIONS FOR USER {test_user} ===")
print(f"{'Article ID':<12} {'Title':<75}")
print("-"*90)
for idx, row in content_recs.iterrows():
    print(f"{row['article_id']:<12} {row['title'][:72]:<75}")
print()

# ==============================================================================
# STEP 6: MATRIX FACTORIZATION (SVD)
# ==============================================================================
print("[STEP 6/6] PART V: MATRIX FACTORIZATION (SVD)")
print("-"*90)

def perform_svd(user_item_matrix, n_components=20):
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

print(f"\n=== SVD FACTORIZATION RESULTS ===")
print(f"Components Used: {svd_result['n_components']}")
print(f"U Shape (User Factors): {svd_result['U'].shape}")
print(f"Sigma Shape (Singular Values): {svd_result['sigma'].shape}")
print(f"V^T Shape (Item Factors): {svd_result['vt'].shape}")
print(f"Total Variance Explained: {svd_result['variance'][-1]:.4f}")

print(f"\n=== VARIANCE EXPLAINED BY COMPONENTS ===")
print(f"{'Component #':<15} {'Cumulative Variance':<20}")
print("-"*90)
for i in range(0, min(10, len(svd_result['variance']))):
    print(f"{i+1:<15} {svd_result['variance'][i]:.4f}")

def recommend_svd_based(user_id, user_item_matrix, svd_result, articles_df, interactions_df, n=10):
    user_ids = user_item_matrix.index.tolist()
    if user_id not in user_ids:
        top_ids = get_top_article_ids(interactions_df, n)
        return articles_df[articles_df['article_id'].isin(top_ids)][['article_id', 'title']]
    
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

print(f"\n=== SVD-BASED RECOMMENDATIONS FOR USER {test_user} ===")
print(f"{'Article ID':<12} {'Title':<75}")
print("-"*90)
for idx, row in svd_recs.iterrows():
    print(f"{row['article_id']:<12} {row['title'][:72]:<75}")
print()

# ==============================================================================
# SUMMARY AND COMPARISON
# ==============================================================================
print("="*90)
print("SUMMARY: RECOMMENDATION APPROACHES COMPARISON")
print("="*90)

summary_text = """
1. RANK-BASED RECOMMENDATIONS
   ├─ Approach: Most popular items for all users
   ├─ Pros: Simple, handles cold-start, no computation needed
   ├─ Cons: Not personalized, same for all users
   └─ Use Case: New users with no interaction history

2. COLLABORATIVE FILTERING (User-User)
   ├─ Approach: Find similar users, recommend their articles
   ├─ Pros: Personalized, discovers new content, no content analysis needed
   ├─ Cons: Cold-start problem, data sparsity, similarity computation
   └─ Use Case: Established users with interaction history

3. CONTENT-BASED RECOMMENDATIONS
   ├─ Approach: Recommend articles similar to user's history
   ├─ Pros: No new-item problem, interpretable, works with new articles
   ├─ Cons: Limited by content quality, filter bubble risk
   └─ Use Case: Articles with rich metadata/descriptions

4. MATRIX FACTORIZATION (SVD)
   ├─ Approach: Discover latent factors in user-item interactions
   ├─ Pros: Powerful predictions, handles sparsity, discovers patterns
   ├─ Cons: Black-box model, cold-start, parameter tuning required
   └─ Use Case: Large datasets with sparse interactions

HYBRID APPROACH (Recommended):
   ├─ Combine multiple methods with weighted ensemble
   ├─ Use rank-based for new users (cold-start)
   ├─ Use collaborative filtering for established users
   ├─ Add content-based signals for diversity
   └─ Score with SVD factors for better predictions

TESTING & EVALUATION METRICS:
   ├─ Precision@K: Fraction of recommended items that are relevant
   ├─ Recall@K: Fraction of relevant items that are recommended
   ├─ Coverage: Percentage of catalog recommended
   ├─ Diversity: Variety in recommendations
   ├─ Novelty: How new/surprising recommendations are
   └─ User Engagement: Click-through rate, time spent, conversions

A/B TESTING STRATEGY:
   ├─ Test Duration: 2-4 weeks minimum
   ├─ Sample Size: Large enough for statistical significance
   ├─ Success Criteria: >5% improvement in CTR or engagement
   ├─ Metrics: Conversion rate, user retention, satisfaction
   └─ Multi-armed bandit: Continuously optimize recommendations

NEXT STEPS:
   ├─ Implement hybrid recommendation model
   ├─ Deep learning embeddings (Word2Vec, FastText)
   ├─ Add temporal dynamics (recency weighting)
   ├─ Incorporate explicit ratings/feedback
   ├─ Real-time feedback loops for continuous learning
   └─ A/B test different algorithms
"""

print(summary_text)

# ==============================================================================
# SAVE RESULTS
# ==============================================================================
print("="*90)
print("SAVING RESULTS")
print("="*90)

results = {
    'execution_info': {
        'timestamp': datetime.now().isoformat(),
        'notebook': 'recommendationsystem_ibmcommunity_analysis.ipynb'
    },
    'part_1_eda': {
        'unique_users': int(sol_1_dict['unique_users']),
        'unique_articles': int(sol_1_dict['unique_articles']),
        'total_articles': int(sol_1_dict['total_articles']),
        'total_interactions': int(sol_1_dict['user_article_interactions']),
        'median_interactions_per_user': float(sol_1_dict['median_val']),
        'max_interactions_by_user': int(sol_1_dict['max_views_by_user']),
        'max_interactions_on_article': int(sol_1_dict['max_views']),
        'most_viewed_article_id': int(sol_1_dict['most_viewed_article_id']),
        'sparsity': float(sparsity)
    },
    'part_2_rank_based': {
        'top_10_articles': [
            {
                'rank': i+1,
                'article_id': int(aid),
                'title': name,
                'interactions': int(interactions[interactions['article_id'] == aid].shape[0])
            }
            for i, (aid, name) in enumerate(zip(top_10_ids, top_10_names))
        ]
    },
    'part_3_collaborative_filtering': {
        'test_user': int(test_user),
        'similar_users': {int(user): float(sim) for user, sim in similar.items()},
        'recommendations': [
            {'article_id': int(row['article_id']), 'title': row['title']}
            for idx, row in cf_recs.iterrows()
        ]
    },
    'part_4_content_based': {
        'test_user': int(test_user),
        'optimal_clusters': int(best_k),
        'best_silhouette_score': float(max(sil_scores)),
        'tfidf_features': int(tfidf_matrix.shape[1]),
        'recommendations': [
            {'article_id': int(row['article_id']), 'title': row['title']}
            for idx, row in content_recs.iterrows()
        ]
    },
    'part_5_svd': {
        'test_user': int(test_user),
        'svd_components': int(svd_result['n_components']),
        'variance_explained': float(svd_result['variance'][-1]),
        'recommendations': [
            {'article_id': int(row['article_id']), 'title': row['title']}
            for idx, row in svd_recs.iterrows()
        ]
    }
}

# Save JSON
output_file = 'notebook_output_results.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"✓ JSON results saved: {output_file}")

# Save text report
report_file = 'notebook_execution_report.txt'
with open(report_file, 'w') as f:
    f.write("="*90 + "\n")
    f.write("RECOMMENDATION SYSTEM: IBM COMMUNITY - EXECUTION REPORT\n")
    f.write("="*90 + "\n\n")
    f.write(f"Execution Timestamp: {datetime.now().isoformat()}\n\n")
    
    f.write("PART I: EXPLORATORY DATA ANALYSIS\n")
    f.write("-"*90 + "\n")
    for key, value in sol_1_dict.items():
        f.write(f"{key}: {value}\n")
    f.write(f"\nMatrix Sparsity: {sparsity:.4f}\n")
    
    f.write("\n\nPART II: RANK-BASED RECOMMENDATIONS (Top 10)\n")
    f.write("-"*90 + "\n")
    for i, (aid, title) in enumerate(zip(top_10_ids, top_10_names), 1):
        count = interactions[interactions['article_id'] == aid].shape[0]
        f.write(f"{i}. {title} (ID: {aid}, Interactions: {count})\n")
    
    f.write("\n\nPART III: COLLABORATIVE FILTERING\n")
    f.write("-"*90 + "\n")
    f.write(f"Test User: {test_user}\n")
    f.write(f"Similar Users (Top 5):\n")
    for user, sim in similar.items():
        f.write(f"  User {user}: {sim:.4f}\n")
    f.write(f"\nRecommendations:\n")
    f.write(cf_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n\nPART IV: CONTENT-BASED RECOMMENDATIONS\n")
    f.write("-"*90 + "\n")
    f.write(f"Optimal Clusters: {best_k}\n")
    f.write(f"Best Silhouette Score: {max(sil_scores):.4f}\n")
    f.write(f"TF-IDF Features: {tfidf_matrix.shape[1]}\n")
    f.write(f"\nRecommendations for User {test_user}:\n")
    f.write(content_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n\nPART V: MATRIX FACTORIZATION (SVD)\n")
    f.write("-"*90 + "\n")
    f.write(f"SVD Components: {svd_result['n_components']}\n")
    f.write(f"Variance Explained: {svd_result['variance'][-1]:.4f}\n")
    f.write(f"\nRecommendations for User {test_user}:\n")
    f.write(svd_recs[['article_id', 'title']].to_string())
    
    f.write("\n\n" + "="*90 + "\n")
    f.write("SUMMARY\n")
    f.write("="*90 + "\n")
    f.write(summary_text)

print(f"✓ Text report saved: {report_file}")

print("\n" + "="*90)
print("EXECUTION COMPLETED SUCCESSFULLY")
print("="*90)
print(f"\nOutput Files Generated:")
print(f"  1. {output_file} - Structured JSON results")
print(f"  2. {report_file} - Detailed text report")
print(f"\nData Files Generated:")
print(f"  1. data/articles.csv - 150 articles")
print(f"  2. data/user_item_interactions.csv - 2417 interactions")
print(f"  3. data/articles_community.csv - Article tags/metadata")
print(f"\nRecommendation Methods Implemented:")
print(f"  ✓ Part I: Exploratory Data Analysis")
print(f"  ✓ Part II: Rank-Based Recommendations")
print(f"  ✓ Part III: Collaborative Filtering (User-User)")
print(f"  ✓ Part IV: Content-Based Recommendations")
print(f"  ✓ Part V: Matrix Factorization (SVD)")
print("="*90)

# IBM Recommendation System Project

## Overview

Complete recommendation engine for IBM Watson Studio articles using multiple approaches:
- Exploratory Data Analysis
- Rank-Based Recommendations (baseline)
- User-User Collaborative Filtering
- Content-Based Recommendations with optimal clustering
- Matrix Factorization using SVD

## Project Rubric Compliance

### ✅ Part I & II: Data Exploration & Rank-Based Recommendations
**Required Statistics:**
- `unique_users`: Total unique users in dataset
- `unique_articles`: Total unique articles  
- `total_articles`: Articles in metadata
- `user_article_interactions`: Total interactions
- `median_val`: Median user interactions
- `max_views_by_user`: Maximum views by any user
- `max_views`: Maximum views for any article
- `most_viewed_article_id`: ID of most viewed article

**Functions:**
- `get_top_article_ids(interactions_df, n)` - Returns top N article IDs
- `get_top_article_names(interactions_df, articles_df, n)` - Returns top N titles
- `sol_1_test(sol_1_dict)` - Validates all statistics

### ✅ Part III: User-User Collaborative Filtering
**Components:**
- Binary user-item interaction matrix (1 if interacted, 0 otherwise)
- Cosine similarity for finding similar users
- Recommendation by aggregating similar users' interactions
- Improved ranking: weight by user similarity + user activity
- Cold-start handling for new users (fallback to popular items)

**Functions:**
- `create_user_item_matrix(interactions_df)`
- `find_similar_users(user_id, user_item_matrix, n_similar)`
- `recommend_user_user_collaborative(user_id, ...)`
- `recommend_user_user_improved(user_id, ...)`
- `recommend_for_new_user(interactions_df, articles_df)`

### ✅ Part IV: Content-Based Recommendations
**Features:**
- TF-IDF vectorization of article text
- Cosine similarity computation
- **KMeans clustering with silhouette score analysis**
- Optimal cluster selection visualization
- Content-based recommendations using article similarity

**Functions:**
- `prepare_article_content(articles_df, articles_community_df)`
- `create_tfidf_similarity_matrix(article_df)`
- `find_optimal_clusters(tfidf_matrix, max_clusters)`
- `recommend_content_based(user_id, ...)`

### ✅ Part V: Matrix Factorization
**Implementation:**
- Singular Value Decomposition (SVD) on user-item matrix
- U, Sigma, V^T matrices decomposition
- Explained variance analysis for different components
- Optimal latent feature selection with justification
- SVD-based article similarity and recommendations

**Explanation:** Why SVD works:
- Discovers latent features explaining interactions
- Reduces noise by keeping top components
- Allows predictions for unseen user-item pairs
- More scalable than explicit models

## Installation & Setup

### Requirements
```bash
python -m pip install -r requirements.txt
```

### Data Files (place in `data/` directory)
- `user_item_interactions.csv` - User interactions with articles
- `articles.csv` - Article metadata (id, title, etc.)
- `articles_community.csv` - Article content/text

### Run Analysis
```bash
# Jupyter Notebook
jupyter notebook recommendationsystem_ibmcommunity_analysis.ipynb

# VS Code with Jupyter support
code recommendationsystem_ibmcommunity_analysis.ipynb
```

## Testing Metrics for Production

### Engagement Metrics
- **CTR** (Click-Through Rate): % recommendations clicked
- **Conversion Rate**: % leading to desired action
- **Time Spent**: User engagement duration

### Quality Metrics
- **Precision@K**: Fraction of top-K that are relevant
- **Recall@K**: Fraction of relevant items in top-K
- **MAP**: Position-weighted relevance

### Coverage & Diversity
- **Coverage**: % of catalog recommendable
- **Diversity**: Variety of recommendations
- **Serendipity**: Unexpected + useful balance

### A/B Testing Strategy
1. **Design**: Control vs. treatment groups
2. **Duration**: 2-4 weeks (capture patterns)
3. **Stats**: T-tests, 95% confidence intervals
4. **Success**: >5% CTR, >3% conversion improvement

## Recommendation Approaches Summary

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Rank-Based** | Simple, cold-start friendly | Not personalized | New users |
| **Collaborative** | Personalized, discovers content | New users, sparse data | Active users |
| **Content-Based** | No new-article problem | Limited by content quality | New items |
| **Matrix Factorization** | Powerful, scalable | Black-box, complex tuning | Large systems |
| **Hybrid** | Leverages all strengths | Complex implementation | Production |

## Key Implementation Details

### TF-IDF Configuration
```
TfidfVectorizer(
    stop_words='english',
    max_df=0.8,        # Ignore terms in 80%+ documents
    min_df=2,          # Ignore terms in <2 documents  
    max_features=1000  # Top 1000 features
)
```

### Cosine Similarity
Used for:
- Finding similar users
- Article similarity (TF-IDF vectors)
- SVD-based article relationships

**Why:** Angle-based, magnitude-invariant, computationally efficient

### SVD Benefits
- Discovers hidden patterns
- Handles sparsity (no data but predicts)
- Scalable with approximate methods
- Balances complexity vs. quality

## Next Steps for Enhancement

### Hybrid Systems
- Combine methods intelligently
- Weight by confidence/coverage
- Ensemble approaches

### Advanced ML
- Deep learning embeddings
- Graph neural networks
- Temporal dynamics

### Cold-Start Solutions
- Onboarding questionnaires
- Content fallback
- Popularity weighting

### Feedback Loops
- Explicit ratings
- Implicit signals
- A/B testing results
- Continuous learning

## Project Structure

```
recommendationsystem_ibmcommunity_project/
├── recommendationsystem_ibmcommunity_analysis.ipynb
├── PROJECT_RUBRIC.md          (Detailed rubric specifications)
├── README.md                  (This file)
├── requirements.txt
└── data/
    ├── user_item_interactions.csv
    ├── articles.csv
    └── articles_community.csv
```

## Completion Status

✅ All rubric requirements implemented:
- Complete exploratory analysis with validation tests
- Rank-based baseline recommendations
- User-user collaborative filtering with improvements
- Content-based recommendations with optimal clustering
- Matrix factorization with variance analysis
- Documentation and metrics discussion
- A/B testing strategy defined
- Next steps for improvement outlined

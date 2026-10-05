# IBM Community Recommendation System
## Complete Execution Report

**Report date:** 2026-10-05

**Notebook:** `recommendationsystem_ibmcommunity_analysis.ipynb`

**Run profile:** Bundled sample data

**Current project revision:** `7882fbf`

## Executive Summary

The notebook's complete sample-data run succeeds. It loads the project CSVs, computes and validates exploration statistics, produces rank-based, collaborative, content-based, and SVD recommendations, generates both plots, runs edge/data validation, and exports review tables and metrics.

The bundled files are a small sample (172 interactions, 30 users, and 20 article IDs), not the canonical full IBM corpus described by the reviewer. Results below are sample results. Canonical totals and numeric similar-user benchmarks are recorded as reference expectations but were not verified against full data.

## Data and Exploration

The loader searches the notebook/project locations for `user_item_interactions.csv` and `articles_community.csv`. `articles.csv` is optional. If both article tables are present, it selects the table containing more unique article IDs to avoid preferring stale sample metadata over a larger community corpus. Interaction tables may identify users with either `email` or `user_id`.

| Measure | Sample result |
| --- | ---: |
| Interaction rows | 172 |
| Unique users | 30 |
| Unique articles in interactions | 20 |
| Articles in metadata | 20 |
| Median interactions per user | 6.0 |
| Maximum interactions per user | 6 |
| Maximum views per article | 9 |
| Most-viewed article | 4 |
| User-item matrix | 30 × 20 |
| Matrix sparsity | 71.33% |

`sol_1_test(sol_1_dict)` compares all eight statistics against the sample profile. The canonical profile supplied in reviewer feedback is supported when the corresponding 45,993-row full dataset is loaded.

## Recommendation Results

### Rank-Based

Articles are ranked by total interaction count. In the sample, the top ten are tied at 9 interactions; deterministic article-ID ordering resolves ties. See [top_articles.csv](../results/top_articles.csv).

### User-User Collaborative Filtering

The binary user-item matrix is used to rank neighbors by shared-interaction dot product. `find_similar_users` excludes the query user and returns the complete ordered ID list by default; an optional `n_similar` limit is supported. Both `user_item=` and `user_item_matrix=` call forms are accepted.

For sample user 1, the first five neighbors are `[8, 22, 29, 15, 6]`. New users receive popularity-ranked fallback recommendations. A synthetic email-key fixture verifies user lookup, similar-user ordering, and recommendations with the alternate `email` schema.

### Content-Based Recommendations

The content pipeline applies TF-IDF, reduces text with LSA/TruncatedSVD, fits K-Means, and selects the inertia elbow. For the 20-article sample, `k=12` is selected from candidates `2–19`. Content recommenders first restrict candidates to the same cluster, exclude already-read items where applicable, then rank candidates by interaction popularity.

See the [K-Means inertia chart](../results/charts/kmeans_inertia_elbow.png), [inertia values](../results/kmeans_inertia_points.csv), and [cluster assignments](../results/article_cluster_assignments.csv).

### SVD

The sample matrix supports at most 19 components. Deterministic holdout evaluation selected 5 components, with RMSE `0.3924` and cumulative explained variance `81.43%`. SVD item neighbors use reduced `Vᵀ` vectors mapped through `user_item_matrix.columns`; the sample neighbors for the first article are `[8, 15, 7, 14, 2]`.

See the [SVD selection chart](../results/charts/svd_feature_selection.png), [feature metrics](../results/svd_feature_metrics.csv), and [sample SVD neighbors](../results/recommendations_example_article_svd.csv).

## Validation

The notebook run completed these local checks successfully:

- Comprehensive rubric checks for exploration, ranked recommendations, matrix shape/values, collaborative recommendations, content clustering/ranking, and SVD mapping.
- Exact `analyze_latent_features(user_item_matrix, max_components=10)` call.
- `find_similar_users(..., user_item=user_item_matrix)` keyword form.
- Email-key user fixture and article metadata fallback/coverage checks.
- Edge-case assertions and dataset-integrity assertions.
- Notebook diagnostics reported no errors; every code cell has a successful execution record.

The separate `project_tests.py` file was not included in this checkout. The supplied numeric benchmark lists were skipped because their user IDs are not in the bundled sample.

## Canonical Full-Data Validation Still Needed

The reviewer’s full IBM reference is 45,993 interactions, 5,148 users, 714 interacted article IDs, and 1,051 metadata articles, with median 3.0, maximum 364 interactions per user, maximum 937 views for an article, and most-viewed article ID `1429.0`. Those canonical CSVs were not present during this run.

On that full corpus, 50 K-Means clusters and 200 SVD components are dimensionally feasible. The notebook evaluates those candidate ranges when full data is loaded, but their selected metrics and the numeric user-neighbor benchmark lists remain to be confirmed against the full files.

## Artifact Index

- [Run metrics JSON](../results/review_metrics.json)
- [Exploration statistics](../results/exploration_statistics.csv)
- [Top article ranking](../results/top_articles.csv)
- [Article cluster assignments](../results/article_cluster_assignments.csv)
- [Collaborative user recommendations](../results/recommendations_example_user_collaborative.csv)
- [Content user recommendations](../results/recommendations_example_user_content.csv)
- [Content article recommendations](../results/recommendations_example_article_content.csv)
- [SVD article recommendations](../results/recommendations_example_article_svd.csv)
- [Execution results](EXECUTION_RESULTS.md)
- [Rubric compliance report](RUBRIC_COMPLIANCE_REPORT.md)

The previous September 3 synthetic-data metrics have been replaced by this current sample-based report set.

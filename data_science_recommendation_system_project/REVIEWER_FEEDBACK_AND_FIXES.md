# Reviewer Feedback and Fixes

**Review date:** 2026-10-05  
**Project:** IBM Community Article Recommendation System

This note maps the reported rubric failures to the corresponding fixes and the results produced from the CSV files included with this project.

## Findings and Resolutions

| Reviewer finding | Resolution | Evidence |
| --- | --- | --- |
| Notebook stopped while loading `user_item_interactions.csv`. | The notebook locates the three required CSVs from the project root or its `data/` directory, independent of the kernel's starting directory. Missing files now raise a clear `FileNotFoundError`; the loader no longer silently creates substitute data. | All three input files loaded successfully; 172 interaction rows were read. |
| Exploration validation checked only that dictionary keys existed. | `sol_1_test` now compares the complete statistics dictionary to the expected values calculated for the included dataset. | Exact values are listed below; the exploration assertion passed. |
| `find_similar_users` returned a Pandas Series rather than a list of IDs. | The function now returns a cosine-similarity-ordered Python list of user IDs. Collaborative-filtering callers consume that list. | Type and recommendation assertions passed in `test_all_functions()`. |
| Content clustering/recommendation did not follow the required K-Means workflow. | Article text is vectorized with TF-IDF, reduced with TruncatedSVD/LSA, clustered with K-Means, and assessed with an inertia elbow plot. Content recommendations first restrict candidates to the seed/user-history cluster, then rank candidates by interaction popularity. | Selected `k=12`; both article and user content recommendation assertions passed. See the [inertia elbow chart](results/charts/kmeans_inertia_elbow.png) and [inertia data points](results/kmeans_inertia_points.csv). |
| Latent-feature count relied on explained variance alone. | A deterministic holdout evaluates RMSE and explained variance across feasible component counts. The selected count is the smallest model within 0.01 RMSE of the best observed score, with a written rationale in the notebook. | Selected 5 components, RMSE `0.3924`, explained variance `81.43%`. See the [feature-selection chart](results/charts/svd_feature_selection.png) and [feature metrics](results/svd_feature_metrics.csv). |
| SVD article recommendations could map vectors to the wrong article IDs. | Similarity vectors are aligned directly to `user_item_matrix.columns`, and article neighbors use the selected reduced-feature SVD model. | The three-neighbor alignment assertion passed; sample output is in [SVD article recommendations](results/recommendations_article_svd.csv). |
| `max_components` was not accepted by the SVD function. | `perform_svd` and its factorization wrapper accept `max_components`; the comprehensive test calls that keyword. | SVD signature and shape assertions passed. |

## Dataset Statistics

The included files contain 172 user-article interactions, 30 users, 20 unique article IDs, and 20 metadata articles. The expected exploration dictionary is:

| Statistic | Expected value |
| --- | ---: |
| `median_val` | 6.0 |
| `user_article_interactions` | 172 |
| `max_views_by_user` | 6 |
| `max_views` | 9 |
| `most_viewed_article_id` | 4 |
| `unique_articles` | 20 |
| `unique_users` | 30 |
| `total_articles` | 20 |

## Feasibility Notes

The supplied dataset has only 20 article texts and 20 article columns in the user-item matrix. Therefore, a 50-cluster target and 200 SVD components cannot be fit to this dataset. K-Means candidates are bounded to the feasible range `2` through `19`; SVD evaluation is bounded to at most `19` components. The selected values are determined from the available data rather than hard-coded to infeasible targets.

## Validation and Review Artifacts

The notebook was executed through all code cells. Its comprehensive rubric assertions, edge-case checks, and data-integrity checks passed. No separate `project_tests.py` was present in this project checkout, so the notebook's rubric-focused validation cells are the available project test suite.

The final measured values and validation statuses are recorded in [review metrics](results/review_metrics.json). Other review outputs include [exploration statistics](results/exploration_statistics.csv), [article cluster assignments](results/article_cluster_assignments.csv), [top articles](results/top_articles.csv), and example [collaborative recommendations](results/recommendations_user_1_collaborative.csv), [user content recommendations](results/recommendations_user_1_content.csv), and [article content recommendations](results/recommendations_article_content.csv).
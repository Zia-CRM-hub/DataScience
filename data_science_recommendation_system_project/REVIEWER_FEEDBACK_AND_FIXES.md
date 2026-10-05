# Reviewer Feedback and Fixes

**Review date:** 2026-10-05

**Project:** IBM Community Article Recommendation System

This note maps the reported rubric failures to the corresponding fixes and the results produced from the CSV files included with this project. It supersedes historical metrics in `output_files/RUBRIC_COMPLIANCE_REPORT.md`, which were generated from a different dataset snapshot.

## Findings and Resolutions

| Reviewer finding | Resolution | Evidence |
| --- | --- | --- |
| Notebook stopped while loading `user_item_interactions.csv`. | Data discovery works from the project root or `data/`. Interactions and `articles_community.csv` are required; `articles.csv` is optional. The loader selects whichever article table has more unique IDs, derives metadata when needed, and raises a clear error for missing required files instead of creating substitute data. | Required-file loading, optional metadata fallback, and stale-subset metadata regression checks pass. |
| Exploration validation checked only dictionary keys; reviewer supplied canonical IBM totals. | The exploration function accepts either a `user_id` or `email` interaction key and counts unique metadata article IDs. `sol_1_test` checks known values for the bundled sample and canonical IBM profile, with independent recomputation for other datasets. | Bundled-sample assertions pass. Canonical constants are recorded below, but cannot be validated without the full CSVs. |
| `find_similar_users` returned a Pandas Series and omitted the expected full ordered list. | The function now ranks by shared-interaction dot product, excludes the query user, and returns all ordered IDs by default; `n_similar` optionally truncates the list. It accepts both `user_item=` and `user_item_matrix=` and works with numeric IDs or email keys. | Full-list type/order, reviewer-keyword, and email-schema integration assertions pass. Exact numeric benchmarks run only when all listed IDs are present. |
| Content clustering/recommendation did not follow cluster-based popularity ranking. | Article text is vectorized with TF-IDF, reduced with TruncatedSVD/LSA, clustered with K-Means, and assessed with an inertia elbow. User and article content recommenders filter to matching clusters first and then rank by overall interaction popularity. | Bundled sample selects `k=12`. See the [inertia elbow chart](results/charts/kmeans_inertia_elbow.png) and [inertia data points](results/kmeans_inertia_points.csv). |
| Latent-feature count relied on explained variance alone; reviewer requested a rationale for 200 features. | A deterministic holdout evaluates RMSE and explained variance, and the notebook selects the smallest dimension within 0.01 RMSE of the best observed score. It evaluates up to 200 features when the full 714-item interaction matrix is loaded; it does not claim 200 is optimal without those measured results. | Bundled sample selects 5 components, RMSE `0.3924`, explained variance `81.43%`. See the [feature-selection chart](results/charts/svd_feature_selection.png) and [feature metrics](results/svd_feature_metrics.csv). |
| SVD article recommendations could map vectors to the wrong article IDs. | `get_svd_similar_article_ids(article_id, user_item_matrix, vt, n)` maps vectors using `user_item_matrix.columns` and computes cosine similarity on reduced item vectors. | Matrix-column ID and reduced-factor assertions pass; sample output is in [SVD article recommendations](results/recommendations_example_article_svd.csv). |
| `max_components` and `max_comp` argument names did not match. | `perform_svd`, its factorization wrapper, and `analyze_latent_features` use the `max_components` keyword. | The exact `analyze_latent_features(user_item_matrix, max_components=10)` call is executed and passes. |

## Dataset Statistics

The committed sample contains 172 user-article interactions, 30 users, 20 unique article IDs, and 20 metadata articles. Its expected exploration dictionary is:

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

The reviewer also provided expected values for the canonical full IBM dataset. The notebook recognizes that profile when the matching full data is loaded:

| Statistic | Canonical IBM value |
| --- | ---: |
| `median_val` | 3.0 |
| `user_article_interactions` | 45,993 |
| `max_views_by_user` | 364 |
| `max_views` | 937 |
| `most_viewed_article_id` | `1429.0` |
| `unique_articles` | 714 |
| `unique_users` | 5,148 |
| `total_articles` | 1,051 |

The full dataset is not included in this checkout, so these canonical values are implemented as the reference profile but have not been reproduced locally.

The supplied similar-user benchmark examples are `1 -> [3933, 46, 4201, 253, 824, 5034, 5041, 136, 2305, 395]`, `3933 -> [1, 46, 4201, 253, 824]`, and `46 -> [4201, 790, 5077]`. The notebook asserts these ordered lists only when all listed IDs exist in the loaded matrix; the bundled sample has users 1 through 30, so those benchmark assertions are explicitly skipped here.

## Feasibility Notes

For the bundled sample, 20 article texts and 20 interaction-matrix columns bound K-Means candidates to `2` through `19` and SVD evaluation to at most `19` components. For the canonical dataset described by the reviewer, 1,051 article texts make 50 clusters feasible, and 714 interaction-matrix columns make 200 SVD components feasible. The notebook bounds both workflows from the actual input dimensions and uses measured inertia/RMSE rather than claiming a target based on the smaller sample.

## Validation and Review Artifacts

The notebook's comprehensive rubric assertions, edge-case checks, data-integrity checks, `email`-schema fixture, optional metadata fallback, SVD mapping check, and `max_components` call passed on the bundled sample. The full-data benchmark IDs and canonical dataset constants could not be exercised because the 45,993-row IBM CSVs were not included. No separate `project_tests.py` was present in this project checkout, so the notebook's rubric-focused validation cells are the available local test suite.

The final measured values and validation statuses are recorded in [review metrics](results/review_metrics.json). Other review outputs include [exploration statistics](results/exploration_statistics.csv), [article cluster assignments](results/article_cluster_assignments.csv), [top articles](results/top_articles.csv), and example [collaborative recommendations](results/recommendations_example_user_collaborative.csv), [user content recommendations](results/recommendations_example_user_content.csv), [article content recommendations](results/recommendations_example_article_content.csv), and [SVD article recommendations](results/recommendations_example_article_svd.csv).
# Latest Rubric Compliance Report

**Assessment date:** 2026-10-05

**Project:** IBM Community Article Recommendation System

**Assessment basis:** Current notebook run using the bundled sample CSVs

> This report replaces the historical September 3 report in this folder. Its figures describe the current 172-interaction sample, not the full IBM dataset cited in the reviewer feedback.

## Criteria and Evidence

| Rubric criterion | Status on bundled sample | Evidence / remaining limitation |
| --- | --- | --- |
| Notebook code executes and produces visible results | **PASS** | All code cells have successful executions; both charts render; notebook diagnostics report no errors. |
| All tests pass | **PASS locally** | `test_all_functions()`, `test_edge_cases()`, and `test_data_validation()` pass. No separate `project_tests.py` is included in this checkout. |
| Data exploration values are correct | **PASS for sample** | 172 interactions, 30 users, 20 interacted articles, 20 metadata articles, median 6.0, max per user 6, max article views 9, most viewed article 4. Exact values are asserted by `sol_1_test()`. |
| Rank-based article recommendations | **PASS** | Top IDs and names are computed from interaction counts; exported in `results/top_articles.csv`. |
| User-item matrix and similar users | **PASS for sample** | Binary 30 × 20 matrix. Similar users are returned as an ordered Python list; `user_item=` and `user_item_matrix=` forms are tested. The `email` schema is covered by a fixture. |
| Reviewer numeric similar-user benchmarks | **NOT VERIFIED** | Expected IDs (including 3933, 4201, and 5077) are not in the bundled 30-user sample. Assertions run conditionally when all expected IDs exist; the full IBM interactions were not supplied. |
| TF-IDF/LSA/K-Means cluster selection | **PASS for sample** | Inertia elbow selected `k=12` from the feasible `2–19` range. See `results/charts/kmeans_inertia_elbow.png` and `results/kmeans_inertia_points.csv`. |
| Cluster-based content recommendations | **PASS** | Recommendations are restricted to the seed/user-history cluster and ranked by overall interaction popularity. User and article examples are exported under `results/recommendations_example_*.csv`. |
| SVD latent-feature selection | **PASS for sample** | Holdout RMSE and explained variance are measured over 1–19 feasible components. Five components were selected: RMSE 0.3924, explained variance 81.43%. See `results/svd_feature_metrics.csv`. |
| Reviewer target of 200 SVD features | **FEASIBLE, NOT VERIFIED** | The canonical interaction matrix has 714 article columns, so 200 is dimensionally feasible and is included in the candidate evaluation range. This bundled sample has only 20 columns and cannot evaluate 200; no full-data performance result is claimed. |
| SVD article-article recommendations | **PASS for sample** | `get_svd_similar_article_ids` uses item vectors from reduced `Vᵀ` and maps positions through `user_item_matrix.columns`. Alignment tests pass. |
| Written results and production evaluation discussion | **PASS** | Notebook describes method trade-offs, metrics, and A/B testing considerations. |

## Bundled Sample Statistics

| Statistic | Value |
| --- | ---: |
| `median_val` | 6.0 |
| `user_article_interactions` | 172 |
| `max_views_by_user` | 6 |
| `max_views` | 9 |
| `most_viewed_article_id` | 4 |
| `unique_articles` | 20 |
| `unique_users` | 30 |
| `total_articles` | 20 |

## Canonical Reviewer Reference

The reviewer supplied these expected values for the full IBM corpus. The notebook recognizes this profile and validates against it when matching full data is loaded; these values were not reproduced locally:

| Statistic | Expected full-dataset value |
| --- | ---: |
| `median_val` | 3.0 |
| `user_article_interactions` | 45,993 |
| `max_views_by_user` | 364 |
| `max_views` | 937 |
| `most_viewed_article_id` | `1429.0` |
| `unique_articles` | 714 |
| `unique_users` | 5,148 |
| `total_articles` | 1,051 |

The full corpus permits evaluating up to 50 text clusters (1,051 articles) and 200 SVD components (714 interaction-matrix columns). The actual selected values must be supported by metrics computed from those full files.

## Review Artifacts

- [Execution results](EXECUTION_RESULTS.md)
- [Machine-readable metrics](../results/review_metrics.json)
- [K-Means elbow plot](../results/charts/kmeans_inertia_elbow.png)
- [SVD feature plot](../results/charts/svd_feature_selection.png)
- [Inertia datapoints](../results/kmeans_inertia_points.csv)
- [SVD feature datapoints](../results/svd_feature_metrics.csv)

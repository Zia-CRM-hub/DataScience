# Execution Results

**Execution date:** 2026-10-05

**Notebook:** `recommendationsystem_ibmcommunity_analysis.ipynb`

**Dataset profile:** Bundled sample (`user_id` schema)

**Notebook kernel:** Python 3.14.4

## Execution Outcome

The current notebook summary shows every code cell executed successfully. Both the K-Means inertia plot and SVD RMSE/variance plot rendered. The final export cell reruns the local tests before writing result files. **All 3 of 3 notebook-defined validation suites pass** against the included sample data.

| Check | Outcome | Detail |
| --- | --- | --- |
| `sol_1_test(sol_1_dict)` | PASS | All eight sample statistics equal their expected values. |
| `test_all_functions()` | PASS | Rank-based, collaborative, content, SVD, API compatibility, email-key fixture, and metadata-selection checks. |
| `test_edge_cases()` | PASS | Missing users, sparse users, oversized requests, and recommendation fallbacks. |
| `test_data_validation()` | PASS | Required fields, valid IDs, duplicates, and metadata references. |
| Notebook diagnostics | PASS | No errors reported. |
| Canonical reviewer benchmark IDs | NOT VERIFIED | Full IBM dataset is not present; numeric IDs are absent from this 30-user sample. |
| External `project_tests.py` | NOT RUN | No such file was present in this checkout. |

## Sample Inputs and Exploration

The committed sample contains three CSVs: `data/user_item_interactions.csv`, `data/articles.csv`, and `data/articles_community.csv`. The loader requires interactions and community content, supports an optional article metadata file, and selects the article table with greater unique-ID coverage.

| Measure | Executed result |
| --- | ---: |
| Interaction rows | 172 |
| User key | `user_id` |
| Unique users | 30 |
| Unique articles with interactions | 20 |
| Article metadata count | 20 |
| Median interactions per user | 6.0 |
| Maximum interactions by one user | 6 |
| Maximum views for one article | 9 |
| Most-viewed article ID | 4 |
| User-item matrix shape | 30 × 20 |
| Matrix sparsity | 71.33% |

The eight values are also available in [exploration_statistics.csv](../results/exploration_statistics.csv) and the full run summary in [review_metrics.json](../results/review_metrics.json).

## Executed Recommendation Outputs

The ten most popular articles are IDs `4, 5, 11, 12, 18, 19, 1, 2, 8, 9`; each received 9 interactions. See [top_articles.csv](../results/top_articles.csv).

For sample user 1, the ordered dot-product neighbors begin `[8, 22, 29, 15, 6]`. The exported collaborative recommendations are in [recommendations_example_user_collaborative.csv](../results/recommendations_example_user_collaborative.csv). Content recommendations for the same example are in [recommendations_example_user_content.csv](../results/recommendations_example_user_content.csv).

For seed article 1, cluster/popularity recommendations are IDs `2, 4, 5, 8, 9, 3, 6, 7`. Reduced-feature SVD recommendations are IDs `8, 15, 7, 14, 2`. Both result lists are exported: [content-based article recommendations](../results/recommendations_example_article_content.csv) and [SVD article recommendations](../results/recommendations_example_article_svd.csv).

## Model Metrics and Charts

### Content Model

Article text produces a TF-IDF matrix of shape `(20, 11)` and an LSA matrix of shape `(20, 10)`. K-Means evaluated `k=2–19`; the inertia elbow selected `k=12`, with inertia effectively zero. The chart, data points, and assignments are available as [kmeans_inertia_elbow.png](../results/charts/kmeans_inertia_elbow.png), [kmeans_inertia_points.csv](../results/kmeans_inertia_points.csv), and [article_cluster_assignments.csv](../results/article_cluster_assignments.csv).

### SVD Model

The interaction matrix permits at most 19 components. Holdout evaluation selected 5 features:

| Metric | Result |
| --- | ---: |
| Holdout RMSE | 0.3924 |
| Cumulative explained variance | 81.43% |
| Selected component count | 5 of 19 feasible |

See the [SVD feature chart](../results/charts/svd_feature_selection.png) and [svd_feature_metrics.csv](../results/svd_feature_metrics.csv).

## Reviewer Reference Values Not Reproduced Here

The reviewer’s canonical corpus is expected to contain 45,993 interactions, 5,148 users, 714 interacted article IDs, and 1,051 metadata articles. Its expected statistics include median 3.0, max 364 interactions per user, max 937 views per article, and most-viewed ID `1429.0`. Those files were not available for this run.

That full profile makes 50 text clusters and 200 SVD components dimensionally feasible. The notebook supports those candidate ranges when the full inputs are supplied, but their measured selection and the reviewer’s numeric similar-user lists remain NOT VERIFIED.

For the complete mapping from each verified value to its supporting input, output, plot, notebook, and validation cell, see the [verified evidence index](VERIFIED_EVIDENCE_INDEX.md).

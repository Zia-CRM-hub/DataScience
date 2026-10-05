# IBM Community Recommendation System
## Complete Execution Report

**Execution/report date:** 2026-10-05

**Notebook:** `recommendationsystem_ibmcommunity_analysis.ipynb`

**Run profile:** Bundled sample data

**Notebook runtime:** Python 3.14.4

## Executive Summary

The latest notebook execution completes successfully on the bundled sample. All code cells have successful execution records. Exploration, ranking, collaborative filtering, content recommendations, SVD, edge-case validation, data validation, and result export checks pass. Both requested charts render and are saved under `results/charts/`.

This run uses a small sample, not the full IBM dataset named in reviewer expectations. Accordingly, the report separates sample PASS results from canonical full-data checks that could not be reproduced locally. Historical September 3 figures in prior reports have been replaced with current sample measurements.

## Input Data and Execution

The bundled project data consists of:

| File | Role | Sample rows/items |
| --- | --- | ---: |
| `data/user_item_interactions.csv` | user/article interactions | 172 rows |
| `data/articles.csv` | article titles and metadata | 20 unique articles |
| `data/articles_community.csv` | content text for articles | 20 unique articles |

The loader searches the project root and `data/`, accepts `user_id` or `email`, and requires the interaction and community-content CSVs. `articles.csv` is optional; if present alongside community metadata, the table with more unique article IDs is selected so a stale subset cannot mask a larger corpus.

## Exploration Results

| Metric | Result |
| --- | ---: |
| Unique users | 30 |
| Interactions | 172 |
| Unique interacted articles | 20 |
| Metadata articles | 20 |
| Median interactions per user | 6.0 |
| Maximum interactions per user | 6 |
| Maximum views for one article | 9 |
| Most-viewed article ID | 4 |
| User-item matrix shape | 30 × 20 |
| Matrix sparsity | 71.33% |

All eight exploration fields are checked by `sol_1_test(sol_1_dict)` against the sample profile.

## Recommendation Execution Details

### Rank-Based Recommendations

The top ten article IDs are `4, 5, 11, 12, 18, 19, 1, 2, 8, 9`. Each has 9 interactions. Ties are deterministically ordered by article ID. The full table is [top_articles.csv](../results/top_articles.csv).

### Collaborative Filtering

A binary `(30, 20)` user-item matrix was created. Similar users are returned as an ordered Python list based on shared-interaction dot product; the query user is excluded. Sample user 1's first five neighbors are `[8, 22, 29, 15, 6]`. The implementation supports either `user_id` or `email` keys and has passing tests for both matrix argument names.

For sample user 1, collaborative recommendations are exported to [recommendations_example_user_collaborative.csv](../results/recommendations_example_user_collaborative.csv). Cold-start behavior falls back to rank-based results.

### Content-Based Recommendations

Article text is transformed using TF-IDF and LSA/TruncatedSVD before K-Means. The sample has 20 article texts, candidates `k=2–19`, and inertia-elbow selection `k=12`. Recommendations first filter to matching cluster membership, then rank candidates by overall interaction popularity.

For seed article 1, sample article-content recommendation IDs are `[2, 4, 5, 8, 9, 3, 6, 7]`. See the [inertia chart](../results/charts/kmeans_inertia_elbow.png), [inertia data](../results/kmeans_inertia_points.csv), [cluster assignments](../results/article_cluster_assignments.csv), and [article recommendations](../results/recommendations_example_article_content.csv).

### SVD and Article Neighbors

The sample's 20 item columns permit at most 19 components. Holdout evaluation selects 5 features with RMSE `0.3924` and cumulative explained variance `81.43%`. SVD item neighbors are computed from reduced `Vᵀ` vectors and mapped through `user_item_matrix.columns`.

Sample neighbor IDs for the first article are `[8, 15, 7, 14, 2]`. The [feature selection chart](../results/charts/svd_feature_selection.png), [feature datapoints](../results/svd_feature_metrics.csv), and [neighbor output](../results/recommendations_example_article_svd.csv) are available for inspection.

## Test and Validation Results

| Validation | Result |
| --- | --- |
| `sol_1_test(sol_1_dict)` | PASS |
| `test_all_functions()` | PASS |
| `test_edge_cases()` | PASS |
| `test_data_validation()` | PASS |
| Email user-key fixture | PASS |
| Optional/stale article metadata fixture | PASS |
| Reviewer `max_components` and `user_item=` call forms | PASS |
| Notebook diagnostics | No errors |
| External `project_tests.py` | Not present in this checkout |
| Canonical numeric similar-user ID lists | Not verified; required IDs are absent from sample |

## Full IBM Dataset: Pending Reproduction

The reviewer supplied canonical targets of 45,993 interactions, 5,148 users, 714 interacted article IDs, and 1,051 metadata articles, including median 3.0, maximum 364 interactions per user, maximum 937 views per article, and most-viewed article `1429.0`. The full CSVs were not available for this execution.

With those full dimensions, 50 K-Means clusters and 200 SVD components are feasible. The code evaluates the relevant ranges, but the selected full-data elbow, 200-component holdout metrics, and user-ID benchmark lists remain unverified until the canonical files and official project tests are run.

## Report and Result Index

- [Execution data and outputs](EXECUTION_RESULTS.md)
- [Rubric status and evidence](RUBRIC_COMPLIANCE_REPORT.md)
- [Reviewer findings, fixes, and PASS/FAIL comments](../REVIEWER_FEEDBACK_AND_FIXES.md)
- [Machine-readable run metrics](../results/review_metrics.json)
- [Exploration statistics](../results/exploration_statistics.csv)
- [Example user-content recommendations](../results/recommendations_example_user_content.csv)

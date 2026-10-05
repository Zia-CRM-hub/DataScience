# Verified Evidence Index

**Evidence snapshot:** 2026-10-05

**Dataset profile:** Bundled sample (`user_id` schema)
**Notebook:** `recommendationsystem_ibmcommunity_analysis.ipynb`

This index maps each locally verified claim to its data point and supporting artifact. It distinguishes checks run on the committed sample from reviewer expectations that require the full IBM dataset.

## Verified Sample Data Points

| Measure | Verified value | Primary evidence |
| --- | ---: | --- |
| Input interaction rows | 172 | [user_item_interactions.csv](../data/user_item_interactions.csv), [review metrics](../results/review_metrics.json) |
| User key | `user_id` | [interaction CSV](../data/user_item_interactions.csv) |
| Unique users | 30 | [exploration statistics](../results/exploration_statistics.csv) |
| Unique interacted articles | 20 | [exploration statistics](../results/exploration_statistics.csv) |
| Article metadata/content IDs | 20 | [articles.csv](../data/articles.csv), [articles_community.csv](../data/articles_community.csv) |
| Median interactions per user | 6.0 | [exploration statistics](../results/exploration_statistics.csv) |
| Maximum interactions per user | 6 | [exploration statistics](../results/exploration_statistics.csv) |
| Maximum article views | 9 | [exploration statistics](../results/exploration_statistics.csv) |
| Most-viewed article ID | 4 | [exploration statistics](../results/exploration_statistics.csv) |
| User-item matrix dimensions | 30 × 20 | [review metrics](../results/review_metrics.json) and notebook execution output |
| User-item matrix sparsity | 71.33% | [review metrics](../results/review_metrics.json) |
| TF-IDF dimensions | 20 × 11 | Notebook execution output |
| LSA dimensions | 20 × 10 | Notebook execution output |
| K-Means candidate range / selected count | 2–19 / `k=12` | [inertia datapoints](../results/kmeans_inertia_points.csv), [inertia chart](../results/charts/kmeans_inertia_elbow.png) |
| Selected SVD features | 5 of 19 feasible | [SVD feature datapoints](../results/svd_feature_metrics.csv) |
| Selected SVD holdout RMSE | 0.3924446284 | [SVD feature datapoints](../results/svd_feature_metrics.csv), [review metrics](../results/review_metrics.json) |
| Selected SVD explained variance | 81.4265% | [SVD feature datapoints](../results/svd_feature_metrics.csv), [SVD chart](../results/charts/svd_feature_selection.png) |
| Reduced-SVD article neighbors for sample seed | `[8, 15, 7, 14, 2]` | [SVD recommendation output](../results/recommendations_example_article_svd.csv) |
| Similar users for sample user 1 | `[8, 22, 29, 15, 6]` | Notebook execution output; return type and full-list behavior asserted by `test_all_functions()` |

The exploration dictionary values are also recorded in `REVIEWER_FEEDBACK_AND_FIXES.md` and [EXECUTION_RESULTS.md](EXECUTION_RESULTS.md).

## Local Validation Evidence

| Check | Result | What it covers |
| --- | --- | --- |
| `sol_1_test(sol_1_dict)` | PASS | Exact 8-value bundled-sample exploration dictionary. |
| `test_all_functions()` | PASS | Rank-based recommendations, binary matrix, similar-user lists, collaborative recommendations, content cluster/popularity behavior, SVD shapes and ID mapping, email-key fixture, and metadata-source selection. |
| Reviewer API checks | PASS | `analyze_latent_features(..., max_components=10)` and `find_similar_users(..., user_item=...)`. |
| `test_edge_cases()` | PASS | Missing user, sparse user, large recommendation requests, and fallback behavior. |
| `test_data_validation()` | PASS | Input schema, non-empty keys, valid article IDs, duplicate interactions, and metadata references. |
| Notebook diagnostics | PASS | No errors reported; the latest notebook summary shows successful execution records for every code cell. |
| External `project_tests.py` | NOT AVAILABLE | No such file is present in the repository checkout. |

All locally executed validation checks passed. This is **not** a claim of 100% recommendation accuracy, and it does not establish canonical full-dataset benchmark results.

## Canonical Reviewer Data: Not Verified Locally

The reviewer provided these canonical IBM targets. They are recorded as reference values, not as measured results from the bundled sample:

| Statistic | Reviewer-provided canonical target | Verification status |
| --- | ---: | --- |
| Median interactions per user | 3.0 | NOT VERIFIED: full CSV absent |
| Total interactions | 45,993 | NOT VERIFIED: full CSV absent |
| Maximum interactions per user | 364 | NOT VERIFIED: full CSV absent |
| Maximum article views | 937 | NOT VERIFIED: full CSV absent |
| Most-viewed article ID | `1429.0` | NOT VERIFIED: full CSV absent |
| Unique interacted articles | 714 | NOT VERIFIED: full CSV absent |
| Unique users | 5,148 | NOT VERIFIED: full CSV absent |
| Metadata articles | 1,051 | NOT VERIFIED: full CSV absent |
| Similar-user benchmark IDs | User 1, 3933, 46, 4201, 790, 5077, etc. | NOT VERIFIED: benchmark IDs absent from sample |
| 50-cluster elbow result | Candidate is dimensionally feasible with 1,051 texts | NOT VERIFIED: full text corpus absent |
| 200-feature SVD performance | Candidate is dimensionally feasible with 714 item columns | NOT VERIFIED: full interaction matrix absent |

## Supporting Files

### Input Data

- [User-item interactions](../data/user_item_interactions.csv)
- [Article metadata](../data/articles.csv)
- [Article community text](../data/articles_community.csv)

### Implementation and Criteria

- [Recommendation notebook](../recommendationsystem_ibmcommunity_analysis.ipynb)
- [Project rubric](../PROJECT_RUBRIC.md)
- [Requirements](../requirements.txt)
- [Reviewer findings, fixes, and statuses](../REVIEWER_FEEDBACK_AND_FIXES.md)

### Current Result Artifacts

- [Machine-readable metrics](../results/review_metrics.json)
- [Exploration statistics](../results/exploration_statistics.csv)
- [Top articles](../results/top_articles.csv)
- [Article cluster assignments](../results/article_cluster_assignments.csv)
- [K-Means inertia datapoints](../results/kmeans_inertia_points.csv)
- [SVD feature datapoints](../results/svd_feature_metrics.csv)
- [K-Means inertia chart](../results/charts/kmeans_inertia_elbow.png)
- [SVD RMSE/variance chart](../results/charts/svd_feature_selection.png)
- [Example user collaborative recommendations](../results/recommendations_example_user_collaborative.csv)
- [Example user content recommendations](../results/recommendations_example_user_content.csv)
- [Example article content recommendations](../results/recommendations_example_article_content.csv)
- [Example article SVD recommendations](../results/recommendations_example_article_svd.csv)

Additional `recommendations_user_1_*.csv` and non-example `recommendations_article_*.csv` compatibility exports are retained in `results/`; use the `recommendations_example_*.csv` files above as the current named review exports.

### Reports

- [Execution results](EXECUTION_RESULTS.md)
- [Rubric compliance report](RUBRIC_COMPLIANCE_REPORT.md)
- [Complete execution report](COMPLETE_EXECUTION_REPORT.md)

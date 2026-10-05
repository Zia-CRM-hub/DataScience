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

**Verified test-suite result: 3 of 3 notebook-defined validation suites passed (100% of the local suites executed).** This percentage is a test-suite pass rate only. It is not a claim of 100% recommendation accuracy, and it does not include the unavailable external `project_tests.py` or the canonical full-data benchmark cases.

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

This manifest lists the relevant checked-in project files and identifies which are authoritative evidence for the latest run.

### Primary Inputs and Criteria

- [User-item interactions](../data/user_item_interactions.csv) - authoritative input; 172 rows, 30 unique users, 20 interacted articles.
- [Article metadata](../data/articles.csv) - authoritative sample metadata; 20 unique article IDs.
- [Article community text](../data/articles_community.csv) - authoritative sample content; 20 unique article IDs.
- [Project rubric](../PROJECT_RUBRIC.md) - criteria used for the notebook assessment.
- [Requirements](../requirements.txt) - declared Python dependencies.
- [README](../README.md) - project setup, implementation notes, and report links.

### Implementation and Reviewer Record

- [Recommendation notebook](../recommendationsystem_ibmcommunity_analysis.ipynb)
- [Reviewer findings, fixes, and statuses](../REVIEWER_FEEDBACK_AND_FIXES.md)

### Current Result Artifacts (Latest Notebook Export)

- [Machine-readable metrics](../results/review_metrics.json) - canonical summary for the latest export; includes `dataset_profile` and benchmark-verification status.
- [Exploration statistics](../results/exploration_statistics.csv) - all eight measured rubric values.
- [Top articles](../results/top_articles.csv) - ordered article IDs, titles, and counts.
- [Article cluster assignments](../results/article_cluster_assignments.csv) - cluster and popularity per article.
- [K-Means inertia datapoints](../results/kmeans_inertia_points.csv) - exact plotted inertia values and selected `k` flag.
- [SVD feature datapoints](../results/svd_feature_metrics.csv) - RMSE, variance, and selected-dimension flag for each tested count.
- [K-Means inertia chart](../results/charts/kmeans_inertia_elbow.png).
- [SVD RMSE/variance chart](../results/charts/svd_feature_selection.png).
- [Example user collaborative recommendations](../results/recommendations_example_user_collaborative.csv).
- [Example user content recommendations](../results/recommendations_example_user_content.csv).
- [Example article content recommendations](../results/recommendations_example_article_content.csv).
- [Example article SVD recommendations](../results/recommendations_example_article_svd.csv).

Compatibility exports also tracked in `results/` are `recommendations_user_1_collaborative.csv`, `recommendations_user_1_content.csv`, `recommendations_article_content.csv`, and `recommendations_article_svd.csv`. They are retained for compatibility; use the `recommendations_example_*.csv` files above as the primary named review outputs.

### Execution and Historical Reference Files

- [Notebook runner](../run_notebook.py) and [shell entry point](../execute.sh) are legacy automation helpers, not the source of the verified metrics in this index.
- [Synthetic data generator](../generate_synthetic_data.py) and [synthetic execution script](../EXECUTION_OUTPUT.py) generate an alternate synthetic dataset. `execute.sh` invokes the generator before running, which overwrites `data/*.csv`; do not use it when reproducing the committed 172-row sample or a supplied canonical IBM dataset.
- [Historical text execution output](../EXECUTION_RESULTS.txt) is from an older synthetic-data run and is not current sample evidence.
- The `output_files/` folder contains [current execution details](EXECUTION_RESULTS.md), [rubric status](RUBRIC_COMPLIANCE_REPORT.md), [the complete execution report](COMPLETE_EXECUTION_REPORT.md), and this index.

### Reports

- [Execution results](EXECUTION_RESULTS.md)
- [Rubric compliance report](RUBRIC_COMPLIANCE_REPORT.md)
- [Complete execution report](COMPLETE_EXECUTION_REPORT.md)

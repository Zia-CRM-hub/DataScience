# Rubric Compliance Report

**Assessment date:** 2026-10-05

**Assessment data:** Bundled 172-interaction sample
**Overall:** PASS for notebook execution and sample-data criteria; canonical full-corpus criteria remain NOT VERIFIED.

## Code Functionality and Readability

| Criterion | Initial reviewer status | Current status | Evidence and data points |
| --- | --- | --- | --- |
| Notebook runs and outputs are visible | FAIL | **PASS - sample** | Notebook summary shows successful execution for every code cell; both required plots render. |
| Data loading is robust | FAIL | **PASS - sample and fixture** | Finds input files from project root or `data/`; requires interaction/community CSVs; optional/stale metadata handling is tested. |
| Function signatures match callers | FAIL | **PASS - tested calls** | `analyze_latent_features(..., max_components=10)`, SVD `max_components`, and similar-user `user_item=` forms pass. |
| Project tests | FAIL | **PASS locally; external suite unavailable** | Notebook `test_all_functions`, `test_edge_cases`, and `test_data_validation` pass. No `project_tests.py` was found in this checkout. |

## Part I & II: Data Exploration & Create Rank Based Recommendations

**Initial reviewer status:** FAIL. Validation checked keys rather than the values.

**Current status:** **PASS for bundled sample; canonical IBM profile NOT VERIFIED.** `sol_1_test(sol_1_dict)` checks all eight values.

| Variable | Sample value |
| --- | ---: |
| `median_val` | 6.0 |
| `user_article_interactions` | 172 |
| `max_views_by_user` | 6 |
| `max_views` | 9 |
| `most_viewed_article_id` | 4 |
| `unique_articles` | 20 |
| `unique_users` | 30 |
| `total_articles` | 20 |

Top ten articles each have 9 interactions. See [rank output](../results/top_articles.csv).

## Part III: Collaborative Filtering

**Initial reviewer status:** FAIL. Similar users were returned as a Pandas object and the benchmark outputs were missing.

**Current status:** **PASS for sample and alternate schema; numeric full-data benchmarks NOT VERIFIED.** The function returns a Python list ordered by shared-interaction dot product, excludes the query user, supports optional truncation, and accepts either user-key schema.

The sample matrix is binary with shape `30 × 20` and sparsity `71.33%`. Sample user 1 neighbors begin `[8, 22, 29, 15, 6]`. A synthetic `email`-key fixture verifies ordering and recommendation behavior.

The reviewer’s expected numeric benchmark IDs include 3933, 4201, and 5077, which are not in the bundled sample. These exact lists are asserted only when all benchmark IDs exist in the loaded matrix.

## Part IV: Create Rank Based Recommendations

**Initial reviewer status:** FAIL. Content recommendations did not apply cluster membership first and popularity ranking second.

**Current status:** **PASS for bundled sample; full-data elbow NOT VERIFIED.** Content text is transformed with TF-IDF and LSA before K-Means. The inertia elbow selects `k=12` from sample candidates `2–19`; recommendations are restricted to the seed/history cluster and ranked by global interaction popularity.

For this sample, the article corpus has 20 items, so `k≈50` cannot be fit. The reviewer’s canonical article-content corpus has 1,051 articles, where 50 candidate clusters are feasible. See the [inertia chart](../results/charts/kmeans_inertia_elbow.png) and [inertia datapoints](../results/kmeans_inertia_points.csv).

## Part V: Matrix Factorization

**Initial reviewer status:** FAIL. Latent-feature choice lacked a performance-based rationale, and item IDs could be misaligned with SVD vectors.

**Current status:** **PASS for bundled sample; canonical 200-feature result NOT VERIFIED.** Holdout RMSE and explained variance are plotted for feasible dimensions. The sample selects 5 of 19 feasible features with RMSE `0.3924` and explained variance `81.43%`. `get_svd_similar_article_ids` maps reduced item vectors through `user_item_matrix.columns`.

The canonical matrix has 714 article columns, so 200 features are feasible and evaluated when full inputs are loaded. No full-data performance result is claimed without those inputs. See the [feature chart](../results/charts/svd_feature_selection.png) and [SVD datapoints](../results/svd_feature_metrics.csv).

## Canonical Values from Reviewer

These are the reviewer-provided targets for the full IBM data. They are reference values, not results from the local sample run.

| Statistic | Canonical target |
| --- | ---: |
| Median interactions per user | 3.0 |
| Total interactions | 45,993 |
| Maximum interactions by user | 364 |
| Maximum views by article | 937 |
| Most-viewed article ID | `1429.0` |
| Unique interacted articles | 714 |
| Unique users | 5,148 |
| Metadata articles | 1,051 |

## Validation Artifacts

- [Latest execution results](EXECUTION_RESULTS.md)
- [Reviewer findings, fixes, and PASS/FAIL comments](../REVIEWER_FEEDBACK_AND_FIXES.md)
- [Machine-readable metrics](../results/review_metrics.json)
- [Notebook](../recommendationsystem_ibmcommunity_analysis.ipynb)

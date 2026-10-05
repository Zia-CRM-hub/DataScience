# Summary of Rubric Evaluation

**Review date:** 2026-10-05
**Project:** IBM Community Article Recommendation System

| Rubric section | Criterion | Reviewer status received | Current outcome |
| --- | --- | --- | --- |
| Code Functionality and Readability | Notebook executes; function signatures match tests | FAIL | PASS on bundled sample. All code cells have successful executions; the `max_components` API calls pass. Separate `project_tests.py` was not included. |
| Part I & II: Data Exploration & Create Rank Based Recommendations | Correct dataset statistics and ranked article functions | FAIL | PASS for the included 172-row sample. Canonical full IBM totals are supported but NOT VERIFIED because those CSVs are unavailable. |
| Part III: Collaborative Filtering | Ordered similar-user IDs and recommendations | FAIL | PASS for sample and email-schema fixture. Reviewer numeric benchmark IDs are NOT VERIFIED because they are not in the sample. |
| Part IV: Create Rank Based Recommendations (also labeled Part IV: Content-Based Recommendations) | K-Means content clusters and popularity-ranked recommendations | FAIL | PASS on sample with `k=12`; canonical `k≈50` is dimensionally feasible on the full 1,051-article corpus but NOT VERIFIED locally. |
| Part V: Matrix Factorization | Performance-based feature selection and SVD article neighbors | FAIL | PASS on sample with 5 features and aligned item IDs. Canonical 200-feature performance is NOT VERIFIED locally. |

The initial FAIL labels above are transcribed from the reviewer feedback. Current outcomes are separated by data profile: local sample checks passed; full-dataset-only figures and benchmarks are not claimed as tested.

## Code Functionality and Readability

**What went well (reviewer feedback):** The notebook is organized by project part, uses helper functions and docstrings, and includes custom validation cells.

**Reviewer finding and initial status:** FAIL. `load_data()` raised `FileNotFoundError` when the kernel started from a different working directory, which prevented downstream cells from running. A test also called `analyze_latent_features(..., max_components=10)` while the submitted function used a different parameter name.

**Fix:** The loader searches the project root and `data/` folder. Interactions and community content are required; `articles.csv` is optional. When both article tables exist, the loader chooses the one with more unique article IDs, avoiding stale sample metadata. User keys may be `email` or `user_id`. The analysis and SVD functions accept `max_components`; `find_similar_users` accepts both `user_item=` and `user_item_matrix=`.

**Data and outcome:** The bundled tables load as 172 interactions, 20 community articles, and 20 metadata articles. The optional/stale metadata fallback, exact `analyze_latent_features(user_item_matrix, max_components=10)` call, and reviewer keyword form are covered by passing notebook assertions. All notebook code cells have successful execution records; notebook diagnostics report no errors.

## Part I & II: Data Exploration & Create Rank Based Recommendations

**Reviewer finding and initial status:** FAIL. The original validation checked dictionary keys rather than verifying the values computed from the dataset.

**Fix:** `sol_1_test(sol_1_dict)` now checks all eight values for a recognized data profile and independently recomputes values for other profiles. `total_articles` counts unique metadata article IDs.

**Bundled sample results: PASS.**

| Statistic | Measured value |
| --- | ---: |
| `median_val` | 6.0 |
| `user_article_interactions` | 172 |
| `max_views_by_user` | 6 |
| `max_views` | 9 |
| `most_viewed_article_id` | 4 |
| `unique_articles` | 20 |
| `unique_users` | 30 |
| `total_articles` | 20 |

The top ten sample articles each have 9 interactions. Their ordered IDs and titles are in [top_articles.csv](results/top_articles.csv). Both rank-based function checks pass.

**Canonical IBM reference values: NOT VERIFIED locally.** The reviewer supplied median `3.0`, `45,993` interactions, max `364` interactions per user, max `937` views per article, most-viewed article ID `1429.0`, `714` unique interacted articles, `5,148` users, and `1,051` metadata articles. The canonical CSVs were not included in this workspace; these values are supported as the canonical profile but were not reproduced in this run.

## Part III: Collaborative Filtering

**Reviewer finding and initial status:** FAIL. Similar-user output was a Pandas Series rather than a plain list, and the reviewer supplied ordered benchmark lists.

**Fix:** Similar users are ranked by shared-interaction dot product, the queried user is removed, and a Python list of all ordered user IDs is returned by default. Optional `n_similar` limits the result. The function works with either numeric user IDs or email keys. The recommender functions use the detected interaction user column.

**Data and outcome:** The sample matrix is binary with shape `(30, 20)` and sparsity `71.33%`. Sample user 1's first five neighbors are `[8, 22, 29, 15, 6]`. Full-list return type/order, recommendation, cold-start, email-key, and reviewer API-key assertions pass.

The reviewer benchmark examples are:

- User 1: `[3933, 46, 4201, 253, 824, 5034, 5041, 136, 2305, 395]`
- User 3933: `[1, 46, 4201, 253, 824]`
- User 46: `[4201, 790, 5077]`

**Benchmark outcome: NOT VERIFIED.** Those IDs are absent from the bundled user IDs `1–30`. The notebook only asserts the lists if every referenced ID is present in the loaded matrix.

## Part IV: Create Rank Based Recommendations

**Reviewer finding and initial status:** FAIL. Recommendations used article-wide pairwise similarity instead of the required same-cluster candidate set followed by popularity ranking.

**Fix:** The content pipeline transforms article text with TF-IDF and LSA/TruncatedSVD, runs K-Means across feasible cluster counts, and selects using the inertia elbow. Both user- and article-based content recommendations first restrict candidates to the matching cluster, exclude previously read items when appropriate, and then rank by total interaction popularity.

**Data and outcome: PASS on sample.** There are 20 article texts; candidates are bounded to `k=2–19`, and the elbow selection is `k=12`. The cluster/popularity assertions pass. Review the [K-Means inertia chart](results/charts/kmeans_inertia_elbow.png), [inertia datapoints](results/kmeans_inertia_points.csv), and [article cluster assignments](results/article_cluster_assignments.csv).

The reviewer’s full community file has 1,051 articles, making a candidate `k=50` feasible. The full content corpus was not present, so its elbow and selected `k` remain NOT VERIFIED.

## Part V: Matrix Factorization

**Reviewer finding and initial status:** FAIL. Latent-feature selection lacked a performance-based explanation, and article vectors could be indexed against metadata IDs rather than the interaction matrix columns.

**Fix:** The notebook evaluates holdout RMSE and explained variance, plots both against component count, and explains the smallest-count-within-0.01-RMSE selection rule. `get_svd_similar_article_ids(article_id, user_item_matrix, vt, n)` maps item vectors directly through `user_item_matrix.columns` and computes cosine similarity on the reduced `Vᵀ` item vectors.

**Sample outcome: PASS.** The sample matrix has 20 item columns, so at most 19 components can be evaluated. The selected model uses 5 components, holdout RMSE `0.3924`, and explained variance `81.43%`. The SVD neighbor example for the first article is `[8, 15, 7, 14, 2]`; matrix-column alignment and result-shape assertions pass. See the [feature chart](results/charts/svd_feature_selection.png), [feature datapoints](results/svd_feature_metrics.csv), and [SVD neighbors](results/recommendations_example_article_svd.csv).

The reviewer’s canonical interaction matrix has 714 item columns, so 200 components are feasible and included in the full-data evaluation range. **The 200-feature performance and justification are NOT VERIFIED locally** because the full matrix is not available; the sample cannot support 200 components.

## Next Steps

1. Supply the canonical interaction and community CSVs to reproduce the reviewer’s stated totals and numeric neighbor benchmarks.
2. Run the notebook from a fresh kernel with all canonical files available; confirm the logged `canonical_similarity_benchmark_status` and the measured 200-component RMSE/variance before claiming full-data certification.
3. Run the separately supplied project test module if it becomes available; no `project_tests.py` was present in this checkout.

## Reviewer Note

The existing sample-based checks establish that the corrected code paths execute and pass on the committed sample. They do not substitute for full-corpus benchmark confirmation. Current run metrics are in [review_metrics.json](results/review_metrics.json); expanded execution details are in [output_files/EXECUTION_RESULTS.md](output_files/EXECUTION_RESULTS.md) and the criteria summary is in [output_files/RUBRIC_COMPLIANCE_REPORT.md](output_files/RUBRIC_COMPLIANCE_REPORT.md).
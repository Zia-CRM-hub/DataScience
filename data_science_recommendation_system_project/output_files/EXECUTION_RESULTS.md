# Latest Notebook Execution Results

**Run date:** 2026-10-05

**Dataset profile:** Bundled project sample
**Notebook:** `recommendationsystem_ibmcommunity_analysis.ipynb`

## Run Status

All notebook code cells have successful execution records. The following notebook validations passed on the bundled sample:

- `test_all_functions()` - exploration, ranking, collaborative filtering, content recommendations, SVD, alternate `email` schema, optional article metadata, and reviewer API signatures.
- `test_edge_cases()` - cold-start, sparse user, oversized request, and missing-user cases.
- `test_data_validation()` - columns, IDs, duplicates, and article references.
- Notebook diagnostics - no errors reported.

The numeric similar-user benchmark IDs from the reviewer were skipped because they are not present in the bundled sample. The separate `project_tests.py` file was not present in this checkout.

## Dataset Statistics

| Metric | Latest value |
| --- | ---: |
| User identifier column | `user_id` |
| User-article interactions | 172 |
| Unique users | 30 |
| Unique articles in interactions | 20 |
| Articles in metadata | 20 |
| Median interactions per user | 6.0 |
| Maximum interactions by a user | 6 |
| Maximum views for an article | 9 |
| Most-viewed article ID | 4 |
| User-item matrix | 30 × 20 |
| Matrix sparsity | 71.33% |

## Recommendation Results

Top articles are tied at 9 interactions each; deterministic ID ordering resolves ties. The complete ranked output is in [top_articles.csv](../results/top_articles.csv).

For sample user 1, dot-product similarity returns the ordered neighbors `[8, 22, 29, 15, 6]`. The exported collaborative example and user-content example are available at [recommendations_example_user_collaborative.csv](../results/recommendations_example_user_collaborative.csv) and [recommendations_example_user_content.csv](../results/recommendations_example_user_content.csv).

For article 1, cluster-popularity recommendations are article IDs `2, 4, 5, 8, 9, 3, 6, 7`. The reduced 5-feature SVD neighbor IDs are `8, 15, 7, 14, 2`. Full outputs: [article content recommendations](../results/recommendations_example_article_content.csv) and [SVD article recommendations](../results/recommendations_example_article_svd.csv).

## Content Clustering

The content workflow transforms TF-IDF features with LSA/TruncatedSVD, fits K-Means over feasible candidate counts, and selects the elbow at `k=12` for this sample. The inertia reaches approximately zero at that point. Review the [elbow chart](../results/charts/kmeans_inertia_elbow.png), [inertia points](../results/kmeans_inertia_points.csv), and [article cluster assignments](../results/article_cluster_assignments.csv).

The current 20-article sample bounds candidate clusters to `2–19`. The reviewer’s canonical content table contains 1,051 articles, where a 50-cluster candidate is feasible; that full corpus was not available for this run.

## SVD Feature Evaluation

The sample user-item matrix has 20 item columns, so at most 19 components were evaluated. The selected model uses 5 components with holdout RMSE `0.3924` and cumulative explained variance `81.43%`. See the [RMSE/variance chart](../results/charts/svd_feature_selection.png) and [feature datapoints](../results/svd_feature_metrics.csv).

The reviewer’s canonical interaction matrix has 714 article columns, making 200 components dimensionally feasible. The notebook evaluates up to 200 when that full matrix is supplied; this run does not claim that 200 is optimal because the canonical data and its holdout results are unavailable.

## Machine-Readable Summary

The authoritative summary for this run is [review_metrics.json](../results/review_metrics.json). It records the dataset profile and marks canonical numeric-ID benchmarks as not verified rather than presenting them as passing.

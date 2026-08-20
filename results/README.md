# Compact result summaries

These CSV files mirror the principal numerical tables in the submitted manuscript and the corresponding executed notebooks. Lower is better for MSE/MAE columns.

- `01_main_retrieval_summary.csv`: six-dataset retrieval evidence; SARAF-Matched is available for the four confirmatory datasets.
- `02_supervision_feature_ablation.csv`: Pattern, Pattern+Context, architecture-matched Shuffled MLP, and Correct Future-Supervised MLP.
- `03_similarity_robustness.csv`: full-memory conventional similarity comparisons.
- `04_candidate_pool_coverage.csv`: Full L2 vs. L2 within Pattern Top-100; fractional penalty/gain columns use 0.10 = 10%.
- `05_finance_multihorizon.csv`: Same/Cross Pattern/Learned retrieval at H=1,5,20.
- `06_finance_direct_comparison.csv`: strongest direct baseline reported at each horizon vs. frozen retrieval forecast.

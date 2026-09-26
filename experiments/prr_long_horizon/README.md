# Main PRR long-horizon pipeline

These notebooks correspond to the final aligned protocol in the paper. They intentionally preserve experiment-level assertions that stop on missing or mismatched artifacts instead of silently regenerating a different protocol.

Recommended order:

1. `00_freeze_evaluation_manifests.ipynb` — deterministic validation/test query-channel manifests.
2. `01_full_prr_training.ipynb` — reproducibility-focused reproduction of the 24 full PRR stacks.
3. `01_prr_retrieval_inference.ipynb` — PRR candidate union and fusion-reranker inference from those full-stack checkpoints.
4. `02_prr_stat_ablation.ipynb` — restricted fixed-Pearson-support PRR-Stat ablation on the common stride-8 memory grid.
5. `03_pearson_exact_baseline.ipynb` — exact Pearson Top-10 baseline on the same frozen test manifests and common stride-8 memory grid.
6. `04_fixed_trust_120_conditions.ipynb` — five-backbone, 120-condition common-trust (`beta=0.1`) control.
7. `05_global_dataset_trust_calibration.ipynb` — global and dataset-level validation-only trust checks.
8. `06_condition_trust_calibration.ipynb` — final validation-only condition-specific trust calibration.
9. `07_matched_pool_feature_ablation.ipynb` — supplementary matched-pool learned-feature/support diagnostic.
10. `08_stride8_alignment_audit_executed.ipynb` — executed post-audit revalidation of the common stride-8 long-horizon protocol and revised paper-facing retrieval table.

## Large generated artifacts

The package omits datasets, trained PRR checkpoints, direct-forecast caches, and per-channel retrieval arrays because they are generated artifacts and dominate archive size. `01_full_prr_training.ipynb` now supplies the complete training code required to regenerate the 24 PRR stacks. `01_prr_retrieval_inference.ipynb` first looks for those reproduced stacks and otherwise accepts the original experiment checkpoints when `PRR_ROOT` points to the historical working repository.

The final PRR checkpoint schema contains `query_encoder`, `history_encoder`, `reranker`, `stats_med`, `stats_iqr`, and `rerank_best_epoch`; reproduced stacks additionally store dataset/horizon and training-range metadata. The inference-critical architecture is mirrored in `scripts/prr_core.py`.

The fast verification path in the root README does not require these large artifacts.

11. `09_anchored_l2_frozen24_executed.ipynb` — executed deterministic last-value-anchored-L2 stress test on the exact 24 frozen long-horizon retrieval manifests.
12. `10_anchored_l2_downstream_120_executed.ipynb` — executed anchored-L2 integration on the same five frozen forecasters with the identical validation-only seven-point trust grid, including the exact paired comparison with full PRR.
13. `11_anchored_prr_strong_base_frozen24_executed.ipynb` — executed strong-base substitution ablation: anchored-L2 Top-100 replaces Pearson Top-100, the original future-supervised learned branch is frozen, and only the fusion reranker is retrained. The notebook reports exact 24-condition A-PRR comparisons and learned-only support usage.
14. `12_craft_matched_retrieval_frozen24_executed.ipynb` — executed matched CRAFT retrieval-rule diagnostic. It reports CRAFT-SC@10 and the train-only top-3 channel-graph CRAFT-Graph@10 variant on the exact frozen retrieval manifests. The paper treats the four-dataset/16-condition overlap with CRAFT's reported benchmark as the primary scope and labels the all-six-dataset result as secondary. This is not an end-to-end CRAFT forecasting reproduction.

15. `13_raft_matched_retrieval_frozen24_executed.ipynb` — executed matched RAFT retrieval-rule diagnostic. It preserves RAFT's three temporal granularities, Top-20 per-scale retrieval, and temperature-0.1 weighting, and reports both a multiscale Top-10 projection and a validation-selected single-scale control on the exact frozen 24-condition protocol. This is not an end-to-end RAFT forecasting reproduction.
16. `14_prr_budget100_frozen24_executed.ipynb` — executed candidate-budget-matched inference control. It reuses the frozen full-PRR checkpoints, truncates the Pearson and learned branches to Top-50 each before unioning (at most 100 distinct candidates), and evaluates the same Top-10 AnalogFutureMSE on all 24 frozen test conditions. The mean union is 94.93; PRR-B100 improves Pearson in 23/24 conditions (+26.56% mean) and PRR-Stat in 22/24 (+11.32% mean). Because the checkpoints were trained under full support, this is an inference-budget control rather than a training-support ablation.

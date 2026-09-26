# Frozen paper-facing results

The top-level CSVs in this directory correspond to the current PRR manuscript. Lower MSE/MAE is better; gain columns are percentage reduction relative to the named baseline.

- `main_retrieval_24.csv`: headline Pearson vs. PRR AnalogFutureMSE comparison under the common stride-8 memory grid.
- `retrieval_24_conditions.csv`: Pearson -> PRR-Stat -> PRR decomposition used as an ablation, with all three aligned on stride 8.
- `frozen_manifest_audit_48.csv`: exact validation/test query-channel coverage for 6 datasets x 4 horizons.
- `prr_support_geometry.csv`: full-PRR and PRR-B100 candidate-support geometry used in Appendix C.
- `fixed_trust_120_conditions.csv`: complete 5-backbone common-trust beta=0.1 control (120 conditions).
- `calibration_overall.csv`: fixed-trust versus final validation-only condition calibration.
- `calibration_by_dataset.csv`, `calibration_by_backbone.csv`, `calibration_by_horizon.csv`: calibrated downstream summaries.
- `selected_beta_distribution.csv`: validation-selected beta counts.
- `calibration_generalization.csv`: validation/test calibration audit.
- `stride8_revalidation_summary.csv`: W/T/L and mean/median gains after the common-stride audit.
- `relevance_to_utility_bridge_24.csv`: revised paper-facing retrieval gains paired with the frozen fixed-trust downstream summary.
- `anchored_l2_long_horizon_summary.csv`: matched 24-condition anchored-L2 retrieval stress-test summary used in Appendix G.
- `anchored_l2_downstream_dataset_summary.csv`: dataset-level 120-condition anchored-L2 downstream calibration summary used in Appendix G.
- `anchored_prr_strong_base_24.csv`: exact 24-condition strong-base substitution comparison (A-PRR vs. anchored L2, current PRR, and Pearson) with support-usage diagnostics.
- `anchored_prr_strong_base_overall.csv`: overall W/T/L and mean/median gain summary for the three A-PRR comparisons.
- `anchored_prr_strong_base_by_dataset.csv`: dataset-level A-PRR comparison and learned-only support summary used in Appendix G.
- `craft_frozen24_raw.csv`: raw matched CRAFT-SC/CRAFT-Graph retrieval metrics on the frozen validation/test protocol.
- `craft_matched_exact_24.csv`: exact 24-condition Pearson/PRR/anchored-L2/CRAFT comparison, including PRR-vs-CRAFT effect sizes.
- `craft_matched_summary.csv`: W/T/L and mean/median matched CRAFT comparison for the 16-condition CRAFT-overlap scope and all 24 conditions.
- `craft_matched_dataset_summary.csv`: dataset-level CRAFT diagnostic and cross-channel-support summary.
- `raft_manifest_audit.csv`: exact validation/test manifest audit used by the matched RAFT diagnostic.
- `raft_matched_val_test_raw.csv`: validation/test AnalogFutureMSE for RAFT-MS and each official temporal granularity.
- `raft_matched_test_with_valscale.csv`: validation-selected RAFT granularity and frozen test result for all 24 conditions.
- `raft_matched_exact_24.csv`: exact Pearson/PRR/anchored-L2/RAFT comparison with PRR-vs-RAFT effect sizes.
- `raft_matched_summary.csv`: W/T/L and mean/median summary for RAFT-MS and RAFT-ValScale matched comparisons.
- `raft_matched_dataset_summary.csv`: dataset-level RAFT matched-retrieval diagnostic and selected-scale summary.
- `prr_budget100_test_24.csv`: exact 24-condition PRR-B100 inference-control outputs and support geometry.
- `prr_budget100_exact_24.csv`: PRR-B100 joined with the aligned Pearson, PRR-Stat, full-PRR, and RAFT-ValScale references.
- `prr_budget100_summary.csv`: W/T/L and mean/median effect-size summary for PRR-B100 vs. Pearson, PRR-Stat, and full PRR.
- `table1_matched_retrieval_24.csv`: exact columns used in the revised main Table 1 (full PRR, PRR-B100, PRR-Stat, RAFT-ValScale, Pearson).
- `full_prr_training_config.csv`: recovered full-PRR training hyperparameters from the original training sources.
- `full_prr_training_geometry.csv`: dataset/horizon-specific train-only memory size, training-channel count, and training-pair budget used by the supplementary training notebook.

`prr_stat_diagnostics/` contains appendix ablations/diagnostics. `backbone_provenance/` retains compact outputs from the frozen-backbone execution path.

- `full_prr_training_recipe.csv` — recovered frozen hyperparameters for the reproducibility-focused full-PRR training notebook.

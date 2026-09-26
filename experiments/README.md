# Experiments

The supplementary package separates the current main method from fixed-support diagnostic experiments.

- `prr_long_horizon/`: final PRR evaluation, exact Pearson baseline, strong deterministic/external retrieval diagnostics (anchored L2, Anchored-PRR, matched CRAFT, and matched RAFT), the PRR-B100 inference control, 120-condition downstream integration, and validation-only trust calibration.
- `prr_stat_diagnostics/`: fixed-Pearson-support PRR-Stat mechanism controls, supervision ablations, similarity robustness, candidate-pool diagnostics, and SARAF-Matched checks. These are ablations/diagnostics, not a second main method.
- `backbone_provenance/`: notebooks used to reproduce or audit frozen PatchTST, iTransformer, TimeMixer, Seg-MoE, and DLinear forecasts and related downstream arrays.

## Path configuration

For the current main notebooks, set:

```bash
export PRR_ROOT=/path/to/which-histories-matter
export PRR_DATA_ROOT=/path/to/datasets   # optional if using data/ layout
```

Some historical diagnostic notebooks retain legacy internal names such as `Ours`, `PR-Stat`, or `PR-Hybrid` solely to preserve correspondence with frozen intermediate artifacts. In the current manuscript, PRR is the only main method and PRR-Stat is a restricted ablation; see `prr_stat_diagnostics/README.md`.

Large generated checkpoints/caches should live under the working root and are excluded from the supplementary zip.

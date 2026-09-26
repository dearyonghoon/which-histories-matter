# Which Histories Matter for Time Series Forecasting?

Official code and reproducibility package for *Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision*.

The current paper has one main retrieval method, **Predictive Relevance Retrieval (PRR)**. **PRR-B100** is its inference-only candidate-budget control, reusing the same frozen full-PRR checkpoint while limiting the test-time candidate pool to at most 100; **PRR-Stat** is the more restricted fixed-Pearson-support ablation.

## Fast verification (CPU, seconds)

```bash
python scripts/verify_frozen_results.py
```

The verifier checks the paper-facing frozen CSVs and the current headline claims:

- Pearson vs. PRR retrieval: 23/24 wins, approximately 26.7% mean AnalogFutureMSE reduction under the common stride-8 memory grid;
- common-trust `beta=0.1` control: 79W/0T/41L over 120 frozen-backbone conditions, +0.97% mean MSE gain;
- validation-only condition calibration: 79W/15T/26L, 94/120 non-degraded, +1.41% mean MSE gain;
- 15/120 validation-selected `beta=0` Direct fallbacks and the reported validation/test calibration audit.
- strong-base substitution: A-PRR vs. current PRR 19W/0T/5L; A-PRR vs. anchored L2 6W/0T/18L, with 45.2% learned-only final Top-10 selections.
- matched CRAFT retrieval diagnostic: CRAFT-Graph vs. Pearson 11W/0T/5L on the 16-condition CRAFT-overlap scope, while PRR is lower than CRAFT-Graph in 16/16 conditions (+33.68% mean PRR-vs.-CRAFT AnalogFutureMSE reduction).
- matched RAFT retrieval diagnostic: RAFT-ValScale vs. Pearson 15W/0T/9L over all 24 conditions, while PRR is lower than both RAFT-MS and RAFT-ValScale in 22/24 conditions (about 20% mean PRR-vs.-RAFT AnalogFutureMSE reduction).
- candidate-budget control: PRR-B100 uses the same frozen full-PRR model but caps inference support at Pearson Top-50 + learned Top-50 (mean union 94.93, maximum 100); it improves Pearson in 23/24 conditions (+26.56% mean) and PRR-Stat in 22/24 (+11.32% mean), while trailing full PRR by only 0.25% on average.

## Main reproducibility path

See `experiments/prr_long_horizon/README.md`. The notebooks train the 24 full PRR stacks, freeze the evaluation manifests, evaluate PRR and Pearson on identical pairs, reproduce the PRR-Stat ablation, assemble the 120-condition fixed-trust control, and apply validation-only trust calibration.

## Appendix diagnostics

- `experiments/prr_stat_diagnostics/`: fixed-support mechanism/ablation studies;
- `experiments/backbone_provenance/`: frozen forecasting-backbone provenance notebooks;

Legacy diagnostic notebooks may contain internal labels such as `Ours`, `PR-Stat`, or `PR-Hybrid` from earlier experiment names. In the current paper these map to **PRR-Stat (ablation)** and **PRR (main method)** as documented in `experiments/prr_stat_diagnostics/README.md`; the legacy variable names are retained only where changing them would obscure correspondence with frozen artifacts.

Large benchmark files, trained PRR checkpoints, direct prediction caches, and per-query retrieval arrays are omitted because they are generated artifacts. The full PRR training notebook regenerates the retrieval checkpoints; downstream notebooks stop on missing/mismatched artifacts rather than silently substituting a different protocol.

See `REPRODUCIBILITY.md` for the execution contract and artifact layout.

## Anchored-L2 stress tests

Two executed notebooks in `experiments/prr_long_horizon/` document the strong deterministic last-value-anchored-L2 diagnostic added in Appendix G. On the exact 24 frozen retrieval manifests, anchored L2 improves over Pearson in 24/24 conditions (26.25% mean AnalogFutureMSE reduction). Under the same 120-condition validation-only downstream trust protocol, calibrated anchored L2 yields 82W/14T/24L and +1.855% mean MSE gain vs. Direct; the exact paired comparison with calibrated full PRR is 64W/10T/46L with a +0.463% mean L2-vs.-PRR MSE advantage. These diagnostics are reported as domain-dependent stress tests rather than a replacement for the main PRR method.


A third executed notebook, `11_anchored_prr_strong_base_frozen24_executed.ipynb`, performs the strong-base substitution ablation from Appendix G. It replaces Pearson Top-100 with anchored-L2 Top-100 while retaining the frozen future-supervised learned Top-100 branch and retraining only the fusion reranker. A-PRR improves the original Pearson-based PRR in 19/24 conditions (+0.840% mean, +1.374% median) but improves standalone anchored L2 in only 6/24 conditions (+1.634% mean, -2.385% median). The mean union size is 173.8, with 73.8 learned-only candidates, and 45.2% of the final Top-10 selections come from outside anchored-L2 Top-100.


## Matched CRAFT retrieval diagnostic

`12_craft_matched_retrieval_frozen24_executed.ipynb` evaluates CRAFT's retrieval rule under the frozen PRR retrieval protocol. The paper-facing primary scope is the 16 conditions from ETTh1, Weather, Electricity, and Traffic, the four datasets shared with CRAFT's reported benchmark. CRAFT-Graph improves Pearson in 11/16 conditions (+1.837% mean), while PRR has lower AnalogFutureMSE in all 16 (+33.681% mean PRR-vs.-CRAFT reduction). The notebook also reports the same-channel frequency-only CRAFT-SC variant and the secondary all-six-dataset summary. This is a retrieval-rule diagnostic, not an end-to-end reproduction of CRAFT's forecasting system.


## Matched RAFT retrieval diagnostic

`13_raft_matched_retrieval_frozen24_executed.ipynb` evaluates the public RAFT retrieval rule under the same frozen 24-condition history-relevance protocol. The notebook preserves RAFT's three temporal granularities (`g={4,2,1}`), Top-20 candidates per scale, and temperature-0.1 weighting, then reports two transparent Top-10 projections because the original forecasting architecture consumes scale-specific retrievals rather than defining one unique Top-10 list. `RAFT-MS@10` averages softmax probability mass across scales, while `RAFT-ValScale@10` selects one official granularity using validation AnalogFutureMSE only and freezes it on test.

RAFT-MS improves Pearson in 13/24 conditions (+7.57% mean), and the stronger validation-selected RAFT control improves Pearson in 15/24 (+7.90% mean). PRR nevertheless has lower AnalogFutureMSE in 22/24 conditions against both RAFT projections; the two RAFT wins occur on Exchange at H=192 and H=336. This is explicitly a matched retrieval-rule diagnostic, not an end-to-end reproduction of RAFT's forecasting benchmark.

## Candidate-budget-matched PRR control

`14_prr_budget100_frozen24_executed.ipynb` addresses whether full PRR benefits simply because its Top-100 + Top-100 union exposes about 183 test-time candidates. The control reuses the same frozen full-PRR checkpoints but truncates each inference branch to Top-50 before unioning. The resulting union contains 94.93 candidates on average (median 97, maximum 100). PRR-B100 still improves Pearson in 23/24 conditions (+26.56% mean AnalogFutureMSE reduction) and improves PRR-Stat in 22/24 (+11.32% mean). Relative to full PRR it gives 11W/0T/13L and -0.25% mean gain, showing that nearly all headline retrieval benefit survives without a larger-than-100 inference candidate budget. This does not establish that broader support is unnecessary during training, because the frozen checkpoint was trained under the full PRR support.

# Reproducibility contract

## 1. Fast frozen-result verification

Run:

```bash
python scripts/verify_frozen_results.py
```

This path needs only Python 3 and the included CSV files. It verifies current-paper row counts and headline aggregates without a GPU.

## 2. Aligned retrieval protocol

The final retrieval benchmark uses ETTh1, Weather, Electricity, Traffic, Exchange, and Solar at horizons 96, 192, 336, and 720. Retrieval lookback is 96 and all aligned methods use a common memory-window stride of 8. Full PRR forms independent Pearson Top-100 and learned-representation Top-100 lists and returns Top-10 analogs; PRR-B100 reuses the same frozen full-PRR checkpoint but truncates both branches to Top-50 before unioning, capping the test-time candidate pool at 100; the more restricted PRR-Stat ablation reranks only the fixed Pearson Top-100 support. Frozen evaluation anchors require at least 512 preceding observations so the same manifests can be reused across the downstream forecasting study. Validation/test methods reuse the same deterministic query-channel manifests. Candidate futures must be fully observed before the query boundary. ETTh1 uses the fixed chronological boundaries `train_end=8640`, `val_end=11520`, and `test_end=len(ETTh1)`; thus its test region is the remaining 5,900 observations rather than a four-month cap. The same ETTh1 boundaries are used by the aligned long-horizon PRR evaluation and the ETTh1 mechanism diagnostics. Weather uses Python-style exclusive boundaries `train_end=36887` and `val_end=42157`; the remaining non-ETT benchmarks use chronological 70/10/20 splits.

`experiments/prr_long_horizon/00_freeze_evaluation_manifests.ipynb` creates the manifests. `03_pearson_exact_baseline.ipynb` reproduces the conventional Pearson baseline under the common stride-8 grid. `02_prr_stat_ablation.ipynb` uses the same stride-8 grid for the fixed-support ablation. `01_full_prr_training.ipynb` reconstructs the 24 full PRR stacks from raw training data, and `01_prr_retrieval_inference.ipynb` reconstructs full PRR retrieval from those checkpoints. `08_stride8_alignment_audit_executed.ipynb` records the post-audit revalidation that established the paper-facing aligned numbers.

### PRR checkpoint contract

Inference-critical fields are:

- `query_encoder`
- `history_encoder`
- `reranker`
- `stats_med`
- `stats_iqr`
- `rerank_best_epoch`

The final architecture is mirrored in `scripts/prr_core.py`: three Conv1d stages -> 64-D unit-normalized embeddings and a 285-D two-block residual fusion MLP. Full stacks are trained separately per dataset and horizon. The supplementary training notebook reproduces the original source protocol: 100 encoder candidates/query (50 Pearson-hard + 50 random), standardized future-distance teacher with temperature 0.5, embedding-student temperature 0.10, 20 encoder epochs, and a fusion reranker trained with listwise supervision plus a unit-weight Top-K-aware pairwise softplus term. The non-ETTh1 stacks use the frozen compute-matched training cap of at most 64 channels and 6,000 channel-anchor pairs; evaluation uses all channels. In the original lineage, ETTh1 H=192 reused a previously validated stack; the supplementary training notebook accepts `ETTH1_H192_SOURCE` to reuse that exact artifact when available, and otherwise retrains H=192 from the documented frozen recipe. The large generated checkpoint files are not included in this zip.

## 3. PRR-Stat fixed-support ablation

`02_prr_stat_ablation.ipynb` reproduces the restricted fixed-Pearson-support reranker. It isolates future-supervised reranking within Pearson support. Moving from PRR-Stat to full PRR additionally introduces learned embedding relations and an embedding-based candidate branch, so that increment is a combined representation-and-support effect rather than a pure support-only estimate. The original mechanism notebooks are grouped under `experiments/prr_stat_diagnostics/`. They are not the main method.

## 4. Frozen forecasters and 120-condition integration

The downstream study uses PatchTST, iTransformer, TimeMixer, Seg-MoE, and DLinear on 6 datasets x 4 horizons = 120 conditions. Direct forecasts are generated once and then frozen. `04_fixed_trust_120_conditions.ipynb` reproduces the common-trust `beta=0.1` control from matching direct/retrieval caches.

## 5. Validation-only trust calibration

The final paper selects one scalar per `(dataset, horizon, backbone)` condition using validation MSE only:

```text
beta in {0, .025, .05, .075, .10, .15, .20}
```

The chosen beta is frozen on test. `beta=0` is an exact Direct fallback. The frozen paper-facing summaries verify that fixed `beta=0.1` gives 79W/0T/41L, condition calibration gives 79W/15T/26L, and 15/120 conditions select `beta=0`. These are reported as separate aggregate facts. When the generated caches are available, `06_condition_trust_calibration.ipynb` also emits the per-condition selected-beta and calibrated-test tables. It is the final calibration notebook; `05_global_dataset_trust_calibration.ipynb` is the lower-capacity sensitivity check. No retriever or forecaster is retrained during calibration.

## 6. Environment and data

Install:

```bash
pip install -r requirements.txt
```

Set the repository root when running the long-horizon notebooks:

```bash
export PRR_ROOT=/path/to/which-histories-matter
```

Place datasets as documented in `data/README.md`. External forecasting repositories/checkpoints used by the provenance notebooks are configured in their first cells. Full forecasting reruns are GPU-intensive; the frozen-result verification and trust sweeps are lightweight.

## 7. Leakage safeguards

The final notebooks assert all of the following:

- train-only channel normalization;
- chronological memory/query boundaries;
- candidate future end before the relevant query boundary;
- exact query/channel manifest equality across compared methods;
- validation-only trust selection;
- no test-query future in candidate generation, reranker scoring, normalization, or trust selection.

## 8. Strong-base retriever substitution

`experiments/prr_long_horizon/11_anchored_prr_strong_base_frozen24_executed.ipynb` tests whether the full PRR framework is tied to Pearson as its deterministic candidate branch. Anchored-PRR (A-PRR) replaces Pearson Top-100 with last-value-anchored-L2 Top-100, retains the frozen future-supervised learned-representation Top-100 branch from the corresponding full-PRR stack, unions the two supports, and retrains only the fusion reranker with the same future-supervised hybrid objective. The anchored base ranking is represented by query-wise standardized negative anchored MSE, which preserves the exact anchored-L2 ordering.

On the exact 24 frozen long-horizon manifests, A-PRR improves the original PRR in 19/24 conditions (+0.840% mean, +1.374% median) but improves standalone anchored L2 in only 6/24 conditions (+1.634% mean, -2.385% median). The mean candidate union contains 173.8 histories, including 73.8 learned-only candidates outside anchored-L2 Top-100; 45.2% of the final Top-10 selections are learned-only. This is a strong-base substitution ablation, not a replacement of the paper's primary PRR method.



## 9. Matched CRAFT retrieval-rule diagnostic

`experiments/prr_long_horizon/12_craft_matched_retrieval_frozen24_executed.ipynb` addresses the baseline-strength question with a matched implementation of CRAFT's retrieval component. The frozen PRR protocol remains unchanged (`L=96`, stride 8, Top-10 AnalogFutureMSE, identical query-channel manifests). `CRAFT-SC@10` applies the low-frequency complex-FFT score within same-channel memory; `CRAFT-Graph@10` additionally uses a train-only top-3 channel-similarity graph and searches historical keys from those graph channels. With `L=96`, the notebook retains `F=5` low-frequency coefficients, preserving CRAFT's 5% frequency-ratio design.

The primary paper-facing scope is the 16 conditions from ETTh1, Weather, Electricity, and Traffic, the four datasets shared with CRAFT's reported benchmark. CRAFT-Graph improves Pearson in 11/16 conditions (+1.837% mean), while PRR has lower AnalogFutureMSE than CRAFT-Graph in all 16 conditions (+33.681% mean PRR-vs-CRAFT reduction). Across all six datasets, CRAFT-Graph improves Pearson in 16/24 conditions and PRR is lower in 18/24. The all-six-dataset summary is secondary because Exchange and Solar are outside the reported CRAFT benchmark overlap. The notebook is explicitly a retrieval-rule diagnostic, not a reproduction of CRAFT's direct forecaster or end-to-end forecasting benchmark.


## 10. Matched RAFT retrieval-rule diagnostic

`experiments/prr_long_horizon/13_raft_matched_retrieval_frozen24_executed.ipynb` adapts the public RAFT retrieval rule to the exact frozen PRR long-horizon protocol. It uses the same six datasets, horizons `{96,192,336,720}`, lookback `L=96`, stride-8 temporally admissible memory, train-only normalization, frozen query-channel manifests, and Top-10 AnalogFutureMSE evaluation.

The implementation preserves the public RAFT retrieval ingredients: temporal granularities `g={4,2,1}`, endpoint-offset removal, flattened multivariate normalized correlation, Top-20 candidates per scale, and temperature `0.1`. Because the original RAFT forecasting architecture consumes separate scale-specific retrievals rather than defining one unique Top-10 history list, the notebook reports two matched projections:

- `RAFT-MS@10`: averages the official Top-20 softmax probability mass across the three scales and selects the final Top-10 histories;
- `RAFT-ValScale@10`: chooses the best official granularity on validation AnalogFutureMSE only and freezes it on test.

The validation-selected control improves Pearson in 15/24 conditions (+7.905% mean). PRR has lower AnalogFutureMSE in 22/24 conditions against both RAFT-MS and RAFT-ValScale; the two RAFT wins are Exchange at H=192 and H=336. The notebook is a retrieval-rule comparison under the paper's frozen relevance metric, not a reproduction of RAFT's end-to-end forecasting benchmark.

## 11. Candidate-budget-matched inference control

`experiments/prr_long_horizon/14_prr_budget100_frozen24_executed.ipynb` reuses the trained full-PRR stacks and changes only the inference candidate support from Pearson Top-100 + learned Top-100 to Pearson Top-50 + learned Top-50. The resulting union is at most 100 distinct histories (94.93 on average; median 97), while all other retrieval settings, frozen query-channel manifests, temporal-admissibility rules, reranker parameters, and Top-10 AnalogFutureMSE evaluation remain unchanged.

Across the 24 conditions, PRR-B100 improves Pearson in 23/24 conditions (+26.56% mean, +27.05% median), improves PRR-Stat in 22/24 (+11.32% mean), and is nearly tied with full PRR (11W/0T/13L; -0.25% mean gain for Budget100 vs. full PRR). This is an inference-budget control only: the underlying checkpoint was trained using the full Top-100 + Top-100 support, so the diagnostic does not claim that broader candidate support is unnecessary during training.

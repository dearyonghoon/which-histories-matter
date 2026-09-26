# Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision

Official code and reproducibility package for the paper **Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision**.

The current release centers on **Predictive Relevance Retrieval (PRR)**. PRR learns historical relevance from future supervision available only during training, while inference uses only past-observable information. **PRR-B100** is an inference-only candidate-budget control using the same frozen full-PRR checkpoint, and **PRR-Stat** is the fixed-Pearson-support ablation.

## Fast verification

```bash
python scripts/verify_frozen_results.py
```

The verifier checks the frozen CSVs and current paper-facing headline results, including the 24-condition retrieval benchmark, 120-condition downstream trust study, matched CRAFT/RAFT diagnostics, strong-base substitution, and PRR-B100 candidate-budget control.

## Main reproducibility path

See [`experiments/prr_long_horizon/README.md`](experiments/prr_long_horizon/README.md). The notebooks train the full PRR stacks, freeze evaluation manifests, compare PRR and Pearson on identical pairs, reproduce the PRR-Stat ablation, assemble the 120-condition fixed-trust control, and apply validation-only trust calibration.

Additional directories:

- `experiments/prr_stat_diagnostics/`: fixed-support mechanism and ablation studies;
- `experiments/backbone_provenance/`: forecasting-backbone provenance notebooks;
- `results/`: frozen paper-facing CSVs and audit summaries;
- `scripts/prr_core.py`: compact implementation of the final PRR encoder/reranker architecture.

Large datasets, checkpoints, prediction caches, and per-query retrieval arrays are intentionally omitted because they are generated artifacts. Full details of the execution contract and artifact layout are in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Repository structure

```text
which-histories-matter/
├── README.md
├── REPRODUCIBILITY.md
├── requirements.txt
├── data/
├── experiments/
│   ├── prr_long_horizon/
│   ├── prr_stat_diagnostics/
│   └── backbone_provenance/
├── results/
└── scripts/
    ├── prr_core.py
    └── verify_frozen_results.py
```

## Authors

Yong-Hoon Choi, Kwang-Hyun Park, and Youngjin Cho  
Division of Robotics, Kwangwoon University, Seoul, Republic of Korea.

# Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision

Official code and experiments for the paper.

Historical similarity is useful for coarse candidate generation, but it need not be the final criterion for predictive relevance. This repository contains the RARanker experiments and the downstream evaluation with frozen strong forecasters.

## Overview

1. Coarse candidate generation using past-pattern similarity.
2. Predictive relevance reranking using a lightweight residual MLP trained with privileged future supervision.
3. Optional integration of the frozen historical memory with PatchTST, iTransformer, TimeMixer, and Seg-MoE.

Future trajectories are used only during training to construct soft relevance targets. At inference time, the reranker uses only past-observable information.

## Reproducibility

Start with the dependency-light frozen-result check:

```bash
python scripts/verify_frozen_results.py
```

The final strong-forecaster notebooks are in [`experiments/downstream/`](experiments/downstream/). They preserve the experiment identifiers used for provenance and require the public datasets, official backbone implementations, and substantial GPU compute for a full rerun. Aggregate outputs used by the manuscript are in [`results/downstream/`](results/downstream/).

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the fast verification path, full A100 rerun guidance, data requirements, and the result provenance map.

## Repository Structure

```text
which-histories-matter/
├── README.md
├── REPRODUCIBILITY.md
├── requirements.txt
├── data/
├── experiments/
│   ├── candidate_pool/
│   ├── mechanism/
│   ├── supervision_ablation/
│   ├── similarity_robustness/
│   ├── saraf_matched/
│   ├── finance/
│   └── downstream/
├── results/
│   ├── retrieval/
│   └── downstream/
└── scripts/
    └── verify_frozen_results.py
```

Intermediate caches, checkpoints, and generated files are intentionally excluded from version control.

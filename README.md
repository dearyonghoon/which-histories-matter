# Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision

Official code and experiments for the paper:

**Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision**

Historical similarity is useful for coarse candidate generation, but it need not be the final criterion for predictive relevance.  
This repository contains the experiments for learning predictive historical relevance from future information available only during training.

## Overview

Our framework consists of two stages:

1. **Coarse candidate generation** using past-pattern similarity.
2. **Predictive relevance reranking** using a lightweight residual MLP trained with privileged future supervision.

Future trajectories are used only during training to construct soft relevance targets.  
At inference time, the reranker uses only past-observable information.

## Reproducibility

The `experiments/` directory contains notebooks corresponding to the main
experiments reported in the paper.

The recommended execution order and the purpose of each notebook are described
in [`experiments/README.md`](experiments/README.md).

Intermediate caches, checkpoints, and generated files are stored under `_work/`
and are excluded from version control.

## Repository Structure

```text
which-histories-matter/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   └── README.md
├── experiments/
│   ├── confirmatory/
│   ├── mechanism/
│   ├── supervision_ablation/
│   ├── similarity_robustness/
│   ├── candidate_pool/
│   ├── saraf_matched/
│   └── finance/
└── results/


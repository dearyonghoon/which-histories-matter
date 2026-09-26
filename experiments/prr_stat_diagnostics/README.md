# PRR-Stat diagnostic notebooks

All experiments in this directory are **ablations or mechanism diagnostics**. They do not define the paper's main retrieval method.

Current naming:
- **PRR**: the main method, with learned embedding relations, learned candidate-support expansion, and fusion reranking.
- **PRR-Stat**: the restricted fixed-Pearson-support ablation using the seven statistical features and their 29-D pair representation.
- **Shuffled / Candidate Prior / Pearson+Context / similarity rules**: controls used only to interpret the PRR-Stat ablation.

Some older notebook code and frozen column names use `Ours` for what is now called **PRR-Stat**, or use provisional names such as `PR-Stat`. These legacy identifiers are retained where changing them would break correspondence with frozen outputs. They should not be interpreted as claiming that PRR-Stat is the proposed main method.

Short-horizon organization:
- **Electricity, Traffic, Exchange, and Solar** form the common five-seed confirmatory fixed-support suite, including the SARAF-Matched comparison.
- **ETTh1 and Weather** are reported separately under the dedicated three-seed mechanism protocol because they were designed as contrasting query-specific and candidate-global cases.
- Together these two protocol blocks cover all six benchmark datasets; the separation is deliberate and avoids mixing confirmatory and mechanism-oriented analyses.

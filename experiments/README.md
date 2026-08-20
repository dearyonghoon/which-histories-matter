# Experiments

Public reproducibility notebooks for **Which Histories Matter? Predictive Relevance from Privileged Futures**.

## Path configuration

Notebooks locate the repository root automatically. By default:

- benchmark datasets: `data/`
- generated caches, checkpoints, and large intermediate outputs: `_work/`

You can override these locations without editing the notebooks:

```bash
export WHM_DATA_ROOT=/path/to/datasets
export WHM_WORK_ROOT=/path/to/workdir
```

`_work/` should be excluded from Git. Add the following line to the root `.gitignore`:

```text
_work/
```

## Generic benchmark workflow

Mechanism diagnostics:

```text
mechanism/00_cross_domain_base.ipynb
    -> mechanism/01_etth1_weather_relevance.ipynb
    -> mechanism/02_candidate_prior.ipynb
```

Final confirmatory pipeline:

```text
confirmatory/confirmatory_benchmark.ipynb
    -> saraf_matched/saraf_matched_protocol.ipynb
    -> supervision_ablation/supervision_feature_ablation.ipynb
    -> similarity_robustness/similarity_robustness.ipynb
    -> candidate_pool/candidate_pool_coverage.ipynb
```

The similarity-robustness notebook reads the SARAF-Matched outputs, so run the SARAF notebook first. The candidate-pool notebook reuses confirmatory caches and similarity-analysis outputs.

## Financial case study

```text
finance/01_data_preparation.ipynb
    -> finance/02_crossstock_ablation.ipynb
    -> finance/03_multihorizon.ipynb
    -> finance/04_direct_baselines.ipynb
```

The last finance notebook additionally imports DLinear, PatchTST, and iTransformer from Time-Series-Library. Either clone it to `external/Time-Series-Library` or set:

```bash
export TSL_ROOT=/path/to/Time-Series-Library
```

For optional native SARAF checks, clone SARAF to `external/SARAF` or set `SARAF_REPO`.

## Notes

The public notebooks intentionally contain no saved execution outputs. Compact paper-result CSVs can be kept separately under the repository's `results/` directory.

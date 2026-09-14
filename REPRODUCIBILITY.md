# Reproducibility guide

This repository provides two paths. The **frozen-result path** validates the
reported paper numbers without downloading data or using a GPU. The
**full-rerun path** contains the final strong-forecaster notebooks used on an
A100 server; those notebooks require the public datasets, the corresponding
official backbone implementations, and substantial compute.

## Fast verification

From the repository root:

```bash
python scripts/verify_frozen_results.py
```

The script checks the presence and row counts of the 96-condition absolute
performance and significance audits, the four-backbone selection table, and
the 24-cell relevance-to-utility bridge.

## Full reruns

The notebooks in `experiments/downstream/` are the final execution records.
They are retained with their experiment identifiers for provenance. They are
not intended to be run as one batch: each notebook documents its dataset,
horizons, checkpoint conventions, and output directory. A full rerun requires
an A100-class GPU and the external backbone repositories described in the
notebook cells. Generated checkpoints, validation arrays, OOF arrays, and
datasets are intentionally not included in Git.

## Result provenance

The compact result bundle in `results/downstream/` contains the final aggregate
CSV files used to prepare the manuscript tables and bridge analyses. Per-query
and per-channel intermediate arrays are omitted from the public snapshot; the
aggregate files are sufficient to verify the reported condition counts,
relative gains, and descriptive bridge statistics.

## Data and anonymity

Dataset acquisition instructions are in `data/README.md`. No dataset or
credential is bundled. During double-blind review, use an anonymized export of
this repository and do not include author-identifying metadata or public URLs
in the submission supplementary.


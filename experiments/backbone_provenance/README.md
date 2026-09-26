# Frozen-backbone provenance notebooks

These notebooks document the forecasting backbones and generated direct-prediction / validation caches used by the final PRR downstream study. The current headline integration and trust calibration are reproduced in `../prr_long_horizon/04`--`06`; this directory is provenance for the frozen forecasting side.

Coverage includes:

- PatchTST
- iTransformer
- TimeMixer
- Seg-MoE
- DLinear

across ETTh1, Weather, Electricity, Traffic, Exchange, and Solar, with horizons 96, 192, 336, and 720. Notebook identifiers are retained because the generated cache/checkpoint paths use them. Some notebooks additionally contain diagnostic analyses from the development path; the paper-facing downstream comparison is always the 120-condition Direct/PRR protocol in `experiments/prr_long_horizon/`.

External repositories and dataset paths are configured in the first cells. Large checkpoints and pair caches are not included in the supplementary archive.

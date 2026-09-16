# Downstream notebook map

The notebooks retain their experiment identifiers to preserve provenance.
Only the final execution path is included.

- `15`--`19`: official PatchTST baselines and frozen-memory integration.
- `21`--`22`: iTransformer baseline and frozen-memory integration.
- `24`--`25`: TimeMixer baseline and frozen-memory integration.
- `27`--`28`: Solar and Exchange three-backbone expansions.
- `34A`--`34D`: Electricity full-321 chronological OOF experiments.
- `35A`--`35F`: Traffic full-862 chronological OOF experiments.
- `36A`--`36F`: Seg-MoE experiments on the six aligned datasets.
- `37`: four-backbone aggregate analysis.
- `39`--`40`: matched long-horizon relevance and utility bridge.
- `41`--`42`: significance and absolute-performance audits.
- `43B`--`48B`: DLinear experiments on the six aligned datasets.
- `49v4`--`50v2`: overlap-aware bootstrap and BH-FDR analyses.
- `51v2`: ETTm1 DLinear experiment across all horizons.

Saved outputs and development-only Markdown cells were removed. Execute code
cells in order after setting the data and external-repository roots in the
configuration cells.

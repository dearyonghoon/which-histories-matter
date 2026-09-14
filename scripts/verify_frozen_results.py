#!/usr/bin/env python3
"""Fast, dependency-light integrity checks for the frozen paper results."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "downstream"
REQUIRED = [
    RESULTS / "direct_forecaster_absolute_performance" / "direct_final_absolute_metrics_96_conditions.csv",
    RESULTS / "direct_forecaster_absolute_performance" / "paper_absolute_metrics_96_conditions.csv",
    RESULTS / "four_backbone_dataset_meta_analysis" / "condition_level_selected.csv",
    RESULTS / "full_long_horizon_relevance_downstream_bridge" / "full_24point_bridge.csv",
    RESULTS / "significance_metadata_recovery_v3_clean" / "paper_downstream_significance_96_conditions.csv",
]

def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        raise SystemExit("Missing required frozen results:\n  " + "\n  ".join(missing))
    for path in REQUIRED:
        data = rows(path)
        if not data:
            raise SystemExit(f"Empty CSV: {path}")
        print(f"PASS {path.relative_to(ROOT)} ({len(data)} rows)")
    abs_rows = rows(REQUIRED[0])
    sig_rows = rows(REQUIRED[4])
    if len(abs_rows) != 96:
        raise SystemExit(f"Expected 96 absolute conditions, found {len(abs_rows)}")
    if len(sig_rows) != 96:
        raise SystemExit(f"Expected 96 significance conditions, found {len(sig_rows)}")
    print("PASS frozen-result integrity checks")

if __name__ == "__main__":
    main()


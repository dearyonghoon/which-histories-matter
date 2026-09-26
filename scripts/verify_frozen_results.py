#!/usr/bin/env python3
"""Dependency-light integrity and headline checks for the current PRR paper results."""
from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"

FILES = {
    "retrieval": R / "main_retrieval_24.csv",
    "decomposition": R / "retrieval_24_conditions.csv",
    "manifest": R / "frozen_manifest_audit_48.csv",
    "fixed120": R / "fixed_trust_120_conditions.csv",
    "overall": R / "calibration_overall.csv",
    "dataset": R / "calibration_by_dataset.csv",
    "backbone": R / "calibration_by_backbone.csv",
    "horizon": R / "calibration_by_horizon.csv",
    "beta": R / "selected_beta_distribution.csv",
    "generalization": R / "calibration_generalization.csv",
    "aprr24": R / "anchored_prr_strong_base_24.csv",
    "aprr_overall": R / "anchored_prr_strong_base_overall.csv",
    "aprr_dataset": R / "anchored_prr_strong_base_by_dataset.csv",
    "craft_exact": R / "craft_matched_exact_24.csv",
    "craft_summary": R / "craft_matched_summary.csv",
    "craft_dataset": R / "craft_matched_dataset_summary.csv",
    "raft_audit": R / "raft_manifest_audit.csv",
    "raft_raw": R / "raft_matched_val_test_raw.csv",
    "raft_test": R / "raft_matched_test_with_valscale.csv",
    "raft_exact": R / "raft_matched_exact_24.csv",
    "raft_summary": R / "raft_matched_summary.csv",
    "raft_dataset": R / "raft_matched_dataset_summary.csv",
    "budget_test": R / "prr_budget100_test_24.csv",
    "budget_exact": R / "prr_budget100_exact_24.csv",
    "budget_summary": R / "prr_budget100_summary.csv",
    "table1": R / "table1_matched_retrieval_24.csv",
}

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def f(x): return float(x)
def i(x): return int(float(x))

def main():
    missing=[str(p.relative_to(ROOT)) for p in FILES.values() if not p.is_file()]
    if missing: raise SystemExit("Missing frozen result files:\n  " + "\n  ".join(missing))
    rows={k:read(p) for k,p in FILES.items()}
    expected={"retrieval":24,"decomposition":24,"manifest":48,"fixed120":120,"overall":2,"dataset":6,"backbone":5,"horizon":4,"beta":7,"generalization":1,"aprr24":24,"aprr_overall":3,"aprr_dataset":6,"craft_exact":24,"craft_summary":12,"craft_dataset":6,"raft_audit":48,"raft_raw":48,"raft_test":24,"raft_exact":24,"raft_summary":8,"raft_dataset":6,"budget_test":24,"budget_exact":24,"budget_summary":3,"table1":24}
    for k,n in expected.items():
        if len(rows[k]) != n: raise SystemExit(f"{k}: expected {n} rows, found {len(rows[k])}")
        print(f"PASS {FILES[k].relative_to(ROOT)} ({n} rows)")

    # Pearson -> PRR headline.
    gains=[f(r["prr_gain_vs_pearson_pct"]) for r in rows["retrieval"]]
    wins=sum(g>0 for g in gains); losses=sum(g<0 for g in gains)
    mean=sum(gains)/len(gains)
    if (wins,losses)!=(23,1): raise SystemExit(f"retrieval W/L mismatch: {wins}/{losses}")
    if abs(mean-26.6827)>0.05: raise SystemExit(f"retrieval mean gain mismatch: {mean:.4f}")
    print(f"PASS retrieval headline: {wins}/24 wins, mean gain {mean:.2f}%")

    # Common-stride decomposition: Pearson -> PRR-Stat -> PRR.
    stat_g=[f(r["prr_stat_gain_vs_pearson_pct"]) for r in rows["decomposition"]]
    full_g=[f(r["prr_gain_vs_prr_stat_pct"]) for r in rows["decomposition"]]
    sw=sum(g>0 for g in stat_g); sl=sum(g<0 for g in stat_g)
    fw2=sum(g>0 for g in full_g); fl2=sum(g<0 for g in full_g)
    smean=sum(stat_g)/len(stat_g); fullmean=sum(full_g)/len(full_g)
    if (sw,sl)!=(20,4): raise SystemExit(f"PRR-Stat W/L mismatch: {sw}/{sl}")
    if abs(smean-17.6656)>0.05: raise SystemExit(f"PRR-Stat mean gain mismatch: {smean:.4f}")
    if (fw2,fl2)!=(22,2): raise SystemExit(f"PRR-vs-PRR-Stat W/L mismatch: {fw2}/{fl2}")
    if abs(fullmean-11.4539)>0.05: raise SystemExit(f"PRR-vs-PRR-Stat mean mismatch: {fullmean:.4f}")
    if any(i(r.get("memory_stride",8)) != 8 for r in rows["retrieval"]+rows["decomposition"]):
        raise SystemExit("retrieval/decomposition stride mismatch: expected stride=8 everywhere")
    print(f"PASS stride-8 decomposition: PRR-Stat {sw}/24 wins, mean {smean:.2f}%; PRR vs PRR-Stat {fw2}/24 wins, mean {fullmean:.2f}%")

    # Fixed beta=.1 control from exact 120 rows.
    fixed_g=[f(r["prr_beta01_gain_vs_direct_pct"]) for r in rows["fixed120"]]
    fw=sum(g>1e-12 for g in fixed_g); fl=sum(g<-1e-12 for g in fixed_g); ft=120-fw-fl
    fmean=sum(fixed_g)/120
    if (fw,ft,fl)!=(79,0,41): raise SystemExit(f"fixed beta=.1 W/T/L mismatch: {fw}/{ft}/{fl}")
    if abs(fmean-.9711588624)>1e-5: raise SystemExit(f"fixed beta=.1 mean mismatch: {fmean}")
    print(f"PASS fixed-trust control: {fw}/{ft}/{fl}, mean gain {fmean:.6f}%")

    # Final condition-calibrated summary.
    cal=next(r for r in rows["overall"] if r["scheme"]=="Condition-Cal")
    tup=(i(cal["W"]),i(cal["T"]),i(cal["L"]))
    if tup!=(79,15,26): raise SystemExit(f"Condition-Cal W/T/L mismatch: {tup}")
    if i(cal["non_degraded"])!=94: raise SystemExit("Condition-Cal non-degraded mismatch")
    if abs(f(cal["mean_gain_pct"])-1.4066022019)>1e-6: raise SystemExit("Condition-Cal mean gain mismatch")
    print("PASS calibrated headline: 79/15/26, 94/120 non-degraded, +1.406602% mean MSE gain")

    # Trust distribution and validation/test audit.
    beta0=sum(i(r["conditions"]) for r in rows["beta"] if abs(f(r["beta"]))<1e-12)
    total=sum(i(r["conditions"]) for r in rows["beta"])
    if (beta0,total)!=(15,120): raise SystemExit(f"beta distribution mismatch: beta0={beta0}, total={total}")
    g=rows["generalization"][0]
    if i(g["same_improvement_sign"])!=94 or i(g["total_conditions"])!=120: raise SystemExit("calibration sign-audit mismatch")
    if abs(f(g["validation_test_gain_correlation"])-.7348759980)>1e-9: raise SystemExit("calibration correlation mismatch")
    print("PASS calibration audit: beta=0 in 15/120; validation/test gain r=0.734876; sign agreement 94/120")

    # Strong-base substitution ablation.
    aprr = rows["aprr_overall"]
    by_name = {r["comparison"]: r for r in aprr}
    checks = {
        "A-PRR vs Anchored L2": (6,0,18,1.633741,-2.385493),
        "A-PRR vs current PRR": (19,0,5,.839667,1.374056),
        "A-PRR vs Pearson": (24,0,0,27.512149,27.932393),
    }
    for name,(ew,et,el,em,emd) in checks.items():
        r=by_name[name]
        got=(i(r["W"]),i(r["T"]),i(r["L"]))
        if got!=(ew,et,el): raise SystemExit(f"{name} W/T/L mismatch: {got}")
        if abs(f(r["mean_gain_pct"])-em)>1e-5: raise SystemExit(f"{name} mean mismatch")
        if abs(f(r["median_gain_pct"])-emd)>1e-5: raise SystemExit(f"{name} median mismatch")
    union=sum(f(r["mean_union_size"]) for r in rows["aprr24"])/24
    learned=sum(f(r["mean_learned_only"]) for r in rows["aprr24"])/24
    top10=100*sum(f(r["mean_final_top10_learned_only_fraction"]) for r in rows["aprr24"])/24
    if abs(union-173.8)>0.1 or abs(learned-73.8)>0.1 or abs(top10-45.2)>0.1:
        raise SystemExit(f"A-PRR support summary mismatch: union={union:.3f}, learned={learned:.3f}, top10={top10:.3f}")
    print("PASS strong-base ablation: A-PRR vs PRR 19/0/5; vs anchored L2 6/0/18; learned-only Top-10 45.2%")

    # Matched CRAFT retrieval-rule diagnostic.
    cs = rows["craft_summary"]
    by_key = {(r["scope"], r["comparison"]): r for r in cs}
    checks = {
        ("CRAFT-paper overlap / 16", "CRAFT-Graph@10 vs Pearson"): (11,0,5,1.837460,1.333802),
        ("All six datasets / 24", "CRAFT-Graph@10 vs Pearson"): (16,0,8,2.510636,1.875227),
    }
    for key,(ew,et,el,em,emd) in checks.items():
        r=by_key[key]
        got=(i(r["W"]),i(r["T"]),i(r["L"]))
        if got!=(ew,et,el): raise SystemExit(f"CRAFT summary W/T/L mismatch for {key}: {got}")
        if abs(f(r["mean_gain_pct"])-em)>1e-5: raise SystemExit(f"CRAFT summary mean mismatch for {key}")
        if abs(f(r["median_gain_pct"])-emd)>1e-5: raise SystemExit(f"CRAFT summary median mismatch for {key}")

    exact=rows["craft_exact"]
    overlap=[r for r in exact if r["dataset"] in {"ETTh1","Weather","Electricity","Traffic"}]
    prr_vs_graph=[f(r["prr_gain_vs_craft_graph_pct"]) for r in overlap]
    if len(overlap)!=16 or sum(g>0 for g in prr_vs_graph)!=16:
        raise SystemExit("CRAFT-overlap PRR-vs-Graph W/L mismatch")
    if abs(sum(prr_vs_graph)/16 - 33.6810425685)>1e-5:
        raise SystemExit("CRAFT-overlap PRR-vs-Graph mean mismatch")
    all_prr_vs_graph=[f(r["prr_gain_vs_craft_graph_pct"]) for r in exact]
    if sum(g>0 for g in all_prr_vs_graph)!=18 or sum(g<0 for g in all_prr_vs_graph)!=6:
        raise SystemExit("all-24 PRR-vs-CRAFT-Graph W/L mismatch")
    if abs(sum(all_prr_vs_graph)/24 - 23.8417360790)>1e-5:
        raise SystemExit("all-24 PRR-vs-CRAFT-Graph mean mismatch")
    mean_same=sum(f(r["Graph_top10_same_channel_pct"]) for r in rows["craft_dataset"])/6
    if abs(mean_same-42.0595)>0.1:
        raise SystemExit(f"CRAFT graph same-channel fraction mismatch: {mean_same:.3f}%")
    print("PASS matched CRAFT diagnostic: Graph vs Pearson 11/16 on overlap; PRR vs Graph 16/16 (+33.68% mean)")

    # Matched RAFT retrieval-rule diagnostic.
    rs = rows["raft_summary"]
    by_name = {r["comparison"]: r for r in rs}
    raft_checks = {
        "RAFT-MS@10 vs Pearson": (13,0,11,7.570427,1.123346),
        "RAFT-ValScale@10 vs Pearson": (15,0,9,7.904704,1.607599),
    }
    for name,(ew,et,el,em,emd) in raft_checks.items():
        r=by_name[name]
        got=(i(r["W"]),i(r["T"]),i(r["L"]))
        if got!=(ew,et,el): raise SystemExit(f"{name} W/T/L mismatch: {got}")
        if abs(f(r["mean_gain_pct"])-em)>1e-5: raise SystemExit(f"{name} mean mismatch")
        if abs(f(r["median_gain_pct"])-emd)>1e-5: raise SystemExit(f"{name} median mismatch")

    rex=rows["raft_exact"]
    prr_ms=[f(r["prr_gain_vs_raft_ms_pct"]) for r in rex]
    prr_vs=[f(r["prr_gain_vs_raft_valscale_pct"]) for r in rex]
    if (sum(g>0 for g in prr_ms),sum(g<0 for g in prr_ms)) != (22,2):
        raise SystemExit("PRR-vs-RAFT-MS W/L mismatch")
    if (sum(g>0 for g in prr_vs),sum(g<0 for g in prr_vs)) != (22,2):
        raise SystemExit("PRR-vs-RAFT-ValScale W/L mismatch")
    if abs(sum(prr_ms)/24 - 20.5830314)>1e-5:
        raise SystemExit("PRR-vs-RAFT-MS mean mismatch")
    if abs(sum(prr_vs)/24 - 20.3438825)>1e-5:
        raise SystemExit("PRR-vs-RAFT-ValScale mean mismatch")

    losses=[(r["dataset"],i(r["horizon"])) for r in rex if f(r["prr_gain_vs_raft_valscale_pct"])<0]
    if losses != [("Exchange",192),("Exchange",336)]:
        raise SystemExit(f"RAFT-ValScale loss-condition mismatch: {losses}")

    selected={}
    for r in rows["raft_test"]:
        g=i(r["selected_g"])
        selected[g]=selected.get(g,0)+1
    if selected != {1:15,2:5,4:4}:
        raise SystemExit(f"RAFT validation-selected period counts mismatch: {selected}")

    print("PASS matched RAFT diagnostic: ValScale vs Pearson 15/24; PRR vs ValScale 22/24 (+20.34% mean)")

    # Candidate-budget-matched PRR inference control.
    bex=rows["budget_exact"]
    gb=[f(r["prr_budget100_gain_vs_pearson_pct"]) for r in bex]
    gs=[f(r["prr_budget100_gain_vs_prr_stat_pct"]) for r in bex]
    gf=[f(r["prr_budget100_gain_vs_full_prr_pct"]) for r in bex]
    if (sum(g>0 for g in gb),sum(g<0 for g in gb)) != (23,1):
        raise SystemExit("PRR-B100-vs-Pearson W/L mismatch")
    if abs(sum(gb)/24 - 26.555807)>1e-5:
        raise SystemExit("PRR-B100-vs-Pearson mean mismatch")
    if (sum(g>0 for g in gs),sum(g<0 for g in gs)) != (22,2):
        raise SystemExit("PRR-B100-vs-PRR-Stat W/L mismatch")
    if abs(sum(gs)/24 - 11.316035)>1e-5:
        raise SystemExit("PRR-B100-vs-PRR-Stat mean mismatch")
    if (sum(g>0 for g in gf),sum(g<0 for g in gf)) != (11,13):
        raise SystemExit("PRR-B100-vs-full-PRR W/L mismatch")
    if abs(sum(gf)/24 + 0.250808)>1e-5:
        raise SystemExit("PRR-B100-vs-full-PRR mean mismatch")
    mean_union=sum(f(r["mean_union_size"]) for r in rows["budget_test"])/24
    max_union=max(i(r["max_union_size"]) for r in rows["budget_test"])
    if abs(mean_union-94.931801)>1e-5 or max_union>100:
        raise SystemExit(f"PRR-B100 support mismatch: mean={mean_union:.6f}, max={max_union}")
    losses=[(r["dataset"],i(r["horizon"])) for r in bex if f(r["prr_budget100_gain_vs_pearson_pct"])<0]
    if losses != [("Exchange",336)]:
        raise SystemExit(f"PRR-B100 Pearson-loss condition mismatch: {losses}")
    print("PASS PRR-B100 control: vs Pearson 23/24 (+26.56% mean), vs PRR-Stat 22/24 (+11.32%), mean union 94.93 <= 100")
    print("PASS all current-paper frozen-result checks")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"

def rows(name):
    with (RES / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

def mean(values):
    values = list(values)
    return sum(values) / len(values)

def close(actual, expected, tol=5e-4):
    if not math.isclose(actual, expected, abs_tol=tol):
        raise AssertionError(f"{actual:.9f} != {expected:.9f} within {tol}")

c2 = rows("c2db_ablation.csv")
j3 = rows("jarvis3d_ablation.csv")
tmd = rows("tmd_shared_cv_summary.csv")
assert len(c2) == 20
assert len(j3) == 8
assert len(tmd) == 6
c2_nogap = mean(float(r["nogap_rmse_eV"]) for r in c2)
c2_gap = mean(float(r["constrained_rmse_eV"]) for r in c2)
j3_nogap = mean(float(r["nogap_rmse_eV"]) for r in j3)
j3_gap = mean(float(r["constrained_rmse_eV"]) for r in j3)
tmd_shared = mean(float(r["shared_rmse_eV"]) for r in tmd)
close(c2_nogap, 0.516132); close(c2_gap, 0.715786)
close(j3_nogap, 1.030699); close(j3_gap, 1.240447); close(tmd_shared, 0.715756)
print(f"2D systems: {len(c2)}")
print(f"3D systems: {len(j3)}")
print(f"TMD CV folds: {len(tmd)}")
print(f"2D mean RMSE, no gap: {c2_nogap:.6f} eV")
print(f"2D mean RMSE, gap constrained: {c2_gap:.6f} eV")
print(f"3D mean RMSE, no gap: {j3_nogap:.6f} eV")
print(f"3D mean RMSE, gap constrained: {j3_gap:.6f} eV")
print(f"TMD shared-parameter CV mean RMSE: {tmd_shared:.6f} eV")
print("Benchmark aggregate checks: OK")

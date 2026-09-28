from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "paper_benchmark" / "results"

def load(name):
    with (RES / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

def test_benchmark_tables_present_and_complete():
    c2 = load("c2db_ablation.csv")
    j3 = load("jarvis3d_ablation.csv")
    tmd = load("tmd_shared_cv_summary.csv")
    assert len(c2) == 20
    assert len(j3) == 8
    assert len(tmd) == 6

def test_published_mean_rmse_values():
    c2 = load("c2db_ablation.csv")
    j3 = load("jarvis3d_ablation.csv")
    mean = lambda rows, key: sum(float(r[key]) for r in rows) / len(rows)
    assert abs(mean(c2, "nogap_rmse_eV") - 0.516132) < 5e-4
    assert abs(mean(c2, "constrained_rmse_eV") - 0.715786) < 5e-4
    assert abs(mean(j3, "nogap_rmse_eV") - 1.030699) < 5e-4
    assert abs(mean(j3, "constrained_rmse_eV") - 1.240447) < 5e-4

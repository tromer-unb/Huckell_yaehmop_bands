from pathlib import Path
import json, os, subprocess, sys
import pytest

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.skipif(os.environ.get("RUN_SLOW_FIT") != "1", reason="set RUN_SLOW_FIT=1 to run optimizer regression")
def test_frontier_fit_regression(tmp_path):
    f = ROOT / "parameter_fitter"
    cmd = [sys.executable, str(f / "fit_eht_v2.py"), str(f / "examples/mos2/structure.cif"), str(f / "examples/mos2/band.png"),
           "--format", "image", "--emin", "-15", "--emax", "11", "--fit-window", "-2", "2",
           "--symmetry-points", "0", "0", "0.5", "0", "0.3333333333333333", "0.3333333333333333", "0", "0",
           "--point-dim", "2", "--labels", "G", "M", "K", "G", "--points-per-line", "30", "--trace-nx", "401",
           "--outdir", str(tmp_path), "--tag", "regression"]
    subprocess.run(cmd, text=True, capture_output=True, check=True)
    data = json.loads((tmp_path / "regression.json").read_text())
    assert data["fit_window_active"] is True
    assert data["fit_window_eV"] == [-2.0, 2.0]
    assert data["fit_points"] > 0
    assert data["best_seen"]["fit_rmse"] < 0.30
    assert abs(data["best_seen"]["gap_error_eV"]) < 0.01

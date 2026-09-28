from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]


def test_band_runner_smoke(tmp_path):
    script = ROOT / "band_runner/huckel_yaehmop.py"
    cif = ROOT / "band_runner/examples/mos2/structure.cif"
    param = ROOT / "band_runner/examples/mos2/param.txt"
    out = tmp_path / "bands.csv"
    plot = tmp_path / "bands.png"
    cmd = [sys.executable, str(script), str(cif), "--param", str(param),
           "--symmetry-points", "0", "0", "0.5", "0", "0.3333333333333333", "0.3333333333333333", "0", "0",
           "--point-dim", "2", "--labels", "G", "M", "K", "G", "--points-per-line", "4",
           "--output", str(out), "--plot", str(plot), "--work-prefix", str(tmp_path / "work/run")]
    p = subprocess.run(cmd, text=True, capture_output=True, check=True)
    assert out.is_file() and out.stat().st_size > 100
    assert plot.is_file() and plot.stat().st_size > 100
    assert "indirect_gap=" in p.stdout

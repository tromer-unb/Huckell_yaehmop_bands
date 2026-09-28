#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cp -f "$ROOT/.venv/bin/python" /dev/null 2>/dev/null || { echo "Run ./setup.sh first." >&2; exit 1; }
# Reuse the root virtual environment from component scripts.
ln -sfn "$ROOT/.venv" "$ROOT/band_runner/.venv"
ln -sfn "$ROOT/.venv" "$ROOT/parameter_fitter/.venv"
"$ROOT/parameter_fitter/run_example_frontier.sh"
cp "$ROOT/parameter_fitter/results_frontier/param_mos2_frontier.txt" "$ROOT/band_runner/examples/mos2/param_from_fit.txt"
"$ROOT/.venv/bin/python" "$ROOT/band_runner/huckel_yaehmop.py" "$ROOT/band_runner/examples/mos2/structure.cif" \
  --param "$ROOT/band_runner/examples/mos2/param_from_fit.txt" \
  --symmetry-points 0 0 0.5 0 0.3333333333333333 0.3333333333333333 0 0 \
  --point-dim 2 --labels G M K G --points-per-line 100 \
  --output "$ROOT/band_runner/results/mos2_from_fit.csv" \
  --plot "$ROOT/band_runner/results/mos2_from_fit.png"
echo "End-to-end MoS2 demo complete."

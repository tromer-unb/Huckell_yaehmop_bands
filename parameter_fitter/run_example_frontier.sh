#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || { echo "Run ./setup.sh first." >&2; exit 1; }
cd "$ROOT"
"$PY" fit_eht_v2.py examples/mos2/structure.cif examples/mos2/band.png \
  --format image --emin -15 --emax 11 --fit-window -2 2 \
  --symmetry-points 0 0 0.5 0 0.3333333333333333 0.3333333333333333 0 0 \
  --point-dim 2 --labels G M K G --points-per-line 30 --trace-nx 401 \
  --outdir results_frontier --tag mos2_frontier

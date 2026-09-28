#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || { echo "Run ./setup.sh first." >&2; exit 1; }
cd "$ROOT"
"$PY" huckel_yaehmop.py examples/mos2/structure.cif \
  --param examples/mos2/param.txt \
  --symmetry-points 0 0 0.5 0 0.3333333333333333 0.3333333333333333 0 0 \
  --point-dim 2 --labels G M K G --points-per-line 100 \
  --output results/mos2_bands.csv --plot results/mos2_bands.png

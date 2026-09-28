#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 -m venv .venv
PY="$ROOT/.venv/bin/python"
"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements-dev.txt
"$ROOT/scripts/install_yaehmop.sh" "$ROOT/band_runner/yaehmop"
"$ROOT/scripts/install_yaehmop.sh" "$ROOT/parameter_fitter/yaehmop"
"$PY" -c "import numpy, scipy, ase, PIL, matplotlib; print('Python dependencies: OK')"
echo "Setup complete. Try: ./scripts/run_mos2_demo.sh"

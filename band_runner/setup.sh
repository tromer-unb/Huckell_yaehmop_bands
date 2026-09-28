#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
PY="$ROOT/.venv/bin/python"
"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt
if [[ -x "$REPO_ROOT/scripts/install_yaehmop.sh" ]]; then
  "$REPO_ROOT/scripts/install_yaehmop.sh" "$ROOT/yaehmop"
else
  echo "ERROR: run this setup script from a full repository checkout." >&2
  exit 1
fi
echo "Setup complete."

#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:?usage: install_yaehmop.sh TARGET_DIRECTORY}"
COMMIT="4ded45bb2bb7a2d38d2527c991debce9226a9066"
REPO="https://github.com/greglandrum/yaehmop.git"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

command -v git >/dev/null || { echo "ERROR: git is required." >&2; exit 1; }
command -v make >/dev/null || { echo "ERROR: make is required." >&2; exit 1; }
command -v cc >/dev/null || { echo "ERROR: a C compiler (gcc/clang) is required." >&2; exit 1; }

if [[ -x "$TARGET/bind" && -f "$TARGET/eht_parms.dat" ]] && "$TARGET/bind" -v >/dev/null 2>&1; then
  echo "YAeHMOP is already installed in $TARGET"
  exit 0
fi

CACHE="$ROOT/.cache/yaehmop-$COMMIT"
if [[ ! -d "$CACHE/.git" ]]; then
  mkdir -p "$ROOT/.cache"
  git clone "$REPO" "$CACHE"
fi

git -C "$CACHE" fetch --quiet origin || true
git -C "$CACHE" checkout --quiet "$COMMIT"
if [[ ! -x "$CACHE/tightbind/bind" ]]; then
  make -C "$CACHE/tightbind"
else
  echo "Reusing cached YAeHMOP build at $CACHE/tightbind/bind"
fi
cp "$CACHE/tightbind/bind" "$TARGET/bind"
cp "$CACHE/tightbind/eht_parms.dat" "$TARGET/eht_parms.dat"
chmod +x "$TARGET/bind"
"$TARGET/bind" -v
printf '%s\n' "$COMMIT" > "$TARGET/UPSTREAM_COMMIT"
cp "$CACHE/license.txt" "$TARGET/LICENSE.txt"
echo "Installed YAeHMOP commit $COMMIT in $TARGET"

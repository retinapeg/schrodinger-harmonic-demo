#!/usr/bin/env bash
# Render demo screenshots into docs/ with headless Chrome (macOS path by default).
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PROFILE="$(mktemp -d)"
shot() { # name query width height
  rm -f "docs/$1.png"
  "$CHROME" --headless --disable-gpu --no-first-run --user-data-dir="$PROFILE" --hide-scrollbars \
    --window-size="$3,$4" --virtual-time-budget=6000 --screenshot="docs/$1.png" \
    "file://$PWD/demo/index.html?$2" >/dev/null 2>&1 &
  local pid=$!
  for _ in $(seq 1 30); do [ -s "docs/$1.png" ] && break; sleep 1; done
  sleep 1; kill "$pid" 2>/dev/null || true
  echo "docs/$1.png"
}
shot demo-light "theme=light&n=4" 1400 1520
shot demo-dark "theme=dark&n=3" 1400 1060
shot demo-probability "theme=light&view=prob&show=10&n=6&omega=1" 1400 1060

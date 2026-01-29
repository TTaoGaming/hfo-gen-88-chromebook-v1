#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[cdp-doctor] cwd=$PWD"

echo "[cdp-doctor] checking local listener :9222 (container)"
if ss -ltn 2>/dev/null | grep -q ':9222'; then
  echo "[cdp-doctor] OK: something is listening on :9222"
else
  echo "[cdp-doctor] NO: nothing is listening on :9222"
fi

echo "[cdp-doctor] probing CDP endpoints"
probe() {
  local label="$1"; shift
  local url="$1"; shift
  if curl -fsS "$url/json/version" >/dev/null 2>&1; then
    echo "[cdp-doctor] OK: $label -> $url"
    curl -fsS "$url/json/version" | head -c 240 || true
    echo
  else
    echo "[cdp-doctor] NO: $label -> $url"
  fi
}

probe "localhost" "http://localhost:9222"
probe "127.0.0.1" "http://127.0.0.1:9222"

GW=$(ip route 2>/dev/null | awk '/default/ {print $3; exit}' || true)
if [[ -n "${GW:-}" ]]; then
  probe "default-gateway" "http://${GW}:9222"
else
  echo "[cdp-doctor] no default gateway found"
fi

echo "[cdp-doctor] chrome/chromium executables"
command -v google-chrome-stable || true
command -v google-chrome || true
command -v chromium || true
command -v chromium-browser || true

if command -v dpkg >/dev/null 2>&1; then
  echo "[cdp-doctor] dpkg chrome/chromium packages (if any)"
  dpkg -l | grep -E 'google-chrome|chromium' || true
fi

echo "[cdp-doctor] guidance"
cat <<'TXT'
- Playwright can use 'host Chrome' ONLY if a CDP endpoint is reachable from this container.
- If you previously 'used host Chrome without websockets', Playwright was still using CDP; it just auto-managed the websocket.

Next steps (pick one):
1) If you can start Chrome on the HOST with CDP exposed to penguin:
   - Ensure http://<reachable-ip>:9222/json/version works from penguin.
   - Then run the VS Code task: "Gen7 v1: Smoke via Host Chrome CDP (no downloads)".

2) If you just need a working browser WITHOUT Playwright downloads:
   - Install chromium inside penguin via apt, then set CHROME_PATH to it.
TXT

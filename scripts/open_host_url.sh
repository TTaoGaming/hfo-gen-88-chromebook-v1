#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
set -euo pipefail

url="${1:-}"
if [[ -z "$url" ]]; then
  echo "usage: $0 <url>" >&2
  exit 2
fi

if command -v garcon-url-handler >/dev/null 2>&1; then
  # ChromeOS/Crostini: opens the URL in the host (ChromeOS) browser.
  exec garcon-url-handler "$url"
fi

if command -v xdg-open >/dev/null 2>&1; then
  exec xdg-open "$url"
fi

echo "No opener found (garcon-url-handler or xdg-open). URL: $url" >&2
exit 1

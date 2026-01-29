#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Stop Shodh backend server (Docker container) to reduce background CPU.

# Keep consistent with scripts/shodh_memory_server.sh
name="${SHODH_DOCKER_NAME:-hfo-shodh-memory}"

if ! command -v docker >/dev/null 2>&1; then
  echo "[shodh] docker not found; nothing to stop" >&2
  exit 0
fi

if docker ps --format '{{.Names}}' | grep -qx "$name"; then
  echo "[shodh] Stopping Docker container: $name"
  docker stop "$name" >/dev/null
  echo "[shodh] Stopped."
else
  echo "[shodh] Container not running: $name"
fi

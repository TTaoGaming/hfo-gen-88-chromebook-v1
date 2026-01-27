#!/usr/bin/env bash
set -euo pipefail

# Starts a local shodh-memory server (downloads latest Linux x64 release if missing).
# Data is stored under artifacts/shodh_memory/.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

bin_dir="$repo_root/artifacts/shodh_memory/bin"
data_dir="$repo_root/artifacts/shodh_memory/data"
mkdir -p "$bin_dir" "$data_dir"

shodh_server_bin="$bin_dir/shodh-memory-server"

if [[ ! -x "$shodh_server_bin" ]]; then
  echo "[shodh] Downloading latest shodh-memory Linux x64 release..." >&2
  tmp_dir="$(mktemp -d)"
  trap 'rm -rf "$tmp_dir"' EXIT

  curl -fsSL "https://github.com/varun29ankuS/shodh-memory/releases/latest/download/shodh-memory-linux-x64.tar.gz" \
    | tar -xz -C "$tmp_dir"

  # The archive includes multiple siblings (server binary, wrapper, TUI, ONNX runtime .so).
  # We install the full payload into artifacts/shodh_memory/bin so relative lookups work.
  cp -f "$tmp_dir"/* "$bin_dir/"
  chmod +x "$bin_dir/shodh-memory" "$bin_dir/shodh-memory-server" "$bin_dir/shodh-tui" || true
fi

# Load repo .env if present
if [[ -f "$repo_root/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$repo_root/.env"
  set +a
fi

export SHODH_HOST="${SHODH_HOST:-127.0.0.1}"
export SHODH_PORT="${SHODH_PORT:-3030}"
export SHODH_MEMORY_PATH="${SHODH_MEMORY_PATH:-$data_dir}"
run_mode="${HFO_SHODH_RUN_MODE:-docker}"

if [[ "$run_mode" == "docker" ]]; then
  if ! command -v docker >/dev/null 2>&1; then
    echo "[shodh] ERROR: docker not found; set HFO_SHODH_RUN_MODE=native to try native binary" >&2
    exit 2
  fi

  container_name="${SHODH_DOCKER_NAME:-hfo-shodh-memory}"
  image="${SHODH_DOCKER_IMAGE:-roshera/shodh-memory}"
  host_port="${SHODH_PORT}"

  # Ensure data directory exists for bind mount
  mkdir -p "$data_dir"

  if docker ps --format '{{.Names}}' | grep -qx "$container_name"; then
    echo "[shodh] Docker container already running: $container_name" >&2
    exit 0
  fi

  if docker ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
    echo "[shodh] Starting existing Docker container: $container_name" >&2
    docker start "$container_name" >/dev/null
  else
    # The README references a Docker Hub image which may not always exist.
    # If pull fails, build a local image from source.
    if ! docker image inspect "$image" >/dev/null 2>&1; then
      echo "[shodh] Pulling image: $image" >&2
      if ! docker pull "$image" >/dev/null 2>&1; then
        image="${SHODH_DOCKER_IMAGE_FALLBACK:-hfo-shodh-memory:local}"
        echo "[shodh] Image not found; building local image: $image" >&2
        src_dir="$repo_root/artifacts/shodh_memory/shodh_src"
        if [[ ! -d "$src_dir/.git" ]]; then
          echo "[shodh] Cloning source into $src_dir" >&2
          rm -rf "$src_dir"
          git clone --depth 1 https://github.com/varun29ankuS/shodh-memory.git "$src_dir" >/dev/null
        fi

        dockerfile_path="$repo_root/scripts/docker/shodh_memory.Dockerfile"
        docker build -t "$image" -f "$dockerfile_path" "$src_dir" >/dev/null
      fi
    fi

    echo "[shodh] Starting Docker container: $container_name ($image)" >&2
    docker run -d \
      --name "$container_name" \
      -p "${host_port}:3030" \
      -e SHODH_HOST=0.0.0.0 \
      -e SHODH_PORT=3030 \
      -e "SHODH_MEMORY_PATH=/data" \
      -e "SHODH_DEV_API_KEY=${SHODH_DEV_API_KEY:-}" \
      -e "SHODH_API_KEYS=${SHODH_API_KEYS:-}" \
      -v "$data_dir:/data" \
      "$image" >/dev/null
  fi

  echo "[shodh] Server should be reachable at http://127.0.0.1:${host_port}/health" >&2
  exit 0
fi

# If SHODH_API_KEY is set, ensure server accepts it in dev mode.
if [[ -n "${SHODH_API_KEY:-}" ]] && [[ -z "${SHODH_DEV_API_KEY:-}" ]] && [[ -z "${SHODH_API_KEYS:-}" ]]; then
  export SHODH_DEV_API_KEY="$SHODH_API_KEY"
fi

echo "[shodh] Starting server on http://${SHODH_HOST}:${SHODH_PORT}" >&2
export LD_LIBRARY_PATH="$bin_dir:${LD_LIBRARY_PATH:-}"
exec "$shodh_server_bin"

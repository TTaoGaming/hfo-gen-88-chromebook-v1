#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
# Minimal clone helper for Gen6 HTML artifacts.
#
# This is intentionally conservative: it copies the file and (optionally) performs a safe string replace.

set -euo pipefail

SRC="${1:-}"
DST="${2:-}"
REPLACE_FROM="${3:-}"
REPLACE_TO="${4:-}"

if [[ -z "${SRC}" || -z "${DST}" ]]; then
  echo "Usage: $0 <src.html> <dst.html> [replace_from] [replace_to]" >&2
  exit 2
fi

if [[ ! -f "${SRC}" ]]; then
  echo "Source does not exist: ${SRC}" >&2
  exit 2
fi

if [[ -e "${DST}" ]]; then
  echo "Destination already exists (refusing to overwrite): ${DST}" >&2
  exit 2
fi

mkdir -p "$(dirname "${DST}")"
cp "${SRC}" "${DST}"

if [[ -n "${REPLACE_FROM}" && -n "${REPLACE_TO}" ]]; then
  # GNU sed in-place edit
  sed -i "s/${REPLACE_FROM}/${REPLACE_TO}/g" "${DST}"
fi

echo "Cloned: ${SRC} -> ${DST}"

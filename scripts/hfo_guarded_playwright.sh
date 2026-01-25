#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
# Guarded Playwright runner: trims background load before/after tests.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1) Reduce background noise to avoid VS Code crash loops.
bash "${ROOT}/scripts/hfo_resource_governor.sh" pretest

# 2) Ensure omega server for Gen6 artifacts.
bash "${ROOT}/scripts/hfo_omega_server_ctl.sh" ensure

# 3) Run Playwright with provided args.
set +e
npx playwright test "$@"
CODE=$?
set -e

# 4) Cleanup browsers and summarize.
bash "${ROOT}/scripts/hfo_resource_governor.sh" posttest

exit ${CODE}

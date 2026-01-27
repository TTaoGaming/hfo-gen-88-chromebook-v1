# Gen88 Chromebook v1 — Forensic Analysis (2026-01-26)

Goal: stabilize the machine and VS Code by identifying (a) runaway always-on agent processes, (b) oversized ledgers/archives that crash editors when tailed/indexed, and (c) swap/disk constraints.

> Scope: read-only probes + recommendations. No destructive actions performed by this report.

## Executive summary

- **Swap is currently not active** (and `swapon` is not even installed in this Linux container), so memory pressure cannot spill to swap.
- **Always-on background workloads exist**: `ollama serve`, multiple `npm exec … mcp-*` servers, a Playwright test server, plus VS Code language servers.
- **Workspace contains extremely large “ledger-like” files** that will crash VS Code (or any tail/index) if opened or scanned aggressively:
  - `hfo_unified_v88_merged.duckdb` (~7.6GB)
  - `mcp_memory.jsonl` (~427MB)
  - dozens of `hot_obsidian_blackboard.jsonl` anchors (~47MB each)
- **Project directory hot spots**:
  - `hfo_hot_obsidian` (~51GB)
  - `.git/objects` (~17GB)
- Disk overall: root filesystem is **~84% used**, and some system mounts (ChromeOS fonts) are **100% full**.

## Proof (raw command output)

### System snapshot (CPU/RAM/disk)

Command:

```bash
uname -a && date && uptime && free -h && df -hT
```

Output:

```text
Linux penguin 6.6.99-08879-gd6e365e8de4e #1 SMP PREEMPT_DYNAMIC Thu, 23 Oct 2025 06:15:52 -0700 x86_64 GNU/Linux
Mon Jan 26 09:55:28 AM MST 2026
09:55:28 up 3 min,  0 user,  load average: 0.91, 1.18, 0.54

               total        used        free      shared  buff/cache   available
Mem:           6.3Gi       2.0Gi       3.5Gi        96Mi       901Mi       4.3Gi
Swap:             0B          0B          0B

Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/vdc       btrfs     262G  216G   43G  84% /
/dev/vdb       ext4       75M   73M     0 100% /opt/google/cros-containers
fonts          virtiofs  3.9G  3.9G   15M 100% /usr/share/fonts/chromeos
...
```

### Swap status

Command:

```bash
echo '## swap status' && swapon --show || true && echo '---' && cat /proc/swaps && echo '---' && grep -nE 'swap|swapfile' /etc/fstab || true
```

Output:

```text
## swap status
bash: swapon: command not found
---
Filename                Type            Size    Used    Priority
---
```

Interpretation:
- `/proc/swaps` shows **no active swap devices**.
- The command `swapon` is missing, which strongly suggests this environment doesn’t have `util-linux` tools available or they’re not in PATH.
- You recently removed `/swapfile` lines from `/etc/fstab` (from your terminal history), so swap persistence would also be disabled even if tools existed.

### Listening ports (services that may be “always on”)

Command:

```bash
ss -lptun | head -n 80
```

Output:

```text
tcp   LISTEN 0   511  127.0.0.1:4337    0.0.0.0:* users:(("code",pid=2709,fd=39))
tcp   LISTEN 0   511  127.0.0.1:34403   0.0.0.0:* users:(("code",pid=1873,fd=85))
tcp   LISTEN 0  4096  127.0.0.1:11434   0.0.0.0:*
...
```

Interpretation:
- `127.0.0.1:11434` is consistent with **Ollama** default.
- Multiple `code` processes are listening locally.

### “Always-on” suspect processes (agents + VS Code helpers)

Command:

```bash
ps aux | egrep -i 'ollama|playwright|mcp|node .*mcp|code --|pylance|python .*mcp|duckdb' | head -n 200
```

Output (excerpt):

```text
ollama     141  ... /usr/local/bin/ollama serve
...
/usr/bin/node hfo_gen_88_chromebook_v_1/node_modules/@playwright/test/cli.js test-server -c hfo_gen_88_chromebook_v_1/playwright.config.ts
npm exec @modelcontextprotocol/server-memory
npm exec @upstash/context7-mcp
npm exec tavily-mcp@0.2.3
node .../mcp-server-sequential-thinking
node .../mcp-server-memory
...
/usr/share/code/code ... ms-python.vscode-pylance .../server.bundle.js
```

Interpretation:
- You have multiple MCP servers started via `npm exec ...` that will remain running unless explicitly shut down.
- Playwright `test-server` is running (often unnecessary unless actively testing).
- `ollama serve` is running (can consume CPU/RAM + keeps a local port open).

### Running user services

Command:

```bash
systemctl --user list-units --type=service --state=running --no-pager | head -n 200
```

Output:

```text
at-spi-dbus-bus.service           loaded active running Accessibility services bus
cros-garcon.service               loaded active running Chromium OS Garcon Bridge
cros-vmstat-metrics.service       loaded active running Chromium OS /proc/vmstat Metrics Collection Daemon
...
pipewire.service                  loaded active running PipeWire Multimedia Service
wireplumber.service               loaded active running Multimedia Service Session Manager
```

Interpretation:
- These are mostly baseline Crostini/user services. The “agent” load is primarily from userland processes (`npm exec`, `ollama`, Playwright, VS Code helpers), not systemd user services.

### VS Code footprint

Command:

```bash
code --version | head -n 3
ls -1 /home/tommytai3/.vscode/extensions | wc -l
```

Output:

```text
1.108.1
585eba7c0c34fd6b30faac7c62a42050bfbc0086
x64
---
41
```

Interpretation:
- VS Code has **41 extensions installed**. On a 6.3GiB RAM environment, extension overhead can become crashy, especially if extensions spawn background servers.

## Workspace risk factors (proof)

### Biggest files in the repo

Command:

```bash
find hfo_gen_88_chromebook_v_1 -type f -printf '%s\t%p\n' | sort -nr | head -n 40
```

Output (top entries):

```text
7593799680	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
946436569	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/persist/6_persist/wikipedia_simple.zim
946436569	hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/4_archive/persist/6_persist/wikipedia_simple.zim
823851719	hfo_gen_88_chromebook_v_1/.git/objects/pack/pack-7c439325ce0d507677dba07976332f1a736476a1.pack
427173411	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
...
```

### Biggest directories in the repo

Command:

```bash
du -x -h --max-depth=2 hfo_gen_88_chromebook_v_1 | sort -h | tail -n 40
```

Output (top entries):

```text
17G	hfo_gen_88_chromebook_v_1/.git/objects
30G	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive
47G	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze
51G	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian
```

### Ledger-like files by size

Command:

```bash
find hfo_gen_88_chromebook_v_1 -type f \( -iname '*.jsonl' -o -iname '*.duckdb' -o -iname '*.md' -o -iname '*.log' \) -printf '%s\t%p\n' | sort -nr | head -n 60
```

Output (top entries):

```text
7593799680	hfo_gen_88_chromebook_v_1/.../hfo_unified_v88_merged.duckdb
427173411	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
47482962	hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/.../hot_obsidian_blackboard.jsonl
... many ~47MB anchor jsonl files ...
```

## Likely crash triggers (ranked)

1. **VS Code indexing / file watcher overload** from `hfo_hot_obsidian/**` (~51GB) and huge `.jsonl` / `.duckdb` / `.zim` files.
2. **Always-on Node/MCP servers + Playwright test-server** keeping CPU active and leaking memory over time.
3. **No swap fallback** + constrained container environment ⇒ transient spikes crash apps instead of swapping.
4. **Disk full mounts** (`/usr/share/fonts/chromeos` 100%, `/opt/google/cros-containers` 100%) can cause weird failures and crashes when software tries to write caches.

## Quarantine recommendations (safe, reversible)

### A) Stop the always-on agent processes (immediate relief)

These are your current always-on style processes from the proof above:
- `ollama serve`
- `npm exec @modelcontextprotocol/server-memory`
- `npm exec @upstash/context7-mcp`
- `npm exec tavily-mcp@0.2.3`
- Playwright `test-server`

Recommended approach:
1. Close VS Code completely.
2. In a terminal, stop the known offenders *for this session*:

```bash
pkill -f 'ollama serve' || true
pkill -f 'mcp-server-' || true
pkill -f 'npm exec .*mcp' || true
pkill -f 'playwright.*test-server' || true
```

If you want, I can generate a tiny `scripts/stop_background_agents.sh` that prints what it will kill first (dry-run) and then stops them.

### B) Prevent VS Code from scanning the giant ledgers

Add workspace settings to exclude the heavy directories:

- Exclude `hfo_hot_obsidian/**`, `hfo_cold_obsidian/**`, and `**/*.jsonl`, `**/*.duckdb`, `**/*.zim` from watcher + search.

This is the single most effective fix for “tail/open crashes” inside the editor.

### C) Swap: what you can prove right now, and what to do next

What we proved:
- No active swap (`/proc/swaps` empty).
- `swapon` command missing.

Next steps options:
- If this is Debian/Ubuntu-like inside Crostini and you *can* install packages: install `util-linux` tools so `swapon` exists.
- Consider **zram** (often best on Chromebooks) rather than a swapfile on slow storage.

### D) Disk pressure

We observed system mounts at 100% (`/usr/share/fonts/chromeos`, `/opt/google/cros-containers`). Even if your root has 43G free, those mounts being full can still cause crashes.

Recommended: identify what can be removed from those mounts (often not much user-control). If you want, I can probe what’s consuming space there using read-only `du` and propose safe deletions.

## Next actions I can do for you (pick 1)

1. Create a workspace `.vscode/settings.json` to exclude the huge dirs/files (safe, reversible).
2. Create a `stop_background_agents.sh` + a `status_agents.sh` that prints proof before/after.
3. Add a “quarantine” folder + move/zip old `stigmergy_anchors` to reduce file watcher churn (requires your explicit approval; this is destructive).

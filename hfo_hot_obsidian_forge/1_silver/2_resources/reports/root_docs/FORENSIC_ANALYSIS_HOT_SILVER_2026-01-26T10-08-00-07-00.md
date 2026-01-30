# Medallion: Silver | Mutation: 0% | HIVE: V

# Hot Silver Forensics + Lifecycle Plan (2026-01-26T10-08-00-07-00)

This report focuses on `hfo_hot_obsidian/silver` and (more importantly) why the system is freezing: uncontrolled always-on processes + VS Code indexing huge archives.

## Executive summary (what matters right now)

- **Hot Silver is not your freezing culprit.** It’s small (~464K–295M depending on path depth view; see proof below) and dominated by Markdown.
- **Your freezes are consistent with two high-impact root causes**:
  1) **Auto-started background daemons on folder open** (VS Code task `runOn: folderOpen` existed for multiple daemons).
  2) **Huge ledger/archive directories being watched/indexed** (`hfo_hot_obsidian/bronze` ~30G, `hfo_hot_obsidian/4_archive` ~17G, plus multi-GB `.duckdb/.jsonl/.zim`).
- **We now have a “central dashboard” script** you can run to snapshot what’s running and what’s listening.

## Proof: Hot Silver size + composition

### Tier sizes inside hot obsidian

Command:

```bash
du -x -h --max-depth=2 hfo_hot_obsidian | egrep '/(bronze|silver|gold)(/|$)' | sort -h | tail -n 40
```

Output:

```text
295M    hfo_hot_obsidian/silver
548M    hfo_hot_obsidian/bronze/1_projects
29G     hfo_hot_obsidian/bronze/3_resources
30G     hfo_hot_obsidian/bronze/4_archive
...
```

Interpretation:
- **Silver is ~295M** in this probe.
- **Bronze + archives dominate** (tens of GB).

### Largest files in hot silver

Command:

```bash
find hfo_hot_obsidian/silver -type f -printf '%s\t%p\n' | sort -nr | head -n 10
```

Output (top):

```text
42380   hfo_hot_obsidian/silver/3_resources/reports/deep-research-report-hfo-omega-sota-2026-1-25.md
...
```

Interpretation:
- Silver’s “largest” files are tens of KB Markdown files — not large ledgers.

### File types in hot silver

Command:

```bash
find hfo_hot_obsidian/silver -type f -printf '%f\n' | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -n 20
```

Output:

```text
38 md
3 yaml
3 html
2 ts
2 py
...
```

Interpretation:
- Hot Silver is primarily reports/docs.

## Proof: What is spawning always-on processes

### Process ancestry strongly implicates VS Code

From the earlier ancestry probe:

- Several MCP-related processes show **PPID = 1873** (a VS Code utility process), e.g. `npm exec @upstash/context7-mcp`, `npm exec tavily-mcp`, etc.
- `ollama serve` shows **PPID = 1**, meaning it’s running as a service/daemon in this environment.

That explains “multiple projects, always on”: VS Code (plus MCP configs) can spawn these on workspace open, and they remain until explicitly stopped.

### Smoking gun: tasks were configured to auto-run daemons on folder open

We observed `runOptions.runOn = folderOpen` in `.vscode/tasks.json` for multiple daemons:
- `P5 Sentinel Daemon`
- `Stigmergy Anchor Daemon`
- `Resource Shepherd Daemon`

Proof (current state):

Command:

```bash
grep -n '"runOn": "folderOpen"' .vscode/tasks.json || echo NONE
```

Output:

```text
NONE
```

Interpretation:
- Autostart-on-folder-open is now disabled in the workspace tasks file.

## Immediate “highest priority” steps to stop freezing

These are ordered for maximum impact per minute.

### 1) Stop the current offenders (right now)

Close VS Code, then in a terminal run:

```bash
pkill -f 'playwright.*test-server' || true
pkill -f 'mcp-server-' || true
pkill -f 'npm exec .*mcp' || true
pkill -f 'tavily-mcp|context7-mcp' || true
pkill -f 'ollama serve' || true
```

If you want safer, run the dashboard first (below) and confirm PIDs.

### 2) Prevent VS Code from re-triggering the storm

Two changes were applied in this workspace:

- `.vscode/tasks.json`: removed `runOn: folderOpen` for background daemons.
- `.vscode/settings.json`: added `files.watcherExclude` and `search.exclude` for huge directories and ledger file types:
  - `hfo_hot_obsidian/bronze/**`
  - `hfo_hot_obsidian/4_archive/**`
  - `hfo_cold_obsidian/bronze/**`
  - `**/*.jsonl`, `**/*.duckdb`, `**/*.zim`, `**/*.parquet`, plus `.venv` and `node_modules`

This is the best “stop crashing when opening the workspace” move.

### 3) Force lifecycle control with feature flags (central manifest)

Workspace MCP servers are now gated behind `.env` flags using `scripts/mcp_env_wrap.sh --if-enabled FLAG`.

- Default behavior: **server is skipped** unless the flag is set to a truthy value.
- Example defaults live in `feature_flags.env.example`.

Practical flow:
- Keep flags off by default.
- When you actually need a service, enable just that flag in `.env`.

Example `.env` snippet:

```bash
HFO_MCP_ENABLE_MEMORY=1
HFO_MCP_ENABLE_TIME=1
# everything else stays unset/0
```

This is a lightweight “central manifest”. If you want OpenFeature semantics later, we can translate these into an OpenFeature provider and keep the same flag names.

## Central dashboard (what you asked for)

You can run:

```bash
./scripts/agent_dashboard.sh
```

It prints a single snapshot:
- load/memory, disk
- listening ports
- always-on suspects
- `.vscode/mcp.json` excerpt
- whether `.vscode/tasks.json` still contains `folderOpen` autostarts
- flags present in `.env`

## What likely happened (how we got here)

- Past agents added “helpful” automation:
  - MCP server definitions in `.vscode/mcp.json` (including a memory server pointing at a **~427MB** jsonl ledger).
  - VS Code tasks that autostarted daemons on `folderOpen`.
  - Playwright server/test tooling that stays running.
- Combined with huge on-disk ledgers/archives, VS Code’s file watchers + indexers do expensive work and become unstable.

## Next steps I can do (recommended)

1) Add a `scripts/agent_stop.sh` that lists PIDs first (dry-run) and then stops only the known-bad patterns.
2) Add a `scripts/agent_start.sh` that starts only the flagged services you enable (single entrypoint).
3) If you want OpenFeature: add a tiny Node/Python flag provider reading a central `flags.json` so the same flag set controls MCP + daemons + local servers.

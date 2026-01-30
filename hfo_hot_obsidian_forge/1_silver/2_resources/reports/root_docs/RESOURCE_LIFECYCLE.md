# Medallion: Silver | Mutation: 0% | HIVE: V

# Resource lifecycle (Gen88)

This is the operational “manifest + lifecycle” for always-on processes.

## Proof that Ollama is disabled

See the captured log:
- `artifacts/forensics/ollama_disable_2026-01-26T10-36-02-07-00.log`

Additional status snapshots:
- `artifacts/forensics/status_2026-01-26T10-37-59-07-00.log`
- `artifacts/forensics/status_after_settings_2026-01-26T10-41-26-07-00.log`

Expected proof markers:
- `is-enabled: disabled`
- `is-active: inactive`
- `port11434:` shows **no listener** output

## What was causing the always-on storm

1) VS Code MCP servers (workspace-managed)
- Config lives in `.vscode/mcp.json`.
- These servers previously started `npx/uvx` processes (memory/time/sequential-thinking/tavily/context7/etc).
- They are now feature-flag gated via `scripts/mcp_env_wrap.sh --if-enabled FLAG`.

2) VS Code Tasks autostart (workspace-managed)
- `.vscode/tasks.json` previously had tasks with `runOn: folderOpen` that started daemons.
- That autostart trigger was removed.

3) System services (machine-managed)
- `ollama.service` was a systemd unit with `Restart=always`.
- It is now disabled and stopped.

4) VS Code global settings (user-managed)
- Your VS Code user settings were changed to reduce auto-spawn behavior:
	- `"chat.mcp.gallery.enabled": false`
	- `"task.allowAutomaticTasks": "off"`
These help prevent MCP servers and background tasks from respawning across projects.

## Central “status dashboard” (low impact)

Run:

```bash
./scripts/agent_status_light.sh
```

This avoids heavy `ps aux` sweeps and only checks targeted offenders.

## Central “stop now” (low impact)

Run:

```bash
./scripts/agent_stop.sh
```

- Writes a proof log to `artifacts/forensics/agent_stop_<timestamp>.log`.
- Stops Playwright test-server + MCP servers.

## Feature-flag manifest (progressive enable)

Copy example flags into your repo root `.env`:

```bash
cp feature_flags.env.example .env
```

Then enable only what you need, e.g.:

```bash
# enable only minimal MCP
HFO_MCP_ENABLE_TIME=1
HFO_MCP_ENABLE_MEMORY=1
```

Everything else stays off by default.

## Recommended “safe boot” routine

1) Ensure ollama stays off:
- `systemctl is-active ollama.service` should be `inactive`
- `ss -lptn 'sport = :11434'` should show no listener

2) Before opening VS Code:
- Run `./scripts/agent_stop.sh` once.

3) Open VS Code and confirm it is not auto-starting tasks.

4) Only then, enable specific MCP flags in `.env` and re-open the workspace if needed.

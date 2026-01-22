# Medallion: Bronze | Mutation: 0% | HIVE: V

<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# HFO Handoff (Omega Gen5) — Rate Limit Recovery (2026-01-20)

This handoff is written to survive **Copilot / chat rate limiting** and to give any new agent a deterministic restart path.

## What is true right now (repo ground truth)

- Branch: `master`
- Last known pushed commit (from earlier session context): `3fd4c43` (P5: speed up pre-push blackboard purity gate)
- Current working tree is **not clean** (many modified + untracked artifacts exist). Treat the repo as “evolving Bronze”.

Run this immediately to refresh the snapshot:

- `git status -sb`
- `git --no-pager log -n 20 --oneline`

## Canonical entrypoints (agent-safe)

1) **Briefing (do this first)**
   - `python3 hfo_hub.py vision`

2) **Launcher HTML (stable surface)**
   - `active_hfo_omega_entrypoint.html` + `active_hfo_omega_entrypoint.json`
   - Legacy shim: `active_omega.html` + `active_omega.json`

3) **Gen5 artifacts (current evolution)**
   - Gen5 has evolved beyond v8; v10.x → v11 → v11.1 multi-app stepping stone.
   - Look under: `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/`

## The thing that caused “stale work” in chat

- Copilot chat rate limiting caused long-running threads to desync from repo reality.
- The repo continued evolving (new v10.x/v11/v11.1 artifacts, new gates, new governance notes).

**Rule:** treat this document + `git status` + `hfo_hub.py vision` as authoritative over any prior chat context.

## “Fastest safe resume” checklist (for any agent)

### 0) Confirm you’re looking at the right baseline

- Open `active_hfo_omega_entrypoint.html` in a browser via your local server.
- Confirm it forwards to the intended Gen5 artifact (per the JSON config / query override rules).

### 1) Run the cheapest integrity gates first

- `python3 scripts/p5_preflight_audit.py`

If `package.json` exposes these scripts, prefer them:

- `npm run p5:preflight`
- `npm run test:gen5:v11:entrypoint`

### 2) Run the “one-command” Gen5 gate (if present)

Some sessions added a v11 full gate script:

- `scripts/hfo_gen5_v11_full_gate.sh`

If it exists and `package.json` wires it, run:

- `npm run test:gen5:v11:full`

### 3) Only after gates: decide what to do with the working tree

- If the goal is **shipping**: batch commits by area (launcher, Gen5 artifact, scripts, docs) and keep pushes bounded.
- If the goal is **exploration**: keep untracked specs/reports uncommitted and add a short note in a handoff/status log.

## Known operational hazards (still relevant)

### Pre-push governance is expensive

- `git push` can be slow because it runs a full pre-push suite.
- Avoid treating “no output” as a hang; always use a bounded timeout for diagnosis:
  - `timeout 600 git push origin master`

### Blackboard churn makes everything noisier

- Any process writing to `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl` can cause manifest drift.
- Before pushing, stop blackboard writers, regenerate the manifest once, then push.

## Copilot rate limiting playbook (practical)

When you hit rate limits or the agent starts going stale:

1) **Freeze the thread into repo artifacts**
   - Write/update a single handoff doc (this file) + a “next actions” list.

2) **Switch to evidence-first mode**
   - Only use repo sources, `git status`, and runnable scripts.
   - Avoid long narrative prompts; use bullet constraints and exact commands.

3) **Make progress without chat**
   - Encode commands into scripts (or tasks) so a new agent can run them without re-deriving context.

4) **Prefer stable surfaces**
   - Use `active_hfo_omega_entrypoint.html/json` as the stable launch surface.
   - Use `hfo_hub.py vision` as the stable briefing surface.

## Where to look next (high-signal docs)

- Forensics weaknesses report: `hfo_hot_obsidian/bronze/3_resources/reports/HFO_FORENSICS_WEAKNESSES_2026_01_20.md`
- Legacy v8 handoff (historical): `hfo_omega_gen5_v8_handoff_swarm.md`

---

If you are a new agent: do **not** implement changes until you can run preflight + at least one Gen5 smoke gate successfully.

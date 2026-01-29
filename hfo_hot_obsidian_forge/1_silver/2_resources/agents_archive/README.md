# Agent Modes Archive (Hot/Silver)

This directory contains timestamped snapshots of non-core GitHub agent mode files that were moved out of `.github/agents/`.

## Why this exists

We keep only three active modes in `.github/agents/` to reduce operational drift:

- `.github/agents/hfo-basic-mcp.agent.md`
- `.github/agents/hfo-gen88-p3s.agent.md`
- `.github/agents/hfo_hive_8_agent_gen_88_v_4.agent.md`

Everything else (older modes, experiments, retired personas) belongs here.

## Layout

- Each subfolder name is a UTC timestamp (e.g. `2026_01_29T044815Z/`).
- Each subfolder contains the archived `.agent.md` files as they existed when archived.
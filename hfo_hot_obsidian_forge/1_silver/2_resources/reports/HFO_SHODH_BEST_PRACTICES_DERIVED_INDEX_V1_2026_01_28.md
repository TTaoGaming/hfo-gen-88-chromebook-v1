# Medallion: Silver | Mutation: 0% | HIVE: V

# Shodh — Best Practices (Derived Index) (V1, 2026-01-28)

## What Shodh is for (and what it is NOT)

- **Shodh is a derived, rebuildable index** over the Doobidoo SSOT.
- Shodh is for:
  - fast recall queries
  - graph-ish browsing and “relationship” exploration
  - running a service optimized for query ergonomics
- Shodh is **NOT**:
  - a write-path SSOT
  - a store you trust when it conflicts with SSOT

If Shodh is down, SSOT remains usable (via `hfo_hub.py ssot search`).

## Lifecycle (run Shodh on-demand)

- Start the Shodh server when you need it:
  - VS Code task: **Shodh Memory: Server (3030)**
- Stop it when you’re not actively using it (freeze/CPU control):
  - VS Code task: **Shodh Memory: Stop Server (3030)**

## The safe workflow (SSOT → Shodh)

1) Verify SSOT is healthy:
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py health:ssot --json`

2) Sync SSOT → Shodh (idempotent; dry-run first):
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot sync-shodh --dry-run`
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot sync-shodh`

3) Query Shodh:
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot recall-shodh --query "..." --limit 8`

## Failure modes (expected and safe)

- **Shodh unreachable**:
  - Use SSOT search: `hfo_hub.py ssot search --query "..."`.
  - Then later: start Shodh and re-run `sync-shodh`.
- **Index drift**:
  - Treat drift as normal cache staleness; rebuild via sync.

## Rebuild drills (recommended)

Shodh should be safe to delete and rebuild.

- If you suspect corruption/drift:
  - stop Shodh
  - delete/clear the derived Shodh data dir (only if you accept rebuild)
  - start Shodh
  - run `hfo_hub.py ssot sync-shodh`

## Operational guidance

- Keep Shodh “off” unless actively querying.
- Prefer SSOT for:
  - canonical writes
  - durable incident/status updates
  - audits and proofs
- Prefer Shodh for:
  - fast interactive recall
  - relationship exploration

## Related docs

- `HFO_SSOT_FRONT_DOOR_QUICKSTART_V1_2026_01_28.md`
- `HFO_GEN88_V4_DOOBIDOO_SSOT_SETUP.md`

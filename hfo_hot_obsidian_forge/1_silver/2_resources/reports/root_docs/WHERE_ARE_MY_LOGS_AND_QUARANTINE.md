# Medallion: Silver | Mutation: 0% | HIVE: V

# Where are my logs and quarantines?

This repo uses two concepts:

## 1) Proof logs (always safe)

When scripts run, they write timestamped logs here:
- `artifacts/forensics/`

These logs are small text files meant to prove “before/after” changes.

## 2) Quarantine (nondestructive storage)

Quarantine means “move aside, don’t delete”.

### VS Code quarantine (large)
Your large VS Code extension/chat data was moved here:
- `/home/tommytai3/_archive_dev_2026_1_14/0_quarantine/vscode_storage/`

This contains:
- `globalStorage/kilocode.kilo-code` (agent extension storage)
- `workspaceStorage/*/chatSessions` and `chatEditingSessions`

### Cache cleanup quarantine (future runs)
The script `scripts/cache_cleanup_safe.sh` now defaults to quarantining caches here when your archive root exists:
- `/home/tommytai3/_archive_dev_2026_1_14/0_quarantine/cache_cleanup/`

Override with:
- `HFO_QUARANTINE_ROOT=/some/path ./scripts/cache_cleanup_safe.sh --apply`

## Restore principle

Nothing is deleted by “quarantine” actions.

- To restore, move folders back to their original paths.
- To permanently reclaim disk space, delete quarantined folders only after you confirm you don’t need them.

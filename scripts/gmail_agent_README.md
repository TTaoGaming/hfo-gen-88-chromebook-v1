# Medallion: Bronze | Mutation: 0% | Guide: Gmail API Setup

Timestamp: 2026-01-19T16:58:40-07:00 (America/Denver)

## What this is
A local Gmail API scaffold for VS Code. It lists message metadata and can apply labels (optional).

## Gmail API Setup (safe + local)
1. Create a Google Cloud project.
2. Enable **Gmail API**.
3. Create **OAuth Client ID** → **Desktop app**.
4. Download the client JSON and save it to:
   - `.hfo_secret/gmail/credentials.json`
5. Keep `.hfo_secret/` local only (already git‑ignored).

## Install deps
- Use the repo venv and install from [scripts/requirements-gmail.txt](scripts/requirements-gmail.txt).

## Run
- Read metadata only (read‑only scope):
  - `python scripts/gmail_agent.py --max-results 20`
- Apply a label (requires Gmail modify scope):
  - `python scripts/gmail_agent.py --apply-label --label "triage" --max-results 50`

## Notes
- Tokens are stored at `.hfo_secret/gmail/token.json`.
- Use minimal scopes unless you need labeling.
- Avoid logging full message bodies.

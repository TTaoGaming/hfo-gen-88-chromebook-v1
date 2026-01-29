<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
# Hot/Silver Report — Host Chrome + Playwright Chromium Stabilization (Chromebook / Crostini)

Date (UTC): 2026-01-29

## Objective
Enable two workflows simultaneously, without the prior install/uninstall churn:

1) **Manual testing in ChromeOS host Chrome** (webcam-capable).
2) **Automated testing with Playwright** in penguin, without Playwright browser downloads.

## Constraints
- ChromeOS / Crostini (penguin) environment.
- Playwright browser downloads were explicitly disallowed (Chromium download loops were causing instability).
- Penguin Chromium lacked webcam access, so manual testing needed to occur in **host Chrome**.

## What Worked
### 1) Install Chromium in penguin via apt (automation browser)
Installed Debian Chromium inside penguin so Playwright has a local executable to launch.

Evidence:
- Chromium executable: `/usr/bin/chromium`
- Version observed: `Chromium 144.0.7559.96 built on Debian GNU/Linux 12`

Why this worked:
- Playwright can launch any Chromium/Chrome binary by `executablePath`.
- This avoids Playwright’s managed browser download path entirely.

Relevant repo change:
- Updated Playwright config to auto-detect `/usr/bin/chromium` as a launch target.
  - File: `playwright.config.ts`

### 2) Force host Chrome opens (manual browser) regardless of penguin Chromium
Penguin’s default browser was `chromium.desktop`, so VS Code Live Server “Open in Browser” would open container Chromium.

Fix:
- Created a custom default-browser shim `.desktop` entry that routes URLs to host Chrome using `garcon-url-handler`.
- Set it as the default browser via `xdg-settings`.

Evidence:
- `xdg-settings get default-web-browser` now returns `hfo-host-chrome.desktop`.
- Desktop file path: `~/.local/share/applications/hfo-host-chrome.desktop`
- Exec: `/usr/bin/garcon-url-handler %u`

Why this worked:
- VS Code Live Server uses VS Code “openExternal” → `xdg-open` → *default browser*.
- Changing the default browser changes where Live Server opens.

### 3) Make `npm run launch` and `npm run start:omega` open host Chrome
To make manual workflows predictable (even if defaults drift), added a tiny helper script and used it in npm scripts.

Relevant repo changes:
- Added: `scripts/open_host_url.sh`
- Updated: `package.json` scripts:
  - `start:omega`
  - `launch`

## Validation Checklist
- ✅ `chromium --version` works in penguin.
- ✅ `xdg-settings get default-web-browser` → `hfo-host-chrome.desktop`.
- ✅ Opening `http://localhost:8889/...` uses host Chrome (via `garcon-url-handler`).

## Rollback / Safety
To revert Live Server + xdg-open back to penguin Chromium:

- `xdg-settings set default-web-browser chromium.desktop`

To keep host opens explicit regardless of defaults:
- Keep using `bash scripts/open_host_url.sh <url>`.

## Notes / Follow-ups
- If Live Server still opens Chromium, check VS Code user settings:
  - `Live Server: Custom Browser` must be unset/empty (so it uses the system default).
- The CDP “attach to host Chrome” path (`http://localhost:9222`) was **not** reachable from penguin in this session; the apt-installed Chromium path is the reliable no-download alternative.

## Sources (repo)
- `playwright.config.ts`
- `package.json`
- `scripts/open_host_url.sh`
- `.vscode/tasks.json`

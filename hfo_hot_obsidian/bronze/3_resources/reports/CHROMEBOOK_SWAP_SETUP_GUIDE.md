# Medallion: Bronze | Mutation: 0% | HIVE: V

# Chromebook Plus: Swap Setup (Crostini/Linux) + Monitoring Tools

This is a **practical, step-by-step** guide to add swap on a Chromebook Plus running Linux (Crostini). It also includes tools/extensions that help you *see* memory pressure early so the workflow becomes less fragile.

## 0) Know where you’re running

On Chromebook, “Linux” usually means **Crostini**: a Linux container inside a ChromeOS-managed VM.

That matters because:

- You may be **allowed** to enable swap *inside the container* (swapfile + `swapon`).
- Or you may be **blocked** by VM/container permissions (common), and swap must be handled at ChromeOS/VM level.

In this repo, we observed:

- Swap reported as **0B**
- `swapon` not found in PATH in some runs (it lives under `/usr/sbin/swapon` on Debian)
- Attempting to enable swap inside this Crostini container fails with: **`swapon failed: Operation not permitted`**

## 0.5) Important: crosh swap vs Crostini swap

You can sometimes enable swap in **crosh** and see a non-zero swap there (example: `Swap: 7.8Gi`).

However, Crostini runs inside the **termina VM**. The swap shown in crosh may be **host-level** and not attached to the termina VM. The only reliable check for whether Linux will benefit is to check swap *inside termina*.

### Check swap inside termina (this is the one that matters for your repo)

In **crosh**:

- `vmc start termina`

Then in the `(termina)` shell:

- `free -h`
- `cat /proc/swaps`  (note the space: it’s not `cat/proc/swaps`)

If termina shows `Swap: 0B`, then the Debian container (penguin) will also see `SwapTotal: 0`.

### Common gotcha: `vsh` location

`vsh` is not always available inside the `(termina)` bash shell (you might see `vsh: command not found`). Depending on ChromeOS version/channel, you may need to run container entry commands from **crosh** instead.

From **crosh**, try one of these (varies by device):

- `vmc container termina penguin`

Or from inside `(termina)` (if available):

- `lxc list`
- `lxc exec penguin -- bash -lc 'free -h; cat /proc/swaps'`

## 1) Quick check: do you already have swap?

Run:

- `free -h`
- `cat /proc/swaps`

If `Swap: 0B` and `/proc/swaps` is empty, you have no swap enabled.

## 2) Install the missing swap tooling (inside Linux)

If `swapon: command not found`, install `util-linux`:

- Debian/Ubuntu (typical Crostini):
  - `sudo apt update`
  - `sudo apt install -y util-linux`

Verify:

- `command -v swapon && swapon --version`

If `command -v swapon` prints nothing, try:

- `ls -l /usr/sbin/swapon /usr/sbin/mkswap`

Some wrappers/tools run with a reduced PATH (e.g. missing `/usr/sbin`). In that case, use the full path:

- `sudo /usr/sbin/swapon --show`

## 3) Create a swapfile (recommended first attempt)

Pick a size. On an 8GB device, **2–8GB** is common. Start with **4GB**.

Commands:

1. Create a file:
   - `sudo fallocate -l 4G /swapfile`
   - If `fallocate` fails, use:
     - `sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=progress`
2. Secure permissions:
   - `sudo chmod 600 /swapfile`
3. Format it as swap:
   - `sudo mkswap /swapfile`
4. Enable it:
   - `sudo swapon /swapfile` (or `sudo /usr/sbin/swapon /swapfile` if PATH is restricted)

Verify:

- `swapon --show`
- `free -h`

### If you see “Operation not permitted”

That means the ChromeOS VM/container environment is blocking swap activation (this is what we hit here).

Mitigations:

- Treat swap as **not configurable from inside Debian** on this device.
- Rely on ChromeOS’s own memory compression/zram and reduce memory spikes in your workflow.
- Make the system antifragile by prioritizing bounded hydration + freezing + rollups (so crashes don’t destroy state).

## 4) Make swap persistent across reboots

Add to `/etc/fstab`:

- `echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab`

Test after reboot:

- `swapon --show`

## 5) Safer alternative: compressed RAM swap (zram)

If disk swap is slow or you want less wear on storage, zram can help.

On Debian-like systems with systemd:

- `sudo apt install -y zram-tools`
- Configure `/etc/default/zramswap`
- Enable:
  - `sudo systemctl enable --now zramswap`

Notes:

- Some Crostini setups don’t allow enabling swap/zram from inside the container.

## 6) Monitoring + “don’t crash” tools (recommended)

### Inside Linux (CLI)

Install:

- `sudo apt install -y htop iotop psmisc`

Useful commands:

- `htop` (sort by memory)
- `ps -eo pid,comm,rss,pmem,args --sort=-rss | head -n 25`
- `dmesg -T | grep -i -E 'oom|killed process|out of memory' | tail -n 50`

### VS Code extensions (low-friction)

These help you see pressure before it kills your session:

- **System Monitor / Resource Monitor** (shows RAM/CPU usage)
- **Docker** extension (if you’re running services)
- **Python** extension (profiling/debugger hooks)

(Exact extension IDs vary; search in the Marketplace for “resource monitor”, “system monitor”, “process explorer”.)

### VS Code workspace hygiene (prevents surprise RAM spikes)

This repo contains some *very large* data artifacts (DuckDB, ZIM, Parquet, JSONL ledgers). Even if you only use `tail`, background indexing + file watching can still cause pressure.

We keep paths **discoverable** while preventing auto-indexing via workspace excludes in:

- [.vscode/settings.json](../../../../.vscode/settings.json)

If you need to temporarily search inside excluded content, you can toggle `search.exclude` entries in that file.

### OS-level guardrails

If you can use systemd services, consider **earlyoom** or **systemd-oomd** to kill runaway processes earlier (more graceful than kernel OOM):

- `sudo apt install -y earlyoom`

## 7) Why swap matters for this repo

Your workflow currently includes:

- Large JSONL logs (e.g. `mcp_memory.jsonl` is hundreds of MB)
- Multiple always-on daemons and VS Code services

With **no swap**, a single accidental “read whole file into memory” can cause an immediate OOM kill.

We already applied an emergency fix in the MCP gateway hub to avoid full-file reads when tailing JSONL logs.

## 8) Next: non-destructive progressive summarization (design note)

You asked for a medallion schedule:

- Bronze: daily
- Silver: 8 days
- Gold: 64 days
- HFO: 512 days

This guide doesn’t implement that pipeline yet; it focuses on stabilizing the machine.
If you want, next I can add a script + scheduled task that:

- Copies Hot→Cold snapshots (append-only)
- Writes tamper-evident hash receipts
- Emits daily rollups into Hot Silver

---

## Quick “copy/paste” (minimal)

- `sudo apt update && sudo apt install -y util-linux`
- `sudo fallocate -l 4G /swapfile`
- `sudo chmod 600 /swapfile`
- `sudo mkswap /swapfile`
- `sudo /usr/sbin/swapon /swapfile`
- `sudo /usr/sbin/swapon --show && free -h`

If the last step prints **`swapon failed: Operation not permitted`**, you can’t enable swap from inside this Linux environment on this Chromebook.

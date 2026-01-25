# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen6 v9 Dino jump inconsistency — why it can “edge” but not jump (2026-01-21)

## Symptom

Dino “jump” behavior appears inconsistent:

- The Gen6 visuals (Babylon HUD / readiness + FSM indicators) show a state change to `READY`.
- Sometimes the Dino runner jumps.
- Sometimes it does not, even though the state change appears to have happened.

This report explains why that can happen in the current architecture and where to instrument to make it deterministic.

## The actual jump trigger is an **edge**, not a state

In Gen6 v9, Dino is triggered only on the *specific edge* `IDLE → READY`.

- Source: [omega_gen6_v9.html](../para/omega_gen6_current/omega_gen6_v9.html)
- Trigger condition:
  - `if (fsmState === 'IDLE' && fsmStateNew === 'READY') { ... }`
  - It then runs a cooldown gate and, if allowed, emits a keyboard nematocyst payload.

Important implications:

1) **“It looks READY” does not mean “trigger should fire.”**
   - If the hand is already in `READY` and remains there, there is no new edge.
   - If the hand transitions `READY → COAST → READY`, that is *not* `IDLE → READY`, so no Dino trigger.

2) Cooldown can suppress the edge.
   - Even with a real `IDLE → READY`, Dino can be suppressed if `now - lastReadyTriggerTimes[i] < readyTriggerCooldownMs`.
   - The code emits `p1:cooldown_suppressed` in this case.

### What to check in telemetry

If the HUD shows `READY` but Dino didn’t jump, immediately check whether **the system observed an eligible edge**:

- `p1:fsm_edge` (should appear for a trigger attempt)
- `p1:cooldown_suppressed` (means the edge happened but action was blocked)

The replay harness already counts these events via `window.hfoPortsEffects`.

## Delivery pipeline has multiple “success” levels

Your current telemetry differentiates *some* levels, but there’s a critical missing acknowledgment that can make the system look “successful” even when the game never received a usable key event.

### Pipeline stages

1) **FSM edge** (`IDLE → READY`) produces a payload `{ kind:'keyboard', action:'keypress', key:' ', code:'Space' }`.
2) **AdapterHost delivery** (`window.hfoAdapterHost.deliverEffect('dino-v1', payload)`) attempts `postMessage` into the **Dino wrapper iframe**.
   - Emits: `p7:adapter_deliver`, `p7:dino_queue`, `p7:dino_postMessage`
3) **Wrapper receives message** and forwards it into the inner runner frame via a nematocyst adapter.
   - Wrapper: [dino_v1_wrapper.html](../para/omega_gen6_current/dino_v1_wrapper.html)
   - Adapter: [official_adapters/dino_runner_nematocyst/adapter.js](../para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js)

### Where “it can look green” but still fail

#### A) `postMessage` success is not “jump success”

In AdapterHost, `ok: true` means **`iframe.contentWindow.postMessage(...)` did not throw**.

- That does *not* mean the wrapper’s inner runner is loaded.
- That does *not* mean the wrapper successfully synthesized key events.

Your Playwright replay gate currently asserts `dino_postMessage ok >= N`, which validates *transport*, not *effect*.

#### B) Wrapper can accept message before inner runner is ready

The wrapper hosts an inner iframe (`id="frame"`) pointing to `./vendor/t-rex-runner/index.html`.

In the adapter, a successful injection requires:

- `frameEl.contentDocument` and `frameEl.contentWindow` to be non-null.

If the wrapper is loaded but the inner runner iframe is still loading, `dispatchKeypress(...)` returns `false`, and the Dino jump will not happen.

Current observability gap:

- The adapter **already emits an ack** back to the parent:
  - `postMessage({ type: 'hfo:nematocyst:ack', payload: { ok: boolean, reason?: string } })`
  - Source: [adapter.js](../para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js)
- But the Gen6 host **does not currently listen** for that ack.

So you can see:

- `p1:fsm_edge` ✅
- `p7:dino_postMessage ok` ✅

…and still get **no jump** because the actual injection failed inside the wrapper.

#### C) Two Dino iframe mounts can fight over `systemState.ui.dinoWrapperIframe`

Gen6 v9 contains **two** Dino overlay mount paths:

- SRP layer: mounts Dino with `display: block` (dev sidecar)
- HERO touch2d layer: mounts Dino with `display: none` by default

Both write:

- `systemState.ui.dinoWrapperIframe = iframe`

Depending on mount order, `systemState.ui.dinoWrapperIframe` can point to:

- a hidden iframe,
- an iframe that has not fired `load` yet,
- or an iframe that gets torn down while another is visible.

That makes delivery timing appear inconsistent even if the FSM math is stable.

### What to check in telemetry

To isolate where it failed, follow this ladder:

1) **Did the edge happen?**
   - `p1:fsm_edge` present? If not, you only saw “READY-ish” visuals, not an `IDLE → READY` edge.

2) **Was it suppressed?**
   - `p1:cooldown_suppressed` present? Then the edge happened but you intentionally blocked action.

3) **Did we attempt delivery?**
   - `p3:nematocyst_deliver` (host emits this on trigger attempt)

4) **Did we postMessage successfully?**
   - `p7:dino_postMessage ok` vs `p7:dino_postMessage ok:false`

5) **Did the wrapper successfully synthesize the key?**
   - Missing today: there is no host-side telemetry for `hfo:nematocyst:ack`.

## So is it the dwell / leaky bucket?

Sometimes yes — but “inconsistency” is more often a *gating mismatch* or *delivery/ready race*.

The leaky bucket (charge/drain) influences whether `readiness` crosses `hysteresisHigh`, but the more subtle inconsistency you’re describing (“the state changed but the jump didn’t”) matches these failure modes better:

- The system enters `READY` (visual), but not via `IDLE → READY`.
- The system edges `IDLE → READY`, but cooldown suppresses action.
- The system edges and posts a message, but the wrapper’s inner runner frame isn’t ready, so key synthesis fails.
- The wrong Dino iframe instance is referenced (SRP vs HERO race).

## Recommendations (make it deterministic)

### 1) Wire ACK telemetry (high leverage)

Listen in the Gen6 host for `message` events from the wrapper:

- `type: 'hfo:nematocyst:ack'`

Then emit a Ports Effects event:

- `p7:dino_ack { ok, reason }`

This upgrades “postMessage ok” into “effect ok”.

### 2) Add wrapper-side queueing for inner runner readiness

In the wrapper adapter:

- If `frameEl.contentDocument` is not available, queue the payload.
- Flush on the inner runner iframe `load` event.

### 3) De-conflict multiple Dino mounts

Avoid having both SRP and HERO write to the same global `systemState.ui.dinoWrapperIframe`.

Options:

- Store per-owner references (e.g., `dinoWrapperIframeByOwner`) and have AdapterHost select the active/visible one.
- Or, ensure only one Dino mount exists at a time in v9 dev mode.

### 4) Align the trigger semantics with your mental model

If the intent is “jump whenever we are READY” (not only on the edge), then change the trigger to:

- fire on `READY` dwell thresholds or
- fire on `READY → COMMIT` (pointer/intent edge), or
- fire on `READY` entry + periodic repeat while held.

Right now, it’s explicitly **edge-only**: `IDLE → READY`.

## Practical debug checklist

When you experience a “READY but no jump” moment:

1) Open the Ports Effects panel and filter to:
   - `p1:fsm_edge`
   - `p1:cooldown_suppressed`
   - `p3:nematocyst_deliver`
   - `p7:dino_queue`, `p7:dino_flush_queue`, `p7:dino_postMessage`

2) Confirm which Dino iframe is currently assigned:
   - Look at `dino` state in Ports Effects (`iframePresent`, `readyState`, `queueLength`).

3) If `dino_postMessage ok` is true but there is no jump, treat it as “transport ok, effect unknown” until ACK is wired.

## Sources

- Gen6 v9 (FSM + AdapterHost + Dino mount): [omega_gen6_v9.html](../para/omega_gen6_current/omega_gen6_v9.html)
- Dino wrapper: [dino_v1_wrapper.html](../para/omega_gen6_current/dino_v1_wrapper.html)
- Wrapper nematocyst adapter (includes ack): [official_adapters/dino_runner_nematocyst/adapter.js](../para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js)
- v9 spec (mentions optional ack): [omega_gen6_v9.yaml](../para/omega_gen6_current/omega_gen6_v9.yaml)

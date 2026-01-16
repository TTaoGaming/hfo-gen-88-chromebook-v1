Finish Phase 4 (offline/no-CDN): make V28 run fully with local WASM/models/libs. Your own spec calls this out as a hard requirement.

omega_gen4_v25_spec

MediaPipe’s FilesetResolver supports a base path for loading WASM locally—use that.

Make UPE truly authoritative: no other code should compute clientX/clientY mappings or zoom margins outside UPE. If anything still does, you’ll keep getting “parity drift.”

Lock the operator loop: implement the Essentials/Developer gate + a single readiness gauge that is the only “arming truth” in the UI. (This is the path to “one successful click in 30s” without debug noise.)

omega_gen4_v25_spec
---

ok let's give P5 a preflight audit, and quality gate. we need to give p4 a visual regression tool because we definitely have visual regression. i clikced start live server extension and getting this, when just earlier it was working correctly, why is there regressions like this? do a forensice audit and upgrade Port 4 and Port 5 and tell me if you see the root cause problem. do not fix the problem yet, create the evaluation harness that catches this goldenlayout-dark-theme.css:1  Failed to load resource: net::ERR_CONNECTION_RESET
babylon.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
babylon.loaders.min.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
web-sdk.min.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
omega_gen4_v30_1.html:3403 Live reload enabled.
omega_gen4_v30_1.html:3397 WebSocket connection to 'ws://127.0.0.1:5500/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v30_1.html/ws' failed:
(anonymous) @ omega_gen4_v30_1.html:3397
vision_bundle.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
lil-gui.esm.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
planck.esm.js:1  Failed to load resource: net::ERR_CONNECTION_RESET
zod.esm.js:1  Failed to load resource: net::ERR_CONNECTION_RESET

---

create a forensics report, why was it working before and then regressed? if it wasn't working at all that makes sense, but why would it work and then break? that is a clear sign th ai created PORT 5 is WEAK and doesn't guard me correctly
---

running npm run launch starts this error. This site can’t be reached
The connection was reset.
Try:

Checking the connection
Checking the proxy and the firewall
Running Connectivity Diagnostics
ERR_CONNECTION_RESET. WHAT IS HAPPENING WITH MY APP. why are you ai agents regressing and not being caught? why is my system so WEAK?
---

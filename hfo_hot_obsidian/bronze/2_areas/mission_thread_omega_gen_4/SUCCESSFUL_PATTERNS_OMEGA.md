# Medallion: Bronze | Mutation: 0% | HIVE: E

# 🎯 Successful Patterns: Omega Gen 4 (V1-V19)

As of V19.6, the following architectural patterns have been verified and promoted to "Silver" candidate status for hardened implementation.

## 1. 📂 Centralized Data Fabric (Port 1 Fusion)

- **Pattern**: All sensory data (MediaPipe) MUST pass through `P1Bridger.fuse()` before reaching UI or Physics components.
- **Enforcement**: `scripts/fabric_auditor.py` uses regex to ensure `results.landmarks` is never accessed locally within components, ensuring strict dependency on the Zod-validated `DataFabricSchema`.
- **Benefit**: Ensures a single source of truth for coordinates, facilitating "Mirror Awareness" and "Temporal Smoothing" at a single bottleneck.

## 2. 🪞 Centralized Mirror Awareness

- **Pattern**: Flipping coordinates `(1.0 - x)` and vector math is handled EXCLUSIVELY in Port 1 during fusion.
- **Enforcement**: Removed CSS `transform: scaleX(-1)` from video feeds to prevent "Double Mirroring" bugs.
- **Benefit**: Coordination between the virtual physics laser and the real video hand is guaranteed regardless of camera orientation.

## 3. 🧪 Multi-Tenancy Effects (JuiceLayers)

- **Pattern**: Visualization effects (PixiJS) are decoupled from the main loops into a `JuiceSubstrate` class.
- **Enforcement**: `systemState.ui.juiceLayers` array allows multiple visualizers (Hero view, Tactical view) to subscribe to the same data fabric stream.
- **Benefit**: Enables layering WebGL effects over disparate 2D canvas elements without code duplication.

## 4. 📐 MCP-Anchored Rigid Rod Projection

- **Pattern**: Projection rays originate from the MCP (Knuckle) rather than the Index Tip.
- **Benefit**: drastically improves stability and "leverage" during pointing, as the knuckle move less than the tip during fine gesture adjustments.

## 🛡️ P5 Integrity Standard

- All pattern promotions require a `P5 Forensic Audit` receipt confirming:
  - Medallion Provenance Headers present.
  - No Slop/Theater (Stubs) found in active logical paths.
  - Chronological blockchain integrity (CHRONOS PASS).
## 5. 🧩 Hybrid Strategy Adapter (V28 Heuristics)
- **Pattern**: Solving DOM interaction failures through recursive ancestor search (`findInteractiveParent`) and 10ms state-settling delays.
- **Benefit**: Bridges the gap between clean architectural dispatch (W3C Pointer Events) and the messy reality of nested, state-driven UI frameworks like React/Excalidraw.
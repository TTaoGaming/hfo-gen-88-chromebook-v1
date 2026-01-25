# Medallion: Bronze | Mutation: 0% | HIVE: V

<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Dino Runner Nematocyst Adapter (Bronze)

## Purpose

Bridge HFO Port 3 (W3C Pointer Nematocyst Injector) to a keyboard-driven same-origin Dino Runner surface by accepting a small `hfo:nematocyst` payload and synthesizing a Space keypress into the inner runner frame.

## Constraints

- Same-origin only (fail-closed on `postMessage` origin mismatch).
- No upstream Dino code copied/rewritten here.
- Adapter is a thin wrapper: payload in → keypress out.

## Files

- adapter_manifest.json
- adapter.js

## Target

- Wrapper: ../../dino_v1_wrapper.html
- Vendored runner: ../../vendor/t-rex-runner/index.html

## Notes

- This adapter only provides keyboard injection. Pointer injection remains handled by the existing Port 3 injector pipeline.

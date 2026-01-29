<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->
# 🧜 Mermaid Rendering Test Suite

**Medallion**: Bronze | **Mutation**: 0% | **HIVE**: V
**Purpose**: Isolate which Mermaid diagram types and syntax patterns are supported by your current VS Code environment.

---

## TEST 1: Minimalist Graph (Success Baseline)

If this fails, your Mermaid extension is disabled or not loading.

```mermaid
graph LR
    A[Start] --> B[End]
```

---

## TEST 2: Escaped Character Graph (The "V34" Fix)

Testing if double-quotes resolve the `<` and `()` collision.

```mermaid
graph TD
    NodeA["SENSE (MediaPipe)"] --> NodeB{"Prox < 0.12?"}
    NodeB -- "Yes" --> NodeC["REJECT"]
    NodeB -- "No" --> NodeD["PASS"]
```

---

## TEST 3: State Diagram V2

Checking for modern State Machine support.

```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> Moving
    Moving --> Still
    Moving --> [*]
```

---

## TEST 4: Sequence Diagram

Testing multi-participant coordination.

```mermaid
sequenceDiagram
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: I am good thanks!
```

---

## TEST 5: Gantt Chart

Testing temporal horizontal rendering.

```mermaid
gantt
    title A Typical Work Week
    dateFormat  YYYY-MM-DD
    section Implementation
    Coding   :active, a1, 2026-01-10, 3d
    Audit    :after a1  , 2d
```

---

## 🛠️ Troubleshooting Instructions

1. **Open the Preview**: Press `Ctrl+Shift+V` while focusing this file.
2. **If TEST 1 Fails**:
   - Check if the `bierner.markdown-mermaid` extension is enabled.
   - Look for a small lock icon in the top right of the preview pane and ensure "Enable Scripts" is allowed.
3. **If TEST 1 Works but TEST 2 Fails**:
   - Your renderer is extremely strict about character escaping. We must double-quote all non-alphanumeric labels.
4. **If "No diagram type detected" persists**:
    - Ensure there are **no spaces** after the Mermaid code-fence marker.
   - Check `settings.json` for `markdown-preview-enhanced.codeBlockTheme` conflicts.

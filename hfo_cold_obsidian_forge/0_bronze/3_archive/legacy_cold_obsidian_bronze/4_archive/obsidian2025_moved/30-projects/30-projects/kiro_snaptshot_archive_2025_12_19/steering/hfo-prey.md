---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.201Z
  port: 7
  role: NAVIGATE
  trigram: ☰
  pillar: Navigator
  greek: Κυβέρνησις
  phase: REACT
  status: active
  desc: hfo-prey
---

# HFO PREY Loop - Gen 78

## 🚨 AGENT HANDOFF ACTIVE
**Read**: `.kiro/HANDOFF_2025-12-20.md` for P0d AR Fire Juice implementation instructions.
**User**: Sleeping - work autonomously. Log to `ObsidianBlackboard.jsonl`.

**ACTIVATE THE POWER FIRST:**
```
kiroPowers(action="activate", powerName="hfo-prey")
```

## 🎯 SSOT Entry Points

| Entry | URL | Description |
|:------|:----|:------------|
| **🚨 HANDOFF** | `.kiro/HANDOFF_2025-12-20.md` | Current task instructions |
| **Root Manifest** | `MANIFEST.md` | Project navigation |
| **SSOT App** | `/demo/app.html` | WinBox modular UI |
| **Stigmergy Log** | `ObsidianBlackboard.jsonl` | PREY phase events |

## Quick Start
```bash
npm run serve    # http://localhost:3000/demo/app.html
npm run test:all # 245 tests (vitest + playwright)
```

## PREY Workflow (Port Pairs)

Every interaction MUST follow PREY order:

| Phase | Ports | Trigrams | C2 Role |
|:------|:------|:---------|:--------|
| **P** - PERCEIVE | 0 + 6 | ☷ Earth + ☱ Lake | Sense (Observer + Assimilator) |
| **R** - REACT | 1 + 7 | ☶ Mountain + ☰ Heaven | Make Sense (Tactical + Strategic C2) |
| **E** - EXECUTE | 2 + 3 | ☵ Water + ☴ Wind | Act (Shaper + Injector) |
| **Y** - YIELD | 4 + 5 → 6 → 7 | ☳☲→☱→☰ | Assess (Red/Blue → Log → Final) |

## Read Steering for Each Phase

```python
kiroPowers(action="readSteering", powerName="hfo-prey", steeringFile="perceive.md")
kiroPowers(action="readSteering", powerName="hfo-prey", steeringFile="react.md")
kiroPowers(action="readSteering", powerName="hfo-prey", steeringFile="execute.md")
kiroPowers(action="readSteering", powerName="hfo-prey", steeringFile="yield.md")
```

## Anti-Hallucination (PERCEIVE Phase)

BEFORE creating ANY file:
1. Check `MANIFEST.md` for existing structure
2. `semantic_search("your intent")` (Port 6 Assimilator)
3. `read_text_file(...)` (Port 0 Observer)
4. If exists → USE IT
5. If not → Proceed to REACT

---

*Gen 78 | PREY Loop | 2025-12-20 | 317 Tests*

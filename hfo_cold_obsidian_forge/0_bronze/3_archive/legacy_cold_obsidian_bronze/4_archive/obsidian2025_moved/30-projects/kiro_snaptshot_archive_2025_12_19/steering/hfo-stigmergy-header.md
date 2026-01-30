---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.202Z
  port: 7
  role: NAVIGATE
  trigram: ☰
  pillar: Navigator
  greek: Κυβέρνησις
  phase: REACT
  status: active
  desc: hfo-stigmergy-header
---

# HFO Stigmergy Header Standard

## Purpose

All HFO source files MUST include a YAML frontmatter header for version tracking and port assignment. This enables stigmergy coordination across the codebase.

## Header Format (TypeScript)

```typescript
/**
 * @hfo-stigmergy
 * ---
 * generation: 78
 * timestamp: 2025-12-20T19:30:00Z
 * port: 2
 * trigram: ☵
 * role: TRANSFORM
 * pillar: Shaper
 * status: active
 * ---
 */
```

## Header Format (Markdown)

```yaml
---
hfo:
  generation: 78
  timestamp: 2025-12-20T19:30:00Z
  port: 6
  trigram: ☱
  role: REMEMBER
  pillar: Assimilator
  status: active
---
```

## 8 Pillars (Greek Ontology)

| Port | Trigram | Pillar | Greek | Role |
|:-----|:--------|:-------|:------|:-----|
| 0 | ☷ | Observer | Αἴσθησις (Aisthesis) | SENSE |
| 1 | ☶ | Bridger | Σύνδεσμος (Syndesmos) | CONNECT |
| 2 | ☵ | Shaper | Μορφή (Morphe) | TRANSFORM |
| 3 | ☴ | Injector | Ἔκχυσις (Ekchysis) | DELIVER |
| 4 | ☳ | Disruptor | Χάος (Chaos) | CHAOS |
| 5 | ☲ | Immunizer | Ἀσφάλεια (Asphaleia) | VALIDATE |
| 6 | ☱ | Assimilator | Μνήμη (Mneme) | REMEMBER |
| 7 | ☰ | Navigator | Κυβέρνησις (Kybernesis) | NAVIGATE |

## Status Values

- `active` - Currently in use
- `deprecated` - Scheduled for removal
- `theater` - Code exists but not wired
- `archived` - Moved to reference/

## Validation Rules

1. WHEN file lacks header THEN add with current generation
2. WHEN generation increments THEN update all active files
3. WHEN port assignment is wrong THEN flag for refactoring
4. WHEN status changes THEN log to stigmergy

## Example: Port 2 Shaper File

```typescript
/**
 * @hfo-stigmergy
 * ---
 * generation: 78
 * timestamp: 2025-12-20T19:30:00Z
 * port: 2
 * trigram: ☵
 * role: TRANSFORM
 * pillar: Shaper
 * greek: Μορφή
 * status: active
 * contracts:
 *   input: CanonicalLandmarks
 *   output: CanonicalIntent
 * ---
 * 
 * One Euro Filter - Position smoothing for cursor movement
 */

export class OneEuroFilter {
  // ...
}
```

---

*HFO Gen 78 | Stigmergy Header Standard | 2025-12-20*

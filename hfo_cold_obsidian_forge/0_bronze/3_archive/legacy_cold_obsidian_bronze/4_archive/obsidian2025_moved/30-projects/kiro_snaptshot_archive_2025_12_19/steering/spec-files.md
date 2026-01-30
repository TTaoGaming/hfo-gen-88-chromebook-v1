---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.203Z
  port: 7
  role: NAVIGATE
  trigram: ☰
  pillar: Navigator
  greek: Κυβέρνησις
  phase: REACT
  status: active
  desc: spec-files
---

---
inclusion: fileMatch
fileMatchPattern: "**/.kiro/specs/**/*.md"
---

# Spec File Standards (HFO Gen 76)

## Phoenix Protocol Rules
1. **Intent Before Implementation**: Create Grimoire spell card BEFORE coding
2. **One Spec Per Day**: Named `hfo-daily-YYYY-MM-DD`
3. **EARS Patterns**: Use structured requirement language

## EARS Requirement Patterns
- **Ubiquitous**: The system SHALL [action]
- **Event-Driven**: WHEN [trigger] THEN the system SHALL [action]
- **State-Driven**: WHILE [state] the system SHALL [action]
- **Optional**: WHERE [condition] the system SHALL [action]
- **Unwanted**: IF [condition] THEN the system SHALL [action]

## Spec Structure
```
.kiro/specs/hfo-daily-YYYY-MM-DD/
├── requirements.md   # WHAT (EARS patterns)
├── design.md         # HOW (architecture, data models)
└── tasks.md          # WHEN (implementation phases)
```

## Requirements Format
```markdown
### Requirement N: Title

**User Story:** As a [role], I want [goal], so that [benefit].

#### Acceptance Criteria
1. WHEN [trigger] THEN the system SHALL [action]
2. IF [condition] THEN the system SHALL [action]
```

## Task Format
```markdown
- [ ] N. Task title
  - [ ] N.1 Subtask
    - Details
    - _Requirements: X.Y_
```

## Checkpoints
- Include checkpoint after each phase
- Mark completed tasks with `[x]` and ✅
- Add verification notes

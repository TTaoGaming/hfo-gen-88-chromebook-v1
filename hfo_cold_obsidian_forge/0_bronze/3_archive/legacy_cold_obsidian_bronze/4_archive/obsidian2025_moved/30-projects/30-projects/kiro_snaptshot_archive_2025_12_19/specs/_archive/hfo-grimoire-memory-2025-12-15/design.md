# Design Document: HFO Grimoire Memory Consolidation

## Overview

This design describes the process of ingesting 76 generations of HFO knowledge into the memory system (stigmergy-assimilator), consolidating it, and generating a high-fidelity 9-card Grimoire for Gen 76. The system uses the MCP memory server as the knowledge graph backbone.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                                │
├─────────────────────────────────────────────────────────────────┤
│  Gen 1-72 Backup          │  Gen 73-76 HFO_buds                │
│  ├── DuckDB (bronze)      │  ├── generation_73/                │
│  └── Deep Dive MDs        │  ├── generation_74/                │
│                           │  ├── generation_75/                │
│                           │  └── generation_76/                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MEMORY SYSTEM (for-assimilating)              │
├─────────────────────────────────────────────────────────────────┤
│  Entities:                                                      │
│  ├── HFO_System (root)                                         │
│  ├── Observer, Bridger, Shaper, Injector (roles 0-3)           │
│  ├── Disruptor, Immunizer, Assimilator, Navigator (roles 4-7)  │
│  ├── Heartbeat_Mantra                                          │
│  └── Card_64_Manifest                                          │
│                                                                 │
│  Relations:                                                     │
│  ├── role MAPS_TO polymorphic (Greek, I Ching, Gherkin, etc)   │
│  ├── role CONNECTS_TO role (pipeline flow)                     │
│  └── mantra_line ENCODES role                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GEN 76 GRIMOIRE OUTPUT                        │
├─────────────────────────────────────────────────────────────────┤
│  hfo_grimoire/                                                  │
│  ├── CARD_64.md           (manifest, <600 tokens)              │
│  └── silver/                                                    │
│      ├── deck_0_observer.md   (<800 tokens)                    │
│      ├── deck_1_bridger.md    (<800 tokens)                    │
│      ├── deck_2_shaper.md     (<800 tokens)                    │
│      ├── deck_3_injector.md   (<800 tokens)                    │
│      ├── deck_4_disruptor.md  (<800 tokens)                    │
│      ├── deck_5_immunizer.md  (<800 tokens)                    │
│      ├── deck_6_assimilator.md (<800 tokens)                   │
│      └── deck_7_navigator.md  (<800 tokens)                    │
│                                                                 │
│  TOTAL: 9 files, <7000 tokens                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Ingestion Component

**Interface**: `ForAssimilating` (MCP memory server)

**Operations**:
- `create_entities`: Create role entities with type and observations
- `create_relations`: Link roles to polymorphic mappings and each other
- `add_observations`: Append knowledge from each generation

**Data Flow**:
1. Read Gen 1-72 deep dive files → Extract key concepts → Add as observations
2. Read Gen 73-76 card files → Extract 8 Greek sections → Add as observations
3. Create relations between roles based on OBSIDIAN pipeline

### 2. Consolidation Component

**Process**:
1. Query all observations for each role
2. Deduplicate and merge similar observations
3. Rank by detail level (longer = more detailed)
4. Preserve generation provenance

### 3. Generation Component

**Process**:
1. Query memory for role entity
2. Extract observations grouped by Greek question
3. Format into deck card template
4. Validate token count < 800
5. Write to silver layer

## Data Models

### Entity Schema

```
Entity {
  name: string           // e.g., "Observer", "Bridger"
  entityType: string     // "OBSIDIAN_Role" | "Manifest" | "Concept"
  observations: string[] // Knowledge fragments from all generations
}
```

### Relation Schema

```
Relation {
  from: string      // Source entity name
  to: string        // Target entity name
  relationType: string  // "MAPS_TO" | "CONNECTS_TO" | "ENCODES"
}
```

### Deck Card Schema

```markdown
# Deck N: ROLE (☰ Trigram) - Cards X-Y
## "Mantra Line" | for-{verb}ing | GHERKIN

> One-line description

---

## Card X: Role × Ontos
**What IS {role}?**
{content from memory observations}

## Card X+1: Role × Logos
**What CONNECTS {role}?**
{content}

... (8 sections total)

---

```gherkin
Feature: {Role} Deck
  Scenario: {behavior}
    Given/When/Then
```

*Deck N | Role | Gen 76 | SSOT*
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Role Entity Completeness
*For any* OBSIDIAN role (0-7), the memory system should contain an entity with observations from multiple generations.
**Validates: Requirements 1.4**

### Property 2: Polymorphic Mapping Completeness
*For any* role entity, the observations should include all 4 polymorphic mappings (Greek, I Ching, Gherkin, Binary).
**Validates: Requirements 2.2**

### Property 3: Deck Card Section Completeness
*For any* generated deck card, the content should include all 8 Greek sections (Ontos, Logos, Techne, Chronos, Pathos, Ethos, Topos, Telos).
**Validates: Requirements 3.2**

### Property 4: Deck Card Gherkin Inclusion
*For any* generated deck card, the content should include a valid Gherkin feature block.
**Validates: Requirements 3.4**

### Property 5: Manifest Deck Reference Completeness
*For any* manifest card, it should reference exactly 8 deck file paths.
**Validates: Requirements 4.3, 4.4**

### Property 6: Deck Card Token Budget
*For any* generated deck card, the token count should be under 800 tokens.
**Validates: Requirements 5.2**

### Property 7: Memory Queryability
*For any* role name query, the memory system should return non-empty observations.
**Validates: Requirements 6.1**

### Property 8: Consolidation Output Count
*For any* completed consolidation, the memory system should have exactly 9 primary entities (8 roles + 1 manifest).
**Validates: Requirements 7.2**

## Database Consolidation Strategy

### Current State

**Active Repo DuckDB Files (3 total):**
```
generation_1_to_generation_72_backup_QUINE_2025_12_14_12_38_31/
├── generation_73_bronze.duckdb
├── hfo_bronze_consolidation.duckdb
└── hfo_bronze_all_gen_1_to_72_2025_12_14_13_30_00.duckdb  ← PRIMARY
```

**READ-ONLY Reference (DO NOT MODIFY):**
```
Inputs/Safe_Data/  ← NEVER TOUCH THIS FOLDER
├── hfo_knowledge_2025_12_12.duckdb (reference only)
├── hfo_memory_dump_2025-12-12.jsonl (reference only)
└── Historical_Buds_gem_gen_53_to_gen_67/ (reference only)
```

**Active HFO_buds:**
```
HFO_buds/
├── generation_72/
├── generation_73/
├── generation_74/
├── generation_75/
└── generation_76/  ← TARGET OUTPUT
```

### Consolidation Options

#### Option A: Single DuckDB + MCP Memory (Recommended)

| Component | Location | Purpose |
|:----------|:---------|:--------|
| Bronze DB | `data_lake/bronze/hfo_gen76.duckdb` | Historical queries |
| MCP Memory | In-memory (stigmergy-assimilator) | Active knowledge graph |
| Archive | `archive/gen_1_to_75.tar.gz` | Compressed history |

**Tradeoffs:**
- ✅ Single source of truth for queries
- ✅ MCP memory for real-time agent access
- ✅ Compressed archive reduces confusion
- ❌ Requires migration effort
- ❌ Archive not directly queryable

#### Option B: Medallion Lake (Bronze/Silver/Gold DuckDB)

| Layer | Location | Purpose |
|:------|:---------|:--------|
| Bronze | `data_lake/bronze/hfo_raw.duckdb` | All raw data |
| Silver | `data_lake/silver/hfo_validated.duckdb` | Cleaned/validated |
| Gold | `data_lake/gold/hfo_grimoire.duckdb` | Query-optimized |

**Tradeoffs:**
- ✅ Standard data lake pattern
- ✅ Clear data lineage
- ✅ Each layer queryable
- ❌ 3 databases to maintain
- ❌ More complex than needed for 9 cards

#### Option C: JSONL + MCP Memory Only (Minimal)

| Component | Location | Purpose |
|:----------|:---------|:--------|
| Archive | `archive/hfo_gen_1_to_75.jsonl.gz` | Compressed history |
| MCP Memory | In-memory | Active knowledge |
| Grimoire | `HFO_buds/generation_76/hfo_grimoire/` | 9 markdown files |

**Tradeoffs:**
- ✅ Simplest architecture
- ✅ No database maintenance
- ✅ Grimoire is the SSOT
- ❌ Historical queries require decompression
- ❌ No SQL access to history

#### Option D: Hybrid (DuckDB for History + Grimoire for Active)

| Component | Location | Purpose |
|:----------|:---------|:--------|
| History DB | `data_lake/bronze/hfo_history.duckdb` | Gen 1-75 queries |
| Grimoire | `HFO_buds/generation_76/hfo_grimoire/` | Gen 76 SSOT |
| MCP Memory | In-memory | Agent working memory |

**Tradeoffs:**
- ✅ History queryable via SQL
- ✅ Grimoire is clean SSOT
- ✅ MCP for agent context
- ❌ Two systems to understand
- ❌ Sync between DB and Grimoire

### Recommended Approach: Option A

**Rationale:**
1. Single DuckDB for all historical queries
2. MCP memory for agent working context
3. Grimoire (9 files) as human-readable SSOT
4. Archive old databases to reduce confusion

**Migration Steps:**
1. Use existing `hfo_bronze_all_gen_1_to_72_2025_12_14_13_30_00.duckdb` as primary (no copy needed)
2. Create new `data_lake/bronze/hfo_gen76.duckdb` for Gen 76 specific data
3. READ from `Inputs/Safe_Data/` for reference (NEVER WRITE)
4. Ingest key concepts into MCP memory from all sources
5. Generate 9 Grimoire cards from memory to `HFO_buds/generation_76/`
6. Update MCP config to point to new locations

## Error Handling

| Error | Handling |
|:------|:---------|
| Memory server unavailable | Retry 3 times, then fail with clear message |
| File not found during ingestion | Log warning, continue with available files |
| Token budget exceeded | Truncate least important observations |
| Duplicate entity creation | Merge observations into existing entity |

## Testing Strategy

### Property-Based Testing

**Library**: Hypothesis (Python) or fast-check (TypeScript)

**Properties to test**:
1. Role entity completeness (Property 1)
2. Polymorphic mapping completeness (Property 2)
3. Deck card section completeness (Property 3)
4. Token budget compliance (Property 6)
5. Memory queryability (Property 7)

### Unit Tests

1. Entity creation with observations
2. Relation creation between entities
3. Deck card template formatting
4. Token counting accuracy

### Integration Tests

1. Full ingestion pipeline (Gen 1-72 + Gen 73-76)
2. Consolidation process
3. Card generation from memory
4. End-to-end: ingest → consolidate → generate → verify

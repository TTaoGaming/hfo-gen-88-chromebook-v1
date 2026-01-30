# HFO Portable Memory Bank

**Coverage:** Pre-HFO (HOPE, Tectangle, Spatial) through Generation 84  
**Created:** 2025-12-27T21:46:52Z  
**Size:** ~120MB  
**Artifacts:** 6,423 documents

## Purpose

This is a portable AI memory bank containing the complete HFO Evolution Timeline. It enables AI agents to have persistent memory across sessions, understanding the full context of the HFO project from its origins through Gen 84.

## Contents

| File | Description |
|------|-------------|
| `hfo_memory.duckdb` | DuckDB database with FTS enabled |
| `AGENTS.md` | Instructions for AI agents |
| `llms.txt` | LLM-friendly context summary |
| `tools/` | Python utilities for querying |

## Quick Start

```python
import duckdb

con = duckdb.connect('hfo_memory.duckdb', read_only=True)
con.execute('LOAD fts')

# Search for content
results = con.execute("""
    SELECT filename, generation, 
           fts_main_artifacts.match_bm25(id, 'obsidian spider') as score
    FROM artifacts 
    WHERE score IS NOT NULL
    ORDER BY score DESC
    LIMIT 10
""").fetchall()

for r in results:
    print(f"Gen {r[1]}: {r[0]} (score: {r[2]:.2f})")
```

## Search Capabilities

### Currently Working
- **FTS (Full-Text Search)** ✅ - BM25 ranking on content, filename, path

### Planned
- **VSS (Vector Semantic Search)** 🔜 - Embedding-based similarity
- **GraphRAG** 🔜 - Entity/relation graph traversal
- **RRF (Reciprocal Rank Fusion)** 🔜 - Combined ranking from all methods

## Database Schema

```sql
-- Main content table
artifacts (
    id VARCHAR PRIMARY KEY,
    era VARCHAR,           -- 'hfo', 'hope', 'tectangle', 'spatial'
    generation INTEGER,    -- 1-84 for HFO, NULL for pre-HFO
    filename VARCHAR,
    path VARCHAR,
    content VARCHAR,
    content_hash VARCHAR,
    modified VARCHAR,
    char_count INTEGER,
    created_at TIMESTAMP
)

-- Future tables (empty, ready for population)
embeddings (artifact_id, embedding, model, created_at)
entities (id, name, type, generation, era, metadata)
relations (id, source_id, target_id, relation_type, weight, metadata)
```

## Era Timeline

| Era | Period | Description |
|-----|--------|-------------|
| hope | Jan-Aug 2025 | HOPEAI/HOPEOS foundation |
| tectangle | Early 2025 | Tectangle experiments |
| spatial | Early 2025 | Spatial computing work |
| hfo (Gen 1-31) | Sep 2025 | HFO foundation, Zero Invention |
| hfo (Gen 32-52) | Oct 2025 | Vector experiments |
| hfo (Gen 53-67) | Oct-Nov 2025 | Historical Buds consolidation |
| hfo (Gen 68-84) | Nov-Dec 2025 | Rapid iteration, Kraken Keeper |

## Key Concepts

- **Obsidian Spider** - The Godhead archetype, Card 09
- **Zero Invention Principle** - Core HFO philosophy
- **Stigmergy** - Indirect coordination via environment
- **Kraken Keeper** - Memory/knowledge management system
- **Historical Buds** - Preserved knowledge snapshots
- **Grimoire Cards** - Archetypal concept cards

## License

Internal use only. Part of the HFO Evolution Timeline project.

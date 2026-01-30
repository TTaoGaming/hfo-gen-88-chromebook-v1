# AGENTS.md — HFO Portable Memory Bank

## Status (2025-12-27)

| Component | Status | Notes |
|-----------|--------|-------|
| **FTS** | ✅ WORKING | BM25 full-text search on artifacts |
| **VSS** | 🔜 PLANNED | Vector semantic search |
| **GraphRAG** | 🔜 PLANNED | Entity/relation graph |
| **RRF** | 🔜 BLOCKED | Needs VSS + GraphRAG first |

---

## Purpose

This memory bank enables AI agents to query the complete HFO Evolution Timeline (Pre-HFO through Gen 84). Use it for:
- Answering questions about HFO concepts
- Finding relevant documents by keyword or topic
- Understanding the evolution of ideas across generations
- Citing sources accurately

---

## 🚨 Critical Rules

1. **NEVER hallucinate content** — If you can't find it, say so
2. **ALWAYS cite sources** — Include generation number and filename
3. **PREFER exact matches** — Use FTS before guessing
4. **RESPECT generation boundaries** — Don't mix content from different gens

---

## How to Query

### FTS Search (Working Now)

```python
import duckdb

con = duckdb.connect('hfo_memory.duckdb', read_only=True)
con.execute('LOAD fts')

# Search for a concept
query = 'obsidian spider'
results = con.execute(f"""
    SELECT filename, generation, era, content,
           fts_main_artifacts.match_bm25(id, '{query}') as score
    FROM artifacts 
    WHERE score IS NOT NULL
    ORDER BY score DESC
    LIMIT 10
""").fetchall()

for filename, gen, era, content, score in results:
    print(f"Gen {gen} ({era}): {filename} [score: {score:.2f}]")
```

### Get Full Content

```python
# Get specific file content
result = con.execute("""
    SELECT content FROM artifacts 
    WHERE filename LIKE '%HANDOFF%' AND generation = 72
    LIMIT 1
""").fetchone()

if result:
    print(result[0])
```

### Browse by Generation

```python
# List all files in a generation
for row in con.execute("""
    SELECT filename FROM artifacts 
    WHERE generation = 55
    ORDER BY filename
""").fetchall():
    print(row[0])
```

---

## Key File Patterns

| Pattern | What It Contains |
|---------|------------------|
| `HANDOFF*.md` | Generation transition documents |
| `*QUINE*.md` | Self-describing system docs |
| `*GEM*.md` | Core knowledge crystallization |
| `*BATON*.md` | Knowledge transfer docs |
| `*BLACKBOARD*.jsonl` | Stigmergy/state storage |
| `card_*.md` | Grimoire cards (archetypes) |
| `design_*.md` | Design documents |
| `ttao*.md` | User's raw notes |

---

## Anti-Hallucination Protocol

When asked about HFO content:

1. **First**: Search FTS for exact terms
2. **Second**: Check if generation exists (1-84 for HFO)
3. **Third**: Read actual content before summarizing
4. **Fourth**: If not found, say "Not found" — don't guess

**Citation format:**
```
Source: Gen 72, HANDOFF_GEN_72.md
```

---

## Example Queries

### "What is the Obsidian Spider?"
```python
# Search for obsidian spider
results = con.execute("""
    SELECT filename, generation, content,
           fts_main_artifacts.match_bm25(id, 'obsidian spider') as score
    FROM artifacts WHERE score IS NOT NULL
    ORDER BY score DESC LIMIT 5
""").fetchall()
```

### "Show me Gen 55 design docs"
```python
results = con.execute("""
    SELECT filename, content FROM artifacts
    WHERE generation = 55 AND filename LIKE 'design_%'
""").fetchall()
```

### "Find all HANDOFF files"
```python
results = con.execute("""
    SELECT filename, generation FROM artifacts
    WHERE lower(filename) LIKE '%handoff%'
    ORDER BY generation
""").fetchall()
```

---

## Database Stats

- **Total Artifacts:** 6,423
- **Eras:** hfo, hope, tectangle, spatial
- **Generations:** Pre-HFO + Gen 1-84
- **Content Types:** .md, .txt, .jsonl

---

## Do NOT

- ❌ Make up content that doesn't exist
- ❌ Confuse generations (Gen 55 ≠ Gen 72)
- ❌ Assume content exists without searching
- ❌ Summarize without citing source file
- ❌ Mix pre-HFO eras with HFO generations

# Design Document: HFO Silver Data Lake

## Overview

This design transforms the Gen 76 bronze DuckDB (26.79 GB, 70 tables) into a clean silver layer by deduplicating tables, normalizing schemas, and preparing for downstream exports to Parquet, LanceDB, and GraphRAG. The silver layer serves as the validated, query-optimized foundation for all HFO knowledge products.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BRONZE LAYER (INPUT)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  data_lake/bronze/hfo_gen76_consolidated.duckdb                             │
│  ├── Size: 26.79 GB                                                         │
│  ├── Tables: 70 (with duplicates)                                           │
│  ├── Rows: 1,368,454                                                        │
│  └── Prefixes: consol_*, gen72_*, gen73_*, gen76_*, safe_*, safe_hist_*    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRANSFORMATION PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Bronze Expansion                                                        │
│     ├── Ingest HFO_buds/generation_72-76 markdown files                    │
│     ├── Ingest Grimoire cards (Gen 73-76)                                  │
│     └── Ingest deep dive files                                             │
│                                                                             │
│  2. Table Deduplication                                                     │
│     ├── Group by base name (strip prefixes)                                │
│     ├── UNION DISTINCT across duplicate groups                             │
│     └── 70 tables → 41 unique tables                                       │
│                                                                             │
│  3. Schema Normalization                                                    │
│     ├── Add source_table column (provenance)                               │
│     ├── Add dedup_hash column (MD5)                                        │
│     └── Normalize timestamps to ISO 8601                                   │
│                                                                             │
│  4. Validation                                                              │
│     ├── NULL checks on primary keys                                        │
│     ├── Referential integrity                                              │
│     └── Row count verification                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SILVER LAYER (OUTPUT)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  data_lake/silver/hfo_gen76_clean.duckdb                                    │
│  ├── Target Size: <15 GB (44% reduction)                                   │
│  ├── Tables: ~41 (deduplicated)                                            │
│  ├── Rows: ~800K (after dedup)                                             │
│  └── Domains: knowledge, artifacts, holons, relationships, blackboards     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │  Parquet  │   │  LanceDB  │   │ GraphRAG  │
            │  Export   │   │  Vectors  │   │   Graph   │
            └───────────┘   └───────────┘   └───────────┘
```

## Components and Interfaces

### 1. Bronze Expander

**Purpose**: Ingest additional HFO sources into bronze before deduplication

**Input Sources**:
- `HFO_buds/generation_72/` through `generation_76/` - All markdown files
- `HFO_buds/generation_*/hfo_grimoire/` - Grimoire card files
- `generation_1_to_generation_72_backup_*/HFO_*_DEEP_DIVE.md` - Deep dive files

**Output Tables**:
- `gen76_hfo_buds_files` - All markdown files from HFO_buds
- `gen76_grimoire_cards` - Grimoire cards with deck/card metadata
- `gen76_deep_dives` - Monthly deep dive summaries

### 2. Table Deduplicator

**Purpose**: Merge duplicate tables into single canonical tables

**Deduplication Groups** (20 groups identified):
| Base Name | Copies | Total Rows | Unique Rows | Reduction |
|:----------|:------:|:----------:|:-----------:|:---------:|
| knowledge_files | 3 | 216,315 | 72,105 | 67% |
| unified_holons | 3 | 102,216 | 34,072 | 67% |
| unified_archive_index | 2 | 539,296 | 269,648 | 50% |
| unified_git_file_history | 2 | 81,484 | 40,742 | 50% |
| unified_memories | 2 | 40,688 | 20,344 | 50% |
| ... | ... | ... | ... | ... |

**Algorithm**:
```sql
-- For each duplicate group
CREATE TABLE silver.{base_name} AS
SELECT DISTINCT *, '{source_table}' as source_table
FROM (
    SELECT * FROM consol_{base_name}
    UNION ALL
    SELECT * FROM gen72_{base_name}
    UNION ALL
    SELECT * FROM safe_{base_name}
);
```

### 3. Schema Normalizer

**Purpose**: Add provenance and deduplication columns

**Added Columns**:
| Column | Type | Purpose |
|:-------|:-----|:--------|
| `source_table` | TEXT | Original table name for provenance |
| `dedup_hash` | TEXT | MD5 hash of key columns for incremental updates |
| `normalized_at` | TIMESTAMP | When normalization occurred |

**Timestamp Normalization**:
- Convert all timestamp columns to ISO 8601 format
- Handle NULL timestamps gracefully
- Preserve timezone information where available

### 4. Validator

**Purpose**: Ensure data quality before silver layer finalization

**Validation Checks**:
1. **NULL Check**: Primary key columns must not contain NULL
2. **Referential Integrity**: Foreign keys must reference existing entities
3. **Row Count**: Actual counts must match expected deduplication ratios (±5%)
4. **Schema Consistency**: All tables must have required columns

### 5. Export Preparer

**Purpose**: Organize silver data for downstream consumption

**Domain Organization**:
| Domain | Tables | Export Format |
|:-------|:-------|:--------------|
| knowledge | knowledge_files, knowledge_blobs | Parquet |
| artifacts | unified_artifacts, level*_artifacts | Parquet |
| holons | unified_holons, gen53_holons | LanceDB (embeddings) |
| relationships | unified_relationships, edges | GraphRAG |
| blackboards | gen76_blackboards | Parquet + LanceDB |
| grimoire | gen76_grimoire_cards | Parquet |

## Data Models

### Silver Table Schema (Common Columns)

```sql
CREATE TABLE silver.{table_name} (
    -- Original columns from bronze
    ...

    -- Added by normalization
    source_table TEXT NOT NULL,           -- Provenance tracking
    dedup_hash TEXT NOT NULL,             -- MD5 of key columns
    normalized_at TIMESTAMP DEFAULT NOW() -- Normalization timestamp
);
```

### Deduplication Manifest

```sql
CREATE TABLE silver_dedup_manifest (
    id INTEGER PRIMARY KEY,
    base_name TEXT NOT NULL,
    source_tables TEXT[] NOT NULL,        -- Array of source table names
    source_row_count INTEGER NOT NULL,    -- Total rows before dedup
    target_row_count INTEGER NOT NULL,    -- Rows after dedup
    reduction_pct FLOAT NOT NULL,         -- Percentage reduction
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Export Manifest

```sql
CREATE TABLE silver_export_manifest (
    id INTEGER PRIMARY KEY,
    table_name TEXT NOT NULL,
    domain TEXT NOT NULL,                 -- knowledge, artifacts, holons, etc.
    export_format TEXT NOT NULL,          -- parquet, lancedb, graphrag
    text_columns TEXT[],                  -- Columns for LanceDB embedding
    entity_type TEXT,                     -- For GraphRAG: entity or relationship
    row_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Validation Errors

```sql
CREATE TABLE silver_validation_errors (
    id INTEGER PRIMARY KEY,
    table_name TEXT NOT NULL,
    validation_type TEXT NOT NULL,        -- null_check, referential, row_count
    error_message TEXT NOT NULL,
    affected_rows INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: File Ingestion Completeness
*For any* markdown file in `HFO_buds/generation_72` through `generation_76`, the file should exist as a row in `gen76_hfo_buds_files` with non-null path, content, and file_size columns.
**Validates: Requirements 1.1, 1.4**

### Property 2: Deduplication Union Completeness
*For any* duplicate table group, the silver table should contain exactly the UNION DISTINCT of all source tables - no rows lost, no extra rows added.
**Validates: Requirements 2.2, 2.3**

### Property 3: Deduplication Reduction Ratio
*For any* duplicate table group with 3 copies, the row reduction should be between 60-70%. For groups with 2 copies, reduction should be between 45-55%.
**Validates: Requirements 2.4**

### Property 4: Schema Completeness
*For any* silver table, the columns `source_table` and `dedup_hash` should exist and contain no NULL values.
**Validates: Requirements 3.1, 3.2**

### Property 5: Timestamp Format Consistency
*For any* timestamp column in silver tables, all non-null values should match ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
**Validates: Requirements 3.3**

### Property 6: Silver Table Naming
*For any* table in the silver database, the table name should not contain prefixes `consol_`, `gen72_`, `safe_`, or `safe_hist_`.
**Validates: Requirements 4.2**

### Property 7: Primary Key Integrity
*For any* silver table with a defined primary key, no NULL values should exist in primary key columns.
**Validates: Requirements 6.1**

### Property 8: Referential Integrity
*For any* relationship row referencing an entity, the referenced entity should exist in the corresponding entity table.
**Validates: Requirements 6.2**

### Property 9: Incremental Deduplication
*For any* record added via incremental update, if its `dedup_hash` already exists in the table, the record should not be inserted (no duplicates created).
**Validates: Requirements 7.1, 7.2**

### Property 10: Timestamp Preservation
*For any* existing record during incremental update, the `normalized_at` timestamp should not change.
**Validates: Requirements 7.3**

## Error Handling

| Error | Handling |
|:------|:---------|
| Source table missing | Log warning, skip table, continue processing |
| Schema mismatch during UNION | Cast to widest compatible type, log warning |
| NULL in primary key | Log to validation_errors, exclude row from silver |
| Referential integrity violation | Log to validation_errors, include row with warning flag |
| Disk space insufficient | Fail with clear message, suggest cleanup |

## Testing Strategy

### Property-Based Testing

**Library**: Hypothesis (Python)

**Properties to test**:
1. File ingestion completeness (Property 1)
2. Deduplication union completeness (Property 2)
3. Schema completeness (Property 4)
4. Silver table naming (Property 6)
5. Primary key integrity (Property 7)
6. Incremental deduplication (Property 9)

### Unit Tests

1. Prefix stripping function (extract base name from table name)
2. MD5 hash generation for dedup_hash
3. Timestamp normalization to ISO 8601
4. Domain classification for export manifest

### Integration Tests

1. Full bronze expansion pipeline
2. Full deduplication pipeline
3. Silver database creation end-to-end
4. Incremental update with new data

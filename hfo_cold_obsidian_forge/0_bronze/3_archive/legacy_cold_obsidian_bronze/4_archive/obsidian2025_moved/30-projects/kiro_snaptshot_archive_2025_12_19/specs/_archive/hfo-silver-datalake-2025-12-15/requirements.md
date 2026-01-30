# Requirements Document
> Last Updated: 2025-12-15T16:35:00Z
> Status: ✅ REQUIREMENTS VALID - Implementation failed due to wrong deduplication logic

## Introduction

This specification defines the Silver Data Lake layer for HFO Gen 76. The silver layer transforms the raw bronze DuckDB (26.79 GB, 70 tables with duplicates) into a clean, deduplicated database optimized for downstream consumption by Parquet exports, LanceDB vector stores, and GraphRAG knowledge graphs.

## Glossary

- **Bronze Layer**: Raw ingested data with duplicates from multiple sources (Gen 1-72 backup, Safe_Data, Gen 73-76)
- **Silver Layer**: Cleaned, deduplicated, validated data with consistent schemas
- **Gold Layer**: Query-optimized data products (Parquet, LanceDB, GraphRAG)
- **DuckDB**: Columnar analytical database used for data lake storage
- **Parquet**: Columnar file format for efficient analytics
- **LanceDB**: Vector database for semantic search and embeddings
- **GraphRAG**: Graph-based retrieval augmented generation for knowledge graphs
- **SSOT**: Single Source of Truth
- **Deduplication**: Process of removing duplicate records while preserving unique data

## Requirements

### Requirement 1: Bronze Layer Expansion

**User Story:** As a data engineer, I want to expand the bronze layer with additional HFO sources, so that all historical knowledge is captured before deduplication.

#### Acceptance Criteria

1. WHEN the bronze expansion runs THEN the System SHALL ingest all markdown files from `HFO_buds/generation_72` through `generation_76`
2. WHEN the bronze expansion runs THEN the System SHALL ingest all Grimoire cards from Gen 73-76 into a `gen76_grimoire_cards` table
3. WHEN the bronze expansion runs THEN the System SHALL ingest all deep dive markdown files into a `gen76_deep_dives` table
4. WHEN ingesting files THEN the System SHALL store file path, content, file size, and ingestion timestamp
5. WHEN the bronze expansion completes THEN the System SHALL log the total files ingested and bytes processed

### Requirement 2: Table Deduplication

**User Story:** As a data engineer, I want to deduplicate the 70 bronze tables into ~41 unique tables, so that the silver layer has no redundant data.

#### Acceptance Criteria

1. WHEN deduplicating tables THEN the System SHALL identify tables with common base names (stripping `consol_`, `gen72_`, `safe_`, `safe_hist_` prefixes)
2. WHEN multiple tables share a base name THEN the System SHALL merge them using UNION DISTINCT
3. WHEN merging tables THEN the System SHALL preserve all unique rows across sources
4. WHEN deduplication completes THEN the System SHALL reduce row count by 50-67% for duplicate groups
5. WHEN deduplication completes THEN the System SHALL create a `silver_dedup_manifest` table logging source tables, target table, and row counts

### Requirement 3: Schema Normalization

**User Story:** As a data engineer, I want consistent schemas across silver tables, so that downstream consumers have predictable data structures.

#### Acceptance Criteria

1. WHEN normalizing schemas THEN the System SHALL add `source_table` column to track data provenance
2. WHEN normalizing schemas THEN the System SHALL add `dedup_hash` column using MD5 of key columns for future deduplication
3. WHEN normalizing schemas THEN the System SHALL convert all timestamp columns to ISO 8601 format
4. WHEN schema conflicts exist THEN the System SHALL use the widest compatible type (e.g., TEXT over VARCHAR)

### Requirement 4: Silver Database Creation

**User Story:** As a data engineer, I want a separate silver DuckDB file, so that bronze and silver layers are independently queryable.

#### Acceptance Criteria

1. WHEN creating silver database THEN the System SHALL write to `data_lake/silver/hfo_gen76_clean.duckdb`
2. WHEN creating silver database THEN the System SHALL include only deduplicated tables (no `consol_`, `gen72_`, `safe_` prefixes)
3. WHEN creating silver database THEN the System SHALL create indexes on frequently queried columns
4. WHEN silver creation completes THEN the System SHALL be smaller than bronze (target: <15 GB from 26.79 GB)

### Requirement 5: Export Readiness

**User Story:** As a data engineer, I want the silver layer optimized for Parquet, LanceDB, and GraphRAG exports, so that downstream pipelines can consume it efficiently.

#### Acceptance Criteria

1. WHEN preparing for Parquet export THEN the System SHALL organize tables by domain (knowledge, artifacts, holons, relationships, blackboards)
2. WHEN preparing for LanceDB export THEN the System SHALL identify text columns suitable for embedding (content, description, observations)
3. WHEN preparing for GraphRAG export THEN the System SHALL identify entity tables (holons, artifacts) and relationship tables (relationships, edges)
4. WHEN export preparation completes THEN the System SHALL create a `silver_export_manifest` table with export metadata

### Requirement 6: Data Validation

**User Story:** As a data engineer, I want validation checks on the silver layer, so that data quality issues are caught before downstream consumption.

#### Acceptance Criteria

1. WHEN validating silver data THEN the System SHALL verify no NULL values in primary key columns
2. WHEN validating silver data THEN the System SHALL verify referential integrity between entity and relationship tables
3. WHEN validating silver data THEN the System SHALL verify row counts match expected deduplication ratios
4. IF validation fails THEN the System SHALL log errors to `silver_validation_errors` table and continue processing

### Requirement 7: Incremental Updates

**User Story:** As a data engineer, I want the silver layer to support incremental updates, so that future generations can be added without full rebuilds.

#### Acceptance Criteria

1. WHEN adding new data THEN the System SHALL use `dedup_hash` to identify existing records
2. WHEN adding new data THEN the System SHALL INSERT only records with new hashes
3. WHEN updating existing records THEN the System SHALL preserve the original `ingested_at` timestamp
4. WHEN incremental update completes THEN the System SHALL log new rows added and duplicates skipped

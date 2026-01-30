# Implementation Plan

## Phase 1: Bronze Layer Expansion

- [x] 1. Expand Bronze with HFO_buds Files



  - [x] 1.1 Create gen76_hfo_buds_files table

    - Schema: id, file_path, generation, content, file_size_kb, ingested_at
    - _Requirements: 1.1, 1.4_

  - [ ] 1.2 Ingest markdown files from HFO_buds/generation_72 through generation_76
    - Recursively scan all .md files
    - Store path, content, size, timestamp

    - _Requirements: 1.1_
  - [ ] 1.3 Write property test for file ingestion completeness
    - **Property 1: File Ingestion Completeness**
    - **Validates: Requirements 1.1, 1.4**



- [ ] 2. Ingest Grimoire Cards
  - [x] 2.1 Create gen76_grimoire_cards table

    - Schema: id, file_path, generation, deck_num, card_num, role, greek, content, file_size_kb, ingested_at
    - _Requirements: 1.2_

  - [ ] 2.2 Parse Grimoire card metadata from file paths
    - Extract deck number, card number, role, greek question from path/filename

    - _Requirements: 1.2_
  - [x] 2.3 Ingest all Grimoire cards from Gen 73-76

    - Scan HFO_buds/generation_*/hfo_grimoire/
    - _Requirements: 1.2_



- [ ] 3. Ingest Deep Dive Files
  - [ ] 3.1 Create gen76_deep_dives table
    - Schema: id, file_path, month, year, content, file_size_kb, ingested_at
    - _Requirements: 1.3_



  - [ ] 3.2 Ingest all HFO_*_DEEP_DIVE.md files
    - Parse month/year from filename
    - _Requirements: 1.3_


- [x] 4. Checkpoint - Bronze Expansion Complete

  - Verify gen76_hfo_buds_files, gen76_grimoire_cards, gen76_deep_dives tables exist

  - Log total files ingested and bytes processed

  - Ensure all tests pass, ask the user if questions arise.


## Phase 2: Table Deduplication

- [ ] 5. Analyze Duplicate Table Groups
  - [ ] 5.1 Create deduplication analysis script
    - Group tables by base name (strip consol_, gen72_, safe_, safe_hist_ prefixes)
    - Calculate row counts per group
    - _Requirements: 2.1_
  - [ ] 5.2 Generate deduplication plan
    - List all 20 duplicate groups with source tables and expected reduction
    - _Requirements: 2.1_

- [ ] 6. Create Silver Database Structure
  - [ ] 6.1 Create data_lake/silver/ directory
    - _Requirements: 4.1_
  - [ ] 6.2 Initialize hfo_gen76_clean.duckdb
    - Create empty database with metadata tables
    - _Requirements: 4.1_

- [ ] 7. Deduplicate Knowledge Tables
  - [ ] 7.1 Merge knowledge_files (3 copies → 1)
    - UNION DISTINCT from consol_, gen72_, safe_ prefixed tables
    - Add source_table column
    - _Requirements: 2.2, 2.3, 3.1_
  - [ ] 7.2 Merge knowledge_blobs (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 7.3 Write property test for deduplication union completeness
    - **Property 2: Deduplication Union Completeness**
    - **Validates: Requirements 2.2, 2.3**

- [ ] 8. Deduplicate Unified Tables
  - [ ] 8.1 Merge unified_holons (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 8.2 Merge unified_artifacts (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 8.3 Merge unified_relationships (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [x] 8.4 Merge unified_archive_index (2 copies → 1)


    - _Requirements: 2.2, 2.3_
  - [ ] 8.5 Merge unified_git_file_history (2 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 8.6 Merge unified_memories (2 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 8.7 Write property test for deduplication reduction ratio
    - **Property 3: Deduplication Reduction Ratio**
    - **Validates: Requirements 2.4**

- [ ] 9. Deduplicate Gen59 Tables
  - [ ] 9.1 Merge gen59_level0_artifacts (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 9.2 Merge gen59_level1_artifacts (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 9.3 Merge gen59_level2_artifacts (3 copies → 1)
    - _Requirements: 2.2, 2.3_
  - [ ] 9.4 Merge gen59_memory_items (3 copies → 1)
    - _Requirements: 2.2, 2.3_

- [ ] 10. Copy Non-Duplicate Tables
  - [ ] 10.1 Copy gen73_nodes to silver
    - _Requirements: 4.2_
  - [ ] 10.2 Copy gen73_edges to silver
    - _Requirements: 4.2_
  - [ ] 10.3 Copy gen76_blackboards to silver
    - _Requirements: 4.2_
  - [ ] 10.4 Copy gen76_obsidian_roles to silver
    - _Requirements: 4.2_
  - [ ] 10.5 Copy safe_hist_gen53_* tables to silver (rename without prefix)
    - _Requirements: 4.2_
  - [ ] 10.6 Write property test for silver table naming
    - **Property 6: Silver Table Naming**
    - **Validates: Requirements 4.2**

- [x] 11. Create Deduplication Manifest

  - [x] 11.1 Create silver_dedup_manifest table

    - Record source tables, row counts, reduction percentages
    - _Requirements: 2.5_


- [ ] 12. Checkpoint - Deduplication Complete
  - Verify ~41 tables in silver database
  - Verify row reduction matches expected ratios
  - Ensure all tests pass, ask the user if questions arise.

## Phase 3: Schema Normalization

- [ ] 13. Add Provenance Columns
  - [ ] 13.1 Add source_table column to all silver tables
    - _Requirements: 3.1_
  - [ ] 13.2 Add dedup_hash column using MD5 of key columns
    - Identify key columns per table
    - Generate MD5 hash
    - _Requirements: 3.2_
  - [ ] 13.3 Write property test for schema completeness
    - **Property 4: Schema Completeness**
    - **Validates: Requirements 3.1, 3.2**

- [ ] 14. Normalize Timestamps
  - [ ] 14.1 Identify all timestamp columns across silver tables
    - _Requirements: 3.3_
  - [ ] 14.2 Convert timestamps to ISO 8601 format
    - Handle various input formats
    - Preserve NULL values
    - _Requirements: 3.3_
  - [ ] 14.3 Write property test for timestamp format consistency
    - **Property 5: Timestamp Format Consistency**
    - **Validates: Requirements 3.3**

- [ ] 15. Create Indexes
  - [ ] 15.1 Create indexes on primary key columns
    - _Requirements: 4.3_
  - [ ] 15.2 Create indexes on frequently queried columns (file_path, generation, dedup_hash)
    - _Requirements: 4.3_

- [ ] 16. Checkpoint - Schema Normalization Complete
  - Verify all tables have source_table and dedup_hash columns
  - Verify timestamps are ISO 8601 format
  - Ensure all tests pass, ask the user if questions arise.

## Phase 4: Data Validation

- [ ] 17. Validate Primary Keys
  - [ ] 17.1 Check for NULL values in primary key columns
    - Log errors to silver_validation_errors
    - _Requirements: 6.1_
  - [ ] 17.2 Write property test for primary key integrity
    - **Property 7: Primary Key Integrity**
    - **Validates: Requirements 6.1**

- [ ] 18. Validate Referential Integrity
  - [ ] 18.1 Check relationships reference existing entities
    - Verify unified_relationships → unified_holons
    - Verify gen73_edges → gen73_nodes
    - _Requirements: 6.2_
  - [ ] 18.2 Write property test for referential integrity
    - **Property 8: Referential Integrity**
    - **Validates: Requirements 6.2**

- [ ] 19. Validate Row Counts
  - [ ] 19.1 Compare actual vs expected row counts from dedup manifest
    - Allow ±5% tolerance
    - _Requirements: 6.3_

- [ ] 20. Create Validation Report
  - [ ] 20.1 Create silver_validation_errors table if not exists
    - _Requirements: 6.4_
  - [ ] 20.2 Generate validation summary
    - Total tables validated, errors found, warnings
    - _Requirements: 6.4_

- [ ] 21. Checkpoint - Validation Complete
  - Review validation errors
  - Ensure all tests pass, ask the user if questions arise.

## Phase 5: Export Preparation

- [ ] 22. Organize Tables by Domain
  - [ ] 22.1 Classify tables into domains
    - knowledge: knowledge_files, knowledge_blobs
    - artifacts: unified_artifacts, gen59_level*_artifacts
    - holons: unified_holons, gen53_holons
    - relationships: unified_relationships, gen73_edges
    - blackboards: gen76_blackboards
    - grimoire: gen76_grimoire_cards
    - _Requirements: 5.1_

- [ ] 23. Create Export Manifest
  - [ ] 23.1 Create silver_export_manifest table
    - _Requirements: 5.4_
  - [ ] 23.2 Identify text columns for LanceDB embedding
    - content, description, observations columns
    - _Requirements: 5.2_
  - [ ] 23.3 Identify entity and relationship tables for GraphRAG
    - Entity: holons, artifacts, nodes
    - Relationship: relationships, edges
    - _Requirements: 5.3_

- [ ] 24. Verify Silver Database Size
  - [ ] 24.1 Check silver database file size
    - Target: <15 GB (from 26.79 GB bronze)
    - _Requirements: 4.4_

- [ ] 25. Checkpoint - Export Preparation Complete
  - Verify export manifest is complete
  - Verify silver database size meets target
  - Ensure all tests pass, ask the user if questions arise.

## Phase 6: Incremental Update Support

- [ ] 26. Implement Incremental Update Logic
  - [ ] 26.1 Create upsert function using dedup_hash
    - Check if hash exists before insert
    - _Requirements: 7.1, 7.2_
  - [ ] 26.2 Preserve original timestamps on update
    - _Requirements: 7.3_
  - [ ] 26.3 Write property test for incremental deduplication
    - **Property 9: Incremental Deduplication**
    - **Validates: Requirements 7.1, 7.2**
  - [ ] 26.4 Write property test for timestamp preservation
    - **Property 10: Timestamp Preservation**
    - **Validates: Requirements 7.3**

- [ ] 27. Create Incremental Update Logging
  - [ ] 27.1 Log new rows added and duplicates skipped
    - _Requirements: 7.4_

- [ ] 28. Final Checkpoint - Silver Data Lake Complete
  - Ensure all tests pass, ask the user if questions arise.
  - Update MANIFEST.md with silver layer status
  - Log completion to ObsidianBlackboard.jsonl

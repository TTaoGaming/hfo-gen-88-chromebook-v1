# Medallion: Bronze | Mutation: 0% | HIVE: V

# DuckDB Roll-up Strategy: Unified Archive & Active Memory

## 1. Current State Assessment
- **Active Data (`active/`):** ~12 GB
- **Archive Data (`_archive_dev_2026_1_14/`):** ~60 GB
- **Total Footprint:** ~72 GB
- **Primary File Types:** Python (`.py`), JavaScript (`.js`), TypeScript (`.ts`), Markdown (`.md`), and JSON.
- **Redundancy High-Risk:** Massive presence of `.py`, `.js`, and `.ts` files suggest multiple clones/versions of repositories, dependency folders (`node_modules`, `.venv`), and build artifacts.

## 2. DuckDB Advantages
DuckDB is ideal for this roll-up for three reasons:
1.  **Columnar Compression:** Specifically optimized for repetitive text (like source code).
2.  **In-process Speed:** No server overhead; ideal for local forensic analysis.
3.  **Built-in FTS:** The `fts` extension allows full-text indexing of the entire 72GB dataset with minimal overhead compared to standard databases.

---

## 3. Hardware Constraint Analysis (Crucial)
*   **CPU:** 8 Cores (Intel Core i3-N305) - *Adequate for parallel hashing.*
*   **RAM:** 6.3 GiB Total (~1.5 GiB Available) - **CRITICAL LIMIT.** 
    *   *Impact:* We cannot load the entire dataset into memory. DuckDB must be configured to use `memory_limit` and spill to disk.
*   **Disk Space:** 36 GB Available.
    *   *Impact:* Since the source is 72 GB, we **cannot** keep both the original folders and the 1:1 DuckDB on the same disk unless heavy deduplication is achieved during the streaming ingest.

## 4. The Ingestion Process (Step-by-Step)

To handle the "stale" databases and JSONL files alongside the raw filesystem, we will follow this pipeline:

### Step 1: Initialize the "Global Hive" DuckDB
Create the base file with optimized settings:
```sql
SET memory_limit = '1GB'; -- Match our 1.5GB RAM constraint
INSTALL sqlite; LOAD sqlite; -- For ingesting your .db files
```

### Step 2: Ingest Legacy Databases (SQLite)
Instead of manual export/import, we attach the old DBs and pull them into the new schema:
```sql
ATTACH 'path/to/hfo_memory.db' AS legacy_db (TYPE SQLITE);
INSERT INTO blobs (hash, content, metadata)
SELECT sha256(content), content, JSON_OBJECT('source', 'legacy_db', 'table', 'memory') 
FROM legacy_db.memory_table;
DETACH legacy_db;
```

### Step 3: Ingest JSONL Streams
DuckDB handles JSONL natively and extremely fast:
```sql
INSERT INTO blobs (hash, content, metadata)
SELECT sha256(line), line, JSON_OBJECT('origin', 'blackboard_jsonl')
FROM read_csv_auto('**/*.jsonl', columns={'line': 'TEXT'});
```

### Step 4: Content-Addressed File System Scan
Run a Python worker that:
1. Walks `active/` and `_archive/`.
2. Computes SHA-256 of every file.
3. Checks if SHA exists in DuckDB.
4. If MISSING: Ingests content + path.
5. If EXISTS: Only records the new path pointing to the existing hash.

### Step 5: Metadata "Freshness" & Priority Tagging
Every record will carry a `freshness_score` (1-20) calculated as follows:
- **Base Score:** `active/` = 10, `_archive/` = 1-5.
- **Priority Keywords (Total +5 to +10):**
    - `quine`, `gem`, `seed`: +5 priority boost.
    - `galoise lattice`, `grimoire`: +10 priority boost (high value archetypes).
- **Recency Decay:** Older files in archive lose 1 point per 6 months of age.

### Step 6: Final Verification & Pruning
Once the total unique blob size is confirmed and FTS is tested, we can safely archive or delete the duplicate source folders to reclaim the 72GB.

## 5. Recommended Options

### Option A: Content-Addressed "Universal Blob" (Recommended)
This approach prioritizes deduplication. Even if a file exists in 10 different folders, it is stored only once in the `blobs` table.

**Schema:**
- `blobs`: `hash (PK)`, `content (TEXT)`, `size (INT)`, `is_compressed (BOOL)`
- `file_system`: `path (PK)`, `content_hash (FK)`, `created_at`, `modified_at`, `source (active/archive)`

**Pros:**
- **Maximum Deduplication:** Files with identical content (even with different names) are stored only once.
- **Data Integrity:** Hashes ensure content hasn't changed.
- **FTS Optimization:** You only index the `blobs` table, making the search index much smaller.

### Option B: Unified Flat Archive
A simpler "one table to rule them all" approach.

**Schema:**
- `archive`: `path`, `content`, `extension`, `size`, `created_at`, `source`

**Pros:**
- **Simplicity:** Easier to write queries (no joins).
- **Fast Ingestion:** Standard `COPY` operations work directly.

---

## 4. Technical Strategy for Implementation

### A. Deduplication logic
Use SHA-256 for the content hash. During ingestion:
```sql
-- Insert only new unique content
INSERT INTO blobs (hash, content, size)
SELECT hash, content, size FROM incoming_files
WHERE hash NOT IN (SELECT hash FROM blobs);
```

### B. Compression Optimization
For the `content` column, use **ZSTD** compression which is highly effective for source code and markdown text. 
```sql
ALTER TABLE blobs ALTER content SET STORAGE 'ZSTD';
```

### C. Full-Text Search (FTS)
Initialize the index for all captured text:
```sql
PRAGMA create_fts_index('blobs', 'hash', 'content');
-- Search query example:
SELECT content FROM blobs WHERE fts_main_blobs.match(content, 'your search term');
```

## 7. RAM Optimization for Multiple AI Agents
Since you are running 2-3 agents simultaneously on a 6.3GB Chromebook, we need to minimize the "AI Overhead":

1.  **Shared DuckDB Instance:** Do not open separate DuckDB connections in different agent terminals. Each persistent connection reserves its own memory buffer. Use one "Master Ingest" process.
2.  **Sequential Ingestion:** Instead of all agents scanning the disk at once (which spikes I/O and CPU cache usage), have agents "pass the baton" or work on separate sub-directories sequentially.
3.  **Process Pruning:**
    - Use `Shift + Esc` in Chrome to kill the GPU process or background tabs if you don't need them; this is the #1 RAM hog on Chromebooks.
    - Inside Linux, run `htop` and look for zombie `python` or `node` processes from previous agent crashes.
4.  **ZRAM Monitoring:** ChromeOS uses ZRAM (compressed RAM swap). You can check its efficiency in the terminal: `zramctl`. If the compression ratio is low, clearing large text-heavy buffers helps.
5.  **DuckDB Spilling:** Ensure the `temp_directory` is set to the disk (not `/dev/shm` or RAM-backed folders) to ensure that when memory hits 1GB, it overflows to your 36GB free disk space instead of crashing the container.


## 9. "Full Throttle" Optimization (Max Speed)
To ingestion at maximum velocity, we will configure the system for absolute hardware saturation:

1.  **RAM Saturation:** Increase `memory_limit` to `4GB` (leaving ~2GB for Linux/OS/VS Code overhead).
2.  **CPU Parallelism:** Use all **8 Cores** via Python `concurrent.futures`. We will hash files in parallel and then perform a single-threaded "Batched Insert" into DuckDB to prevent lock contention.
3.  **I/O Optimization:** 
    - Set `preserve_insertion_order = false` to allow DuckDB to reorganize data for maximum compression on the fly.
    - Set `checkpoint_threshold = '2GB'` to reduce the frequency of disk synchronization.
4.  **Batch Processing:** We will group files into "Swarms" of 5,000 files to minimize the overhead of intermediate commits.
5.  **Direct Hash Comparison:** Use a temporary DuckDB table to store the hashes of the current run, then a single `INSERT INTO ... SELECT ... WHERE hash NOT IN ...` to deduplicate against the master archive in one atomic operation.

## 10. Final Ingestion Estimates & Setup
*   **Exclusion List:** Created at [`.hfo_ignore`](/home/tommytai3/.hfo_ignore). 
    *   *Saves:* ~12-15 GB by skipping `node_modules`, `.venv`, and `.git` binaries.
*   **Total Projected DB Size:** **18-22 GB** (approx. 70% compression/dedupe ratio).
*   **Time Estimate:** **45-60 Minutes**.
*   **MCP Server:** Initialized at [hfo_duckdb_mcp.py](hfo_duckdb_mcp.py) and registered in VS Code.

---
*Created on 2026-01-15 for HFO Gen 88 Coordination.*

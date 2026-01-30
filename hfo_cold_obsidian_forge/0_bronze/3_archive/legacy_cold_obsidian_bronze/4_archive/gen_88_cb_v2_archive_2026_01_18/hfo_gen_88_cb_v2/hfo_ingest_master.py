# Medallion: Bronze | Mutation: 0% | HIVE: I
import os
import hashlib
import duckdb
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# --- CONFIGURATION ---
DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
# Gen 88 Primary scope for ACTIVE status
GEN_88_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
ROOT_PATHS = [GEN_88_ROOT] 
LEGACY_PATHS = ["/home/tommytai3/_archive_dev_2026_1_14", "/home/tommytai3/active"]
IGNORE_FILE = "/home/tommytai3/.hfo_ignore"
BATCH_SIZE = 500
THREADS = 4
MEMORY_LIMIT = "512MB"

PRIORITY_KEYWORDS = {
    "hyper-sliver": 15,
    "aristocrat": 15,
    "grimoire": 10,
    "galoise lattice": 10,
    "octal": 10,
    "shard": 10,
    "quine": 5,
    "gem": 5,
    "seed": 5
}

def load_ignore_patterns():
    if not os.path.exists(IGNORE_FILE):
        return set()
    with open(IGNORE_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip() and not line.startswith('#'))

def calculate_hash_and_meta(file_path):
    """Worker function to process a single file. Only called if file is changed or new."""
    try:
        path_obj = Path(file_path)
        stat = path_obj.stat()
        size = stat.st_size
        mtime = stat.st_mtime
        
        # Freshness Score Calculation
        base_score = 10 if "active/" in file_path else 1
        age_months = (time.time() - mtime) / (30 * 24 * 3600)
        recency_decay = min(base_score, int(age_months / 6))
        
        # Priority Keyword Boost & Hash calculation
        keyword_boost = 0
        content_for_hash = b""
        
        # Optimize: Read content once for hash and keywords
        if size < 10 * 1024 * 1024:  # Reduce to 10MB limit for faster processing
            try:
                with open(file_path, 'rb') as f:
                    content_for_hash = f.read()
                
                # Check keywords in text (case insensitive)
                text_content = content_for_hash.decode('utf-8', errors='ignore').lower()
                for kw, boost in PRIORITY_KEYWORDS.items():
                    if kw in text_content:
                        keyword_boost += boost
            except:
                pass
        
        final_score = max(1, base_score - recency_decay + keyword_boost)
        file_hash = hashlib.sha256(content_for_hash or file_path.encode()).hexdigest()
        
        project = "gen_88" if GEN_88_ROOT in file_path else "active"
        status = "ACTIVE" if GEN_88_ROOT in file_path else "STALE"

        return {
            "path": file_path,
            "hash": file_hash,
            "size": size,
            "mtime": mtime,
            "score": final_score,
            "project": project,
            "status": status,
            "content": content_for_hash if size < 1 * 1024 * 1024 else None # Only store blobs < 1MB directly
        }
    except Exception as e:
        return None

def init_db(conn):
    conn.execute(f"SET memory_limit = '{MEMORY_LIMIT}';")
    conn.execute(f"SET threads = {THREADS};")
    conn.execute("SET preserve_insertion_order = false;")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS blobs (
            hash TEXT PRIMARY KEY,
            content BLOB,
            size BIGINT,
            is_compressed BOOLEAN DEFAULT TRUE
        );
        CREATE TABLE IF NOT EXISTS file_system (
            path TEXT PRIMARY KEY,
            hash TEXT,
            score INTEGER,
            modified_at TIMESTAMP,
            era TEXT DEFAULT 'Phoenix',
            project TEXT,
            status TEXT DEFAULT 'STALE',
            size BIGINT,
            FOREIGN KEY (hash) REFERENCES blobs(hash)
        );
    """)

def main():
    print(f"🚀 REBIRTH: Optimized Hive Ingestion (Shadow Marking Mode)")
    print(f"📍 Database: {DB_PATH}")
    print(f"🎯 Scope: Gen 88 Priority ({GEN_88_ROOT})")
    
    start_time = time.time()
    ignore_patterns = load_ignore_patterns()
    conn = duckdb.connect(DB_PATH)
    init_db(conn)
    
    # --- PHASE 1: Shadow Marking (Mark existing ACTIVE as STALE) ---
    print("⏳ Shadow Marking previous state...")
    conn.execute("UPDATE file_system SET status = 'STALE' WHERE status = 'ACTIVE'")
    
    # --- PHASE 2: Fast Scan & Delta Detection (Active Roots) ---
    print("📂 Scanning active directories...")
    existing_files = {}
    try:
        res = conn.execute("SELECT path, modified_at, size FROM file_system").fetchall()
        for r in res:
            existing_files[r[0]] = (r[1].timestamp() if r[1] else 0, r[2] or 0)
    except Exception as e:
        print(f"⚠️ Metadata load failed: {e}")
    
    files_to_update = []
    files_to_reactivate = [] 
    found_paths_count = 0

    for root_path in ROOT_PATHS:
        if not os.path.exists(root_path): continue
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d + "/" not in ignore_patterns and d not in ignore_patterns]
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    stat = os.stat(full_path)
                    mtime = stat.st_mtime
                    size = stat.st_size
                except: continue
                found_paths_count += 1
                is_gen_88 = GEN_88_ROOT in full_path
                if full_path in existing_files:
                    db_mtime, db_size = existing_files[full_path]
                    if abs(mtime - db_mtime) < 1 and size == db_size:
                        if is_gen_88: files_to_reactivate.append(full_path)
                        continue
                files_to_update.append(full_path)

    # --- PHASE 2.5: Fast Legacy Registration (Meta Only) ---
    # Ensure foreign key exists
    conn.execute("INSERT OR IGNORE INTO blobs (hash, content, size, is_compressed) VALUES ('LEGACY_STALE', NULL, 0, FALSE)")
    
    legacy_count = 0
    for root_path in LEGACY_PATHS:
        if root_path in ROOT_PATHS: continue
        if not os.path.exists(root_path): continue
        print(f"🕵️ Registering Legacy Meta: {root_path}")
        legacy_batch = []
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d + "/" not in ignore_patterns and d not in ignore_patterns]
            for file in files:
                full_path = os.path.join(root, file)
                if full_path in existing_files: continue
                try:
                    stat = os.stat(full_path)
                    legacy_batch.append((full_path, 'LEGACY_STALE', 1, float(stat.st_mtime), '_archive', 'STALE', stat.st_size))
                    if len(legacy_batch) >= 2000:
                        try:
                            # Use executing without manual BEGIN/COMMIT to avoid state errors
                            conn.executemany("INSERT OR REPLACE INTO file_system (path, hash, score, modified_at, project, status, size) VALUES (?, ?, ?, to_timestamp(?), ?, ?, ?)", legacy_batch)
                            legacy_count += len(legacy_batch)
                        except Exception as te:
                            print(f"⚠️ Batch insert failed: {te}")
                        legacy_batch = []
                except: continue
        if legacy_batch:
            try:
                conn.executemany("INSERT OR REPLACE INTO file_system (path, hash, score, modified_at, project, status, size) VALUES (?, ?, ?, to_timestamp(?), ?, ?, ?)", legacy_batch)
                legacy_count += len(legacy_batch)
            except Exception as te:
                print(f"⚠️ Final batch insert failed: {te}")

    print(f"📊 Global Results:")
    print(f"  - Active files scanned: {found_paths_count}")
    print(f"  - Files needing update/hash: {len(files_to_update)}")
    print(f"  - New Legacy records registered: {legacy_count}")
    
    # --- PHASE 3: Reactive Shadow Marking (Re-activate matching Gen 88 files) ---
    if files_to_reactivate:
        print(f"🔄 Reactivating {len(files_to_reactivate)} cached Gen 88 records...")
        # Batch reactivation in SQL
        for i in range(0, len(files_to_reactivate), 5000):
            batch = files_to_reactivate[i:i+5000]
            conn.execute("UPDATE file_system SET status = 'ACTIVE' WHERE path IN (" + ",".join(["?"] * len(batch)) + ")", batch)

    # --- PHASE 4: Parallel Processing of Deltas ---
    if files_to_update:
        print(f"⚖️ Processing {len(files_to_update)} changes...")
        processed_count = 0
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            for i in range(0, len(files_to_update), BATCH_SIZE):
                chunk = files_to_update[i:i + BATCH_SIZE]
                # Process chunk and immediate ingest to free memory
                results = list(executor.map(calculate_hash_and_meta, chunk))
                
                conn.execute("BEGIN TRANSACTION")
                try:
                    for r in results:
                        if not r: continue
                        conn.execute("INSERT OR IGNORE INTO blobs (hash, content, size) VALUES (?, ?, ?)",
                                     (r['hash'], r['content'], r['size']))
                        conn.execute("INSERT OR REPLACE INTO file_system (path, hash, score, modified_at, project, status, size) VALUES (?, ?, ?, to_timestamp(?), ?, ?, ?)",
                                     (r['path'], r['hash'], r['score'], r['mtime'], r['project'], r['status'], r['size']))
                    conn.execute("COMMIT")
                except Exception as e:
                    conn.execute("ROLLBACK")
                    print(f"❌ Batch insertion failed: {e}")
                
                processed_count += len(chunk)
                if processed_count % 1000 == 0 or processed_count == len(files_to_update):
                    print(f"⚡ {processed_count}/{len(files_to_update)} delta files active/synced.")

    elapsed = time.time() - start_time
    print(f"\n✅ RECONSTRUCTION COMPLETE: {elapsed:.1f}s")
    active_count = conn.execute("SELECT COUNT(*) FROM file_system WHERE status = 'ACTIVE'").fetchone()[0]
    print(f"📈 Total Active (Gen 88) Files: {active_count}")
    conn.close()

if __name__ == "__main__":
    main()

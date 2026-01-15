# Medallion: Bronze | Mutation: 0% | HIVE: V
import os
import hashlib
import duckdb
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# --- PROTOCOL CONFIG (P6) ---
DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
ROOT_PATHS = [
    "/home/tommytai3/active", 
    "/home/tommytai3/_archive_dev_2026_1_14",
    "/home/tommytai3/hfo_gen88",
    "/home/tommytai3/hfo_gen87_x3",
    "/home/tommytai3/hive_fleet_obsidian_2025_11",
    "/home/tommytai3/gen88_bronze",
    "/home/tommytai3/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52"
]
BATCH_SIZE = 500
THREADS = 4  # Reduced from 7 to ensure system stability during heavy I/O
MEM_LIMIT = "1.5GB"

def get_hash(content):
    return hashlib.sha256(content).hexdigest()

def init_db():
    conn = duckdb.connect(DB_PATH)
    conn.execute(f"SET memory_limit = '{MEM_LIMIT}';")
    # Ensure FTS extension is installed for SSOT search capabilities
    conn.execute("INSTALL fts; LOAD fts;")
    conn.execute("CREATE TABLE IF NOT EXISTS blobs (hash TEXT PRIMARY KEY, content BLOB, size INTEGER);")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_system (
            path TEXT PRIMARY KEY, 
            hash TEXT, 
            modified_at TIMESTAMP
        );
    """)
    # Schema Migration: Add era and project if they don't exist
    cols = conn.execute("PRAGMA table_info('file_system')").fetchall()
    col_names = [c[1] for c in cols]
    if "era" not in col_names:
        print("🛠️ Migrating Schema: Adding 'era' column")
        conn.execute("ALTER TABLE file_system ADD COLUMN era TEXT")
    if "project" not in col_names:
        print("🛠️ Migrating Schema: Adding 'project' column")
        conn.execute("ALTER TABLE file_system ADD COLUMN project TEXT")
        
    return conn

def determine_era(file_path):
    """Assigns an 'era' tag based on directory patterns for SSOT timeline mapping."""
    path_lower = file_path.lower()
    if "gen_88" in path_lower or "hfo_gen88" in path_lower:
        return "GEN88_ACTIVE"
    elif "bootstrap" in path_lower:
        return "HFO_BOOTSTRAP"
    elif "hopeos" in path_lower:
        return "HOPEOS_ERA"
    elif "tags" in path_lower or "mediapipe" in path_lower:
        return "TAGS_DRUMPADS"
    elif "tectangle" in path_lower:
        return "TECTANGLE_ERA"
    elif "vision" in path_lower or "mediapipeline" in path_lower:
        return "COMPUTER_VISION_EARLY"
    elif "2025" in path_lower:
        return "COLD_BRONZE_2025"
    return "UNCATEGORIZED"

def stream_files(roots):
    """Generator to yield files one by one to avoid OOM in sorting large lists."""
    for root_path in roots:
        for root, dirs, files in os.walk(root_path):
            # Basic pruning to stay within memory limits
            if ".git" in root or "node_modules" in root:
                continue
            for file in files:
                yield os.path.join(root, file)

def process_batch(batch, conn):
    """Processes a batch of files with transactional safety."""
    conn.execute("BEGIN TRANSACTION")
    try:
        for file_path in batch:
            try:
                p = Path(file_path)
                if not p.is_file(): continue
                
                mtime = p.stat().st_mtime
                size = p.stat().st_size
                
                # Check for existing file + timestamp to skip reprocessing
                existing = conn.execute("SELECT modified_at, era FROM file_system WHERE path = ?", (file_path,)).fetchone()
                era = determine_era(file_path)
                project = file_path.split("/")[3] if len(file_path.split("/")) > 3 else "ROOT"

                if existing and abs(existing[0].timestamp() - mtime) < 1:
                    # Even if file is same, update metadata if era is missing
                    if existing[1] is None:
                        conn.execute("UPDATE file_system SET era = ?, project = ? WHERE path = ?", (era, project, file_path))
                    continue
                
                # Check size BEFORE reading
                content = None
                if size < 5 * 1024 * 1024:  # 5MB limit for DB blobs
                    with open(file_path, "rb") as f:
                        content = f.read()
                    f_hash = hashlib.sha256(content).hexdigest()
                else:
                    # Hash large files in chunks without loading to RAM
                    sha256 = hashlib.sha256()
                    with open(file_path, "rb") as f:
                        while chunk := f.read(1024 * 1024):
                            sha256.update(chunk)
                    f_hash = sha256.hexdigest()
                
                # Dedupe Blobs
                conn.execute("INSERT OR IGNORE INTO blobs (hash, content, size) VALUES (?, ?, ?)", 
                             (f_hash, content, size))
                
                # Record File with Era and Project metadata
                era = determine_era(file_path)
                project = file_path.split("/")[3] if len(file_path.split("/")) > 3 else "ROOT"
                
                conn.execute("""
                    INSERT OR REPLACE INTO file_system (path, hash, modified_at, era, project) 
                    VALUES (?, ?, to_timestamp(?), ?, ?)
                """, (file_path, f_hash, mtime, era, project))
            except Exception as e:
                pass # Silently skip individuals to keep daemon alive
                
        conn.execute("COMMIT")
        return len(batch)
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Batch Error: {e}")
        return 0

def run_daemon():
    print(f"🐙 Kraken Keeper P6 Daemon starting... DB: {DB_PATH}")
    conn = init_db()
    
    batch = []
    total_processed = 0
    estimated_total = 210000  # Revised estimate based on current trajectory
    start_time = time.time()
    
    for file_path in stream_files(ROOT_PATHS):
        batch.append(file_path)
        if len(batch) >= BATCH_SIZE:
            processed = process_batch(batch, conn)
            total_processed += processed
            batch = []
            
            # Detailed reporting every 10,000 files
            if total_processed % 10000 == 0:
                elapsed = time.time() - start_time
                files_per_sec = total_processed / elapsed if elapsed > 0 else 1
                remaining = max(0, estimated_total - total_processed)
                eta_min = (remaining / files_per_sec) / 60 if files_per_sec > 0 else 0
                
                stats = conn.execute("SELECT era, count(*) FROM file_system GROUP BY era").fetchall()
                print("\n" + "="*50)
                print(f"📊 [KRAKEN STATUS REPORT]")
                print(f"   Progress: {total_processed} files assimilated")
                print(f"   Trajectory: {total_processed/estimated_total:.1%} of targeted estimate")
                print(f"   Velocity: {files_per_sec:.1f} files/sec")
                print(f"   Target ETA: {eta_min:.1f} minutes")
                print(f"   Eras Identified: {stats}")
                print("="*50 + "\n")
            else:
                if total_processed % 1000 == 0:
                    print(f"⚡ [P6] Assimilated {total_processed} files... (Elapsed: {time.time()-start_time:.1f}s)")
            
    # Final cleanup
    if batch:
        process_batch(batch, conn)
    
    print("🧠 Building FTS Index for SSOT Search...")
    # This might take a few minutes on 72GB of potential text
    try:
        conn.execute("PRAGMA create_fts_index('file_system', 'path', 'era', 'project')")
        print("✅ FTS Index Built Successfully.")
    except Exception as e:
        print(f"⚠️ FTS Indexing skipped or failed: {e}")
        
    print(f"✅ Protocol L2 Cold Bronze Complete. Total: {total_processed}")
    conn.close()

if __name__ == "__main__":
    run_daemon()

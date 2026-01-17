# Medallion: Bronze | Mutation: 0% | HIVE: E
import os
import hashlib
import duckdb
import time
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# --- CONFIGURATION ---
DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_unified_v88.duckdb"
ROOT_PATHS = ["/home/tommytai3/active", "/home/tommytai3/_archive_dev_2026_1_14"]
IGNORE_FILE = "/home/tommytai3/.hfo_ignore"
BATCH_SIZE = 100
THREADS = 4
MEMORY_LIMIT = "1GB"

PRIORITY_KEYWORDS = {
    "grimoire": 10,
    "galoise lattice": 10,
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
    """Worker function to process a single file."""
    try:
        path_obj = Path(file_path)
        stat = path_obj.stat()
        size = stat.st_size
        
        # Freshness Score Calculation
        base_score = 10 if "active/" in file_path else 1
        # Recency decay (simplified)
        mtime = stat.st_mtime
        age_months = (time.time() - mtime) / (30 * 24 * 3600)
        recency_decay = min(base_score, int(age_months / 6))
        
        # Priority Keyword Boost
        keyword_boost = 0
        content_for_hash = b""
        if size < 100 * 1024 * 1024:  # 100MB limit for content ingestion
            with open(file_path, 'rb') as f:
                content_for_hash = f.read()
            
            # Check keywords in text (case insensitive)
            try:
                text_content = content_for_hash.decode('utf-8', errors='ignore').lower()
                for kw, boost in PRIORITY_KEYWORDS.items():
                    if kw in text_content:
                        keyword_boost += boost
            except:
                pass
        
        final_score = max(1, base_score - recency_decay + keyword_boost)
        
        file_hash = hashlib.sha256(content_for_hash).hexdigest()
        
        return {
            "path": file_path,
            "hash": file_hash,
            "size": size,
            "mtime": mtime,
            "score": final_score,
            "content": content_for_hash if size < 5 * 1024 * 1024 else None # Only store blobs < 5MB in DB directly
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
            size INTEGER,
            is_compressed BOOLEAN DEFAULT TRUE
        );
        CREATE TABLE IF NOT EXISTS file_system (
            path TEXT PRIMARY KEY,
            hash TEXT,
            score INTEGER,
            modified_at TIMESTAMP,
            FOREIGN KEY (hash) REFERENCES blobs(hash)
        );
    """)

def main():
    print(f"🚀 Starting Hive Roll-up: {DB_PATH}")
    start_time = time.time()
    
    ignore_patterns = load_ignore_patterns()
    conn = duckdb.connect(DB_PATH)
    init_db(conn)
    
    file_list = []
    print("📂 Scanning directories...")
    for root_path in ROOT_PATHS:
        for root, dirs, files in os.walk(root_path):
            # Apply ignore patterns to directories
            dirs[:] = [d for d in dirs if d + "/" not in ignore_patterns and d not in ignore_patterns]
            
            for file in files:
                if any(file.endswith(ext.replace('*', '')) for ext in ignore_patterns if ext.startswith('*')):
                    continue
                file_list.append(os.path.join(root, file))
    
    total_files = len(file_list)
    print(f"📄 Total files found: {total_files}")
    
    processed_count = 0
    with ProcessPoolExecutor(max_workers=THREADS) as executor:
        for i in range(0, total_files, BATCH_SIZE):
            batch_files = file_list[i:i + BATCH_SIZE]
            results = list(executor.map(calculate_hash_and_meta, batch_files))
            
            # Filter failed results
            results = [r for r in results if r is not None]
            
            # Batched Ingestion into DuckDB
            for r in results:
                try:
                    # Ingest Blob
                    conn.execute("INSERT OR IGNORE INTO blobs (hash, content, size) VALUES (?, ?, ?)", 
                                (r['hash'], r['content'], r['size']))
                    # Ingest Meta
                    conn.execute("INSERT OR REPLACE INTO file_system (path, hash, score, modified_at) VALUES (?, ?, ?, to_timestamp(?))", 
                                (r['path'], r['hash'], r['score'], r['mtime']))
                except Exception as e:
                    print(f"❌ Error ingesting {r['path']}: {e}")
            
            processed_count += len(batch_files)
            elapsed = time.time() - start_time
            print(f"⚡ Processed {processed_count}/{total_files} files... ({elapsed:.1f}s elapsed)")

    print("\n🔍 Initializing Full-Text Search Index...")
    conn.execute("INSTALL fts; LOAD fts;")
    # Index content for blobs that are likely text
    conn.execute("PRAGMA create_fts_index('blobs', 'hash', 'content');")
    
    conn.close()
    print(f"\n✅ SUCCESS! Unified Hive created in {time.time() - start_time:.1f} seconds.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Specific subfolder path for trial runing")
    args = parser.parse_args()
    
    if args.path:
        ROOT_PATHS = [args.path]
    
    main()

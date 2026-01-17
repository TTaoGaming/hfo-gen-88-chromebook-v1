# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb
import json
import os
from pathlib import Path

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
MANIFEST_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/HFO_MISSION_THREADS_MANIFEST_CONSOLIDATED.json"

def check_status():
    print(f"🔍 Auditing DuckDB: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("❌ Database file not found!")
        return

    conn = duckdb.connect(DB_PATH)
    
    # 1. Check Tables
    tables = conn.execute("SHOW TABLES").fetchall()
    print(f"📊 Tables found: {[t[0] for t in tables]}")
    
    # 2. Check Counts
    try:
        blob_count = conn.execute("SELECT count(*) FROM blobs").fetchone()[0]
        file_count = conn.execute("SELECT count(*) FROM file_system").fetchone()[0]
        print(f"📉 Blob count: {blob_count}")
        print(f"📉 File count: {file_count}")
    except Exception as e:
        print(f"❌ Error querying tables: {e}")
        conn.close()
        return

    # 3. Check Manifest Delta
    if not os.path.exists(MANIFEST_PATH):
        print("❌ Manifest file not found!")
    else:
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
        
        manifest_files = manifest.get("alpha", []) + manifest.get("omega", [])
        manifest_paths = [f.get("path") for f in manifest_files if f.get("path")]
        print(f"📋 Total mission threads in manifest: {len(manifest_paths)}")
        
        # Check how many manifest paths exist in file_system
        placeholders = ', '.join(['?'] * len(manifest_paths))
        query = f"SELECT path FROM file_system WHERE path IN ({placeholders})"
        ingested_manifest_paths = [r[0] for r in conn.execute(query, manifest_paths).fetchall()]
        
        print(f"✅ Mission threads ingested: {len(ingested_manifest_paths)}")
        delta = list(set(manifest_paths) - set(ingested_manifest_paths))
        print(f"⚠️ Delta (Waiting for ingestion): {len(delta)}")
        if delta:
            print("🚀 Sample Delta Paths:")
            for d in delta[:5]:
                print(f"  - {d}")

    # 4. Check for INT32 issues
    try:
        max_size = conn.execute("SELECT max(size) FROM blobs").fetchone()[0]
        print(f"📏 Max blob size: {max_size}")
    except:
        pass

    conn.close()

if __name__ == "__main__":
    check_status()

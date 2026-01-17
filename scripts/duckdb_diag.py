import duckdb
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

def diag():
    if not os.path.exists(DB_PATH):
        print(f"Error: DB not found at {DB_PATH}")
        return

    conn = duckdb.connect(DB_PATH)
    
    print("--- DuckDB Long-Term Memory Audit ---")
    
    # Check tables
    tables = conn.execute("SHOW TABLES").fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    if ('file_system',) in tables:
        fs_count = conn.execute("SELECT count(*) FROM file_system").fetchone()[0]
        active_count = conn.execute("SELECT count(*) FROM file_system WHERE status = 'ACTIVE'").fetchone()[0]
        stale_count = conn.execute("SELECT count(*) FROM file_system WHERE status = 'STALE'").fetchone()[0]
        print(f"file_system count: {fs_count}")
        print(f"  ACTIVE: {active_count}")
        print(f"  STALE: {stale_count}")
        
        # Eras
        eras = conn.execute("SELECT era, count(*) FROM file_system GROUP BY era").fetchall()
        print(f"Eras: {eras}")
    
    if ('blobs',) in tables:
        blobs_count = conn.execute("SELECT count(*) FROM blobs").fetchone()[0]
        print(f"blobs count: {blobs_count}")
        
        # Check for LEGACY_STALE blob
        legacy_blob = conn.execute("SELECT count(*) FROM blobs WHERE hash = 'LEGACY_STALE'").fetchone()[0]
        print(f"LEGACY_STALE blob exists: {legacy_blob > 0}")

    # Check for FK violations (orphaned hashes in file_system)
    orphans = conn.execute("SELECT count(*) FROM file_system fs LEFT JOIN blobs b ON fs.hash = b.hash WHERE b.hash IS NULL").fetchone()[0]
    print(f"Orphaned file_system entries (FK mismatch): {orphans}")

    conn.close()

if __name__ == "__main__":
    diag()

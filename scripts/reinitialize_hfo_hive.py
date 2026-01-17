# Medallion: Bronze | Mutation: 0% | HIVE: I
import duckdb
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

def reinitialize():
    print(f"Connecting to {DB_PATH}...")
    conn = duckdb.connect(DB_PATH)
    
    # Drops
    print("Dropping stale structures...")
    conn.execute("DROP TABLE IF EXISTS blobs_new")
    conn.execute("DROP TABLE IF EXISTS file_system")
    conn.execute("DROP TABLE IF EXISTS blobs")
    
    print("Initializing Hardened Blobs Schema (BIGINT)...")
    conn.execute("""
    CREATE TABLE blobs (
        hash VARCHAR PRIMARY KEY,
        content BLOB,
        size BIGINT,
        is_compressed BOOLEAN DEFAULT TRUE
    )
    """)
    
    print("Initializing Shadow Marking File System Schema...")
    conn.execute("""
    CREATE TABLE file_system (
        path VARCHAR PRIMARY KEY,
        hash VARCHAR,
        score INTEGER,
        modified_at TIMESTAMP,
        era VARCHAR DEFAULT 'Phoenix',
        project VARCHAR,
        status VARCHAR DEFAULT 'STALE',
        FOREIGN KEY (hash) REFERENCES blobs(hash)
    )
    """)
    
    print("Initializing Supporting Structures...")
    conn.execute("CREATE TABLE IF NOT EXISTS actor_states (id VARCHAR PRIMARY KEY, state JSON)")
    conn.execute("CREATE TABLE IF NOT EXISTS mission_journal (id INTEGER PRIMARY KEY, entry TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    
    conn.close()
    print("Hive Reinitialized Successfully.")

if __name__ == "__main__":
    reinitialize()

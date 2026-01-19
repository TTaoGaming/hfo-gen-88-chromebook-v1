# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb
import pandas as pd

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

try:
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    print("--- MISSION JOURNAL SCHEMA ---")
    schema = conn.execute("PRAGMA table_info('mission_journal')").fetchall()
    for col in schema:
        print(col)
        
    print("\n--- RECENT MISSION JOURNAL ENTRIES (Last 50) ---")
    # Assuming the first column is a timestamp or ID
    df = conn.execute("SELECT * FROM mission_journal ORDER BY 1 DESC LIMIT 50").df()
    print(df.to_string())
    
    print("\n--- TOP SCORED FILES ---")
    df_files = conn.execute("SELECT path, score, modified_at FROM file_system ORDER BY modified_at DESC LIMIT 50").df()
    print(df_files.to_string())
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")

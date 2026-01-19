# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb
import json

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

try:
    conn = duckdb.connect(DB_PATH, read_only=True)
    tables = conn.execute("SHOW TABLES").fetchall()
    print("Tables in root DB:")
    for t in tables:
        print(f"- {t[0]}")
    
    # Check if there's an activity or logs table
    for t in tables:
        if 'log' in t[0].lower() or 'activity' in t[0].lower() or 'events' in t[0].lower():
            print(f"\nRecent entries from {t[0]}:")
            try:
                rows = conn.execute(f"SELECT * FROM {t[0]} ORDER BY 1 DESC LIMIT 5").fetchall()
                for r in rows:
                    print(r)
            except Exception as e:
                print(f"Error reading {t[0]}: {e}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")

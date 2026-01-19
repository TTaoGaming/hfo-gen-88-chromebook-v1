import duckdb
import sys

db_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

try:
    con = duckdb.connect(db_path, read_only=True)
    print("Tables:")
    print(con.execute("SHOW TABLES").fetchall())
    
    # Check for anything in 2025
    tables = con.execute("SHOW TABLES").fetchall()
    found_any = False
    for table_tuple in tables:
        table_name = table_tuple[0]
        try:
            # Try to find columns that look like timestamps
            cols = con.execute(f"DESCRIBE {table_name}").fetchall()
            timestamp_cols = [c[0] for c in cols if "timestamp" in c[0].lower() or "time" in c[0].lower() or "created" in c[0].lower() or "modified" in c[0].lower()]
            
            for col in timestamp_cols:
                count = con.execute(f"SELECT COUNT(*) FROM {table_name} WHERE CAST({col} AS STRING) LIKE '2025%'").fetchone()[0]
                if count > 0:
                    print(f"FOUND {count} records in {table_name}.{col} starting with '2025'")
                    found_any = True
                    # show a sample
                    print(con.execute(f"SELECT * FROM {table_name} WHERE CAST({col} AS STRING) LIKE '2025%' LIMIT 1").fetchall())
        except Exception as e:
            # table might not have timestamps
            pass
    if not found_any:
        print("No records from 2025 found in any table.")
            
except Exception as e:
    print(f"Error: {e}")

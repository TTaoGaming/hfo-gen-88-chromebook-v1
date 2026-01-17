import duckdb
import os

db_path = './hfo_gen_88_cb_v2/hfo_unified_v88.duckdb'
conn = duckdb.connect(db_path)

print("--- HFO DELTA AUDIT ---")
total_records = conn.execute("SELECT COUNT(*) FROM file_system").fetchall()[0][0]
print(f"DuckDB Total Records: {total_records}")

# Check existence for all paths
all_paths = [p[0] for p in conn.execute("SELECT path FROM file_system").fetchall()]
exists_count = sum(1 for p in all_paths if os.path.exists(p))

print(f"Files Physically on Disk: {exists_count}")
print(f"Shadow/Missing Files: {total_records - exists_count}")

# Check modified deltas for existing files
# (This would require checksum comparison, but let's start with presence)
print("-----------------------")

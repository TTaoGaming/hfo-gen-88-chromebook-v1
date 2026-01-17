import duckdb
import hashlib
import os

db_path = './hfo_gen_88_cb_v2/hfo_unified_v88.duckdb'
conn = duckdb.connect(db_path)

files_to_check = [
    'hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py',
    'seek_guidance.py',
    'AGENTS.md',
    'hfo_gen_88_cb_v2/hfo_spider_sovereign_daemon.py'
]

print("--- CONTENT DELTA REPORT ---")
for f in files_to_check:
    abs_path = os.path.abspath(f)
    if not os.path.exists(abs_path):
        print(f"{f}: MISSING ON DISK")
        continue
        
    db_row = conn.execute(f"SELECT hash, era FROM file_system WHERE path = '{abs_path}'").fetchone()
    
    with open(abs_path, 'rb') as fh:
        current_hash = hashlib.md5(fh.read()).hexdigest()
        
    if db_row:
        db_hash, era = db_row
        status = "MATCH" if db_hash == current_hash else "MODIFIED"
        print(f"{f} [{era}]: {status}")
        if status == "MODIFIED":
            print(f"  DB Hash: {db_hash}")
            print(f"  Disk Hash: {current_hash}")
    else:
        print(f"{f}: NOT REGISTERED IN DUCKDB")
print("----------------------------")

# Medallion: Bronze | Mutation: 0% | HIVE: V
import os
import duckdb
from pathlib import Path

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
ROOT_PATHS = ["/home/tommytai3/active", "/home/tommytai3/_archive_dev_2026_1_14"]
IGNORE_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".vscode"}

def get_db_paths():
    conn = duckdb.connect(DB_PATH)
    res = conn.execute("SELECT path FROM file_system").fetchall()
    return set(r[0] for r in res)

def find_fs_paths():
    fs_paths = set()
    for root_path in ROOT_PATHS:
        for root, dirs, files in os.walk(root_path):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                fs_paths.add(os.path.join(root, file))
    return fs_paths

def main():
    print("Fetching paths from DB...")
    db_paths = get_db_paths()
    print(f"Total files in DB: {len(db_paths)}")

    print("Scanning filesystem...")
    fs_paths = find_fs_paths()
    print(f"Total files on FS: {len(fs_paths)}")

    delta = fs_paths - db_paths
    print(f"Delta (on FS but not in DB): {len(delta)}")

    if delta:
        print("\nSample delta files (first 10):")
        for p in list(delta)[:10]:
            print(f"  {p}")
            
    # Check for files in DB but not on FS
    phantom = db_paths - fs_paths
    print(f"\nPhantom (in DB but missing from FS): {len(phantom)}")
    if phantom:
        print("\nSample phantom files (first 10):")
        for p in list(phantom)[:10]:
            print(f"  {p}")

if __name__ == "__main__":
    main()

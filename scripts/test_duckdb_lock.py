import duckdb
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

def test_duckdb_lock():
    print(f"🔍 Testing DuckDB lock status for: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("❌ File does not exist.")
        return

    try:
        # Try read-only connection
        con = duckdb.connect(database=DB_PATH, read_only=True)
        res = con.execute("SELECT count(*) FROM file_system").fetchone()
        print(f"✅ Read-only connection successful. File count: {res[0]}")
        con.close()
    except Exception as e:
        print(f"❌ Read-only connection failed: {e}")

    try:
        # Try read-write connection (this will fail if another process is writing or has a lock)
        con = duckdb.connect(database=DB_PATH, read_only=False)
        print("✅ Read-write connection successful (No exclusive locks detected).")
        con.close()
    except Exception as e:
        print(f"⚠️ Read-write connection failed (expected if locked or read-only): {e}")

if __name__ == "__main__":
    test_duckdb_lock()

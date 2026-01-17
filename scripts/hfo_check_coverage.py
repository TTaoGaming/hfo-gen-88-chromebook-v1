# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
KEYWORDS = ['p0_', 'p1_', 'p2_', 'p3_', 'p4_', 'p5_', 'p6_', 'p7_', 'omega_gen4', 'mission_thread']

def check_coverage():
    conn = duckdb.connect(DB_PATH)
    print("Database Keyword Coverage:")
    for kw in KEYWORDS:
        count = conn.execute(f"SELECT count(*) FROM file_system WHERE path LIKE '%{kw}%'").fetchone()[0]
        print(f"  {kw}: {count}")

if __name__ == "__main__":
    check_coverage()

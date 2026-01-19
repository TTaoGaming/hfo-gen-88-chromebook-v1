# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

def search_logic_survivors():
    conn = duckdb.connect(DB_PATH)
    
    print("🔎 Searching for 'Logic Survivors' across history...")
    print("-" * 60)
    
    # Query 1: Concept Density (Quality vs Slop)
    # We rank files where keywords are high but file size is reasonable.
    # We filter out large binary blobs or excessive boilerplate.
    density_query = """
    SELECT 
        fs.path, 
        fs.score, 
        b.size,
        (fs.score * 1.0 / (b.size + 1)) * 1024 as density_index,
        fs.modified_at
    FROM file_system fs
    JOIN blobs b ON fs.hash = b.hash
    WHERE b.size > 100 AND b.size < 500000 -- Ignore empty or massive slop files
    ORDER BY density_index DESC
    LIMIT 15;
    """
    
    # Query 2: Path Immortality (Hash Collisions across different names)
    # This finds logic that you moved or renamed but kept identical because it worked.
    immortality_query = """
    SELECT 
        hash, 
        count(*) as occurrences, 
        list(path) as paths,
        max(modified_at) as last_seen
    FROM file_system
    GROUP BY hash
    HAVING occurrences > 1
    ORDER BY occurrences DESC, last_seen DESC
    LIMIT 10;
    """

    print("\n💎 TOP QUALITY LOGIC (High Concept Density):")
    results = conn.execute(density_query).fetchall()
    for r in results:
        print(f"[{r[4].strftime('%Y-%m')}] Density: {r[3]:.2f} | Score: {r[1]} | {os.path.basename(r[0])}")
        print(f"   -> {r[0]}")

    print("\n♻️ SURVIVOR CORE (Identical Content across Paths/Time):")
    results = conn.execute(immortality_query).fetchall()
    for r in results:
        # Just show the unique folder names to see how it traveled
        folders = set(p.split('/')[-2] for p in r[2])
        print(f"Hash {r[0][:8]}... seen {r[1]} times in: {', '.join(folders)}")
        print(f"   -> Latest: {r[2][0]}")

    conn.close()

if __name__ == "__main__":
    search_logic_survivors()

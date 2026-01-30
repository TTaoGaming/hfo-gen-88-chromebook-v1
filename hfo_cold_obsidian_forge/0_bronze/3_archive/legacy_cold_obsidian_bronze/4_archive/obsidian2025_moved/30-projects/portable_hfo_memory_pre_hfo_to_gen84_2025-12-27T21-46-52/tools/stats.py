#!/usr/bin/env python3
"""
Show statistics about the HFO memory bank.

Usage:
    python tools/stats.py
"""
import duckdb
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hfo_memory.duckdb')

def main():
    con = duckdb.connect(DB_PATH, read_only=True)
    
    print("=" * 50)
    print("HFO MEMORY BANK STATISTICS")
    print("=" * 50)
    
    # Total count
    total = con.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
    print(f"\nTotal artifacts: {total:,}")
    
    # By era
    print("\n=== BY ERA ===")
    for row in con.execute("""
        SELECT era, COUNT(*) as cnt 
        FROM artifacts 
        GROUP BY era 
        ORDER BY cnt DESC
    """).fetchall():
        print(f"  {row[0]}: {row[1]:,}")
    
    # By generation (top 10)
    print("\n=== TOP GENERATIONS ===")
    for row in con.execute("""
        SELECT generation, COUNT(*) as cnt 
        FROM artifacts 
        WHERE generation IS NOT NULL
        GROUP BY generation 
        ORDER BY cnt DESC 
        LIMIT 10
    """).fetchall():
        print(f"  Gen {row[0]}: {row[1]:,}")
    
    # Key files
    print("\n=== KEY FILE COUNTS ===")
    patterns = [
        ('HANDOFF', '%handoff%'),
        ('QUINE', '%quine%'),
        ('GEM', '%gem%'),
        ('BATON', '%baton%'),
        ('BLACKBOARD', '%blackboard%'),
        ('Grimoire Cards', 'card_%'),
    ]
    for name, pattern in patterns:
        count = con.execute(
            "SELECT COUNT(*) FROM artifacts WHERE lower(filename) LIKE ?",
            [pattern]
        ).fetchone()[0]
        print(f"  {name}: {count}")
    
    # Content size
    size_mb = con.execute(
        "SELECT SUM(LENGTH(content))/1024/1024.0 FROM artifacts"
    ).fetchone()[0]
    print(f"\nTotal content size: {size_mb:.1f} MB")
    
    # FTS status
    print("\n=== FTS STATUS ===")
    try:
        con.execute("LOAD fts")
        test = con.execute("""
            SELECT COUNT(*) FROM artifacts 
            WHERE fts_main_artifacts.match_bm25(id, 'test') IS NOT NULL
        """).fetchone()[0]
        print(f"  FTS: ✅ Working ({test} results for 'test')")
    except Exception as e:
        print(f"  FTS: ❌ Error - {e}")
    
    con.close()

if __name__ == '__main__':
    main()

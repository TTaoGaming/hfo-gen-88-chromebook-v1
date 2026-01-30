#!/usr/bin/env python3
"""
Get full content of an artifact by filename.

Usage:
    python tools/get.py HANDOFF_GEN_72
    python tools/get.py card_09_obsidian_spider
"""
import duckdb
import argparse
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hfo_memory.duckdb')

def get(filename):
    con = duckdb.connect(DB_PATH, read_only=True)
    result = con.execute(
        "SELECT filename, generation, era, content FROM artifacts WHERE filename LIKE ? LIMIT 1",
        [f'%{filename}%']
    ).fetchone()
    
    if result:
        gen_str = f"Gen {result[1]}" if result[1] else result[2]
        print(f"=== {result[0]} ({gen_str}) ===\n")
        print(result[3])
    else:
        print(f"Not found: {filename}")
    
    con.close()

def main():
    parser = argparse.ArgumentParser(description='Get artifact content')
    parser.add_argument('filename', help='Filename (partial match)')
    
    args = parser.parse_args()
    get(args.filename)

if __name__ == '__main__':
    main()

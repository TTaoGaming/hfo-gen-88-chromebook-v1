#!/usr/bin/env python3
"""
Search the HFO memory bank using FTS.

Usage:
    python tools/search.py "obsidian spider"
    python tools/search.py "Zero Invention" --limit 5
    python tools/search.py "HANDOFF" --content
"""
import duckdb
import argparse
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hfo_memory.duckdb')

def search(query, limit=10, show_content=False):
    con = duckdb.connect(DB_PATH, read_only=True)
    con.execute('LOAD fts')
    
    results = con.execute("""
        SELECT filename, generation, era, content,
               fts_main_artifacts.match_bm25(id, ?) as score
        FROM artifacts 
        WHERE score IS NOT NULL
        ORDER BY score DESC
        LIMIT ?
    """, [query, limit]).fetchall()
    
    print(f'=== SEARCH: "{query}" ===')
    print(f'Found {len(results)} results\n')
    
    for filename, gen, era, content, score in results:
        gen_str = f"Gen {gen}" if gen else era
        print(f'{gen_str}: {filename}')
        print(f'  Score: {score:.2f}')
        
        if show_content and content:
            # Show snippet around query terms
            content_lower = content.lower()
            query_lower = query.lower().split()[0]
            idx = content_lower.find(query_lower)
            if idx >= 0:
                start = max(0, idx - 100)
                end = min(len(content), idx + 300)
                snippet = content[start:end].replace('\n', ' ')
                print(f'  ...{snippet}...')
        print()
    
    con.close()
    return results

def main():
    parser = argparse.ArgumentParser(description='Search HFO memory bank')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Max results')
    parser.add_argument('--content', '-c', action='store_true', help='Show content snippets')
    
    args = parser.parse_args()
    search(args.query, args.limit, args.content)

if __name__ == '__main__':
    main()

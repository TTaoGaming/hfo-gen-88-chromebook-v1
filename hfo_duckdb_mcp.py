import duckdb
import os
import json
import sys

# Configuration
DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_unified_v88.duckdb"

def run_query(query):
    try:
        conn = duckdb.connect(DB_PATH, read_only=True)
        # Load FTS extension if needed
        conn.execute("INSTALL fts; LOAD fts;")
        result = conn.execute(query).fetchall()
        column_names = [desc[0] for desc in conn.description]
        conn.close()
        return [dict(zip(column_names, row)) for row in result]
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        return

    query = sys.argv[1]
    # Simple JSON-RPC-ish interface for MCP
    response = run_query(query)
    print(json.dumps(response, default=str))

if __name__ == "__main__":
    main()

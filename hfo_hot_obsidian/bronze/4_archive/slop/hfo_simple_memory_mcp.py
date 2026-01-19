# Medallion: Bronze | Mutation: 0% | HIVE: E
# HFO Simple Memory MCP - A robust, non-fragile alternative to the blackboard.
import sqlite3
import json
import sys
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_memory_sqlite.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            description TEXT,
            metadata JSON
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            from_id TEXT,
            to_id TEXT,
            relation_type TEXT,
            FOREIGN KEY(from_id) REFERENCES entities(id),
            FOREIGN KEY(to_id) REFERENCES entities(id)
        )
    """)
    conn.commit()
    conn.close()

def add_entity(entity_id, name, entity_type, description, metadata=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO entities (id, name, type, description, metadata) VALUES (?, ?, ?, ?, ?)",
        (entity_id, name, entity_type, description, json.dumps(metadata or {}))
    )
    conn.commit()
    conn.close()

def search_entities(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM entities WHERE name LIKE ? OR description LIKE ?",
        (f"%{query}%", f"%{query}%")
    )
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    
    # Process CLI command for MCP interaction
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "add":
            # Example: python hfo_simple_memory_mcp.py add "uuid" "Name" "Type" "Desc"
            add_entity(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            print("Entity Added.")
        elif cmd == "search":
            print(json.dumps(search_entities(sys.argv[2]), default=str))

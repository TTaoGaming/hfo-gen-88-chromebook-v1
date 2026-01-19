# Medallion: Bronze | Mutation: 0% | HIVE: I
"""
STRANGLER MIGRATION UTILITY
Source: hfo_memory_sqlite.db (Bespoke relational memory)
Target: memory.jsonl (Official Knowledge Graph format)
Mapping per mcp_migration_map.md
"""

import sqlite3
import json
import os
from datetime import datetime

SQLITE_DB = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_memory_sqlite.db"
OUTPUT_JSONL = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/official_memory.jsonl"

def migrate():
    if not os.path.exists(SQLITE_DB):
        print(f"Error: {SQLITE_DB} not found.")
        return

    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # 1. Migrate Entities
    # Schema: entities(id, name, type, description, metadata)
    # Target: {"type": "entity", "name": "...", "entityType": "...", "observations": ["description", "..."]}
    print("Migrating Entities...")
    cursor.execute("SELECT name, type, description, metadata FROM entities")
    entities = cursor.fetchall()
    
    with open(OUTPUT_JSONL, 'w') as f:
        for name, ent_type, desc, metadata_json in entities:
            observations = [desc] if desc else []
            try:
                metadata = json.loads(metadata_json) if metadata_json else {}
                if isinstance(metadata, dict):
                    for k, v in metadata.items():
                        observations.append(f"{k}: {v}")
                elif isinstance(metadata, list):
                    observations.extend([str(x) for x in metadata])
            except json.JSONDecodeError:
                if metadata_json:
                    observations.append(metadata_json)
            
            entry = {
                "type": "entity",
                "name": name,
                "entityType": ent_type or "Generic",
                "observations": observations
            }
            f.write(json.dumps(entry) + "\n")

        # 2. Migrate Relations
        # Schema: relations(from_id, to_id, relation_type)
        # Note: SQLite uses ID, but official uses Name. We need a lookup.
        print("Migrating Relations...")
        cursor.execute("SELECT id, name FROM entities")
        id_to_name = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute("SELECT from_id, to_id, relation_type FROM relations")
        relations = cursor.fetchall()
        for from_id, to_id, rel_type in relations:
            from_name = id_to_name.get(from_id)
            to_name = id_to_name.get(to_id)
            if from_name and to_name:
                entry = {
                    "type": "relation",
                    "from": from_name,
                    "to": to_name,
                    "relationType": rel_type or "related_to"
                }
                f.write(json.dumps(entry) + "\n")

    conn.close()
    print(f"Migration complete. Output: {OUTPUT_JSONL}")

if __name__ == "__main__":
    migrate()

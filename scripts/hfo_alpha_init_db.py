# Medallion: Bronze | Mutation: 0% | HIVE: I
import duckdb
import os

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

def init_db():
    print(f"🧬 [ALPHA] Initializing Actor State Schema in {DB_PATH}...")
    try:
        con = duckdb.connect(database=DB_PATH)
        
        # Create actor_states table for stateful persistence
        con.execute("""
            CREATE TABLE IF NOT EXISTS actor_states (
                actor_id VARCHAR PRIMARY KEY,
                mission_thread VARCHAR,
                state_json JSON,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1
            );
        """)
        
        # Create mission_journal for event sourcing
        con.execute("""
            CREATE TABLE IF NOT EXISTS mission_journal (
                event_id UUID DEFAULT gen_random_uuid(),
                actor_id VARCHAR,
                event_type VARCHAR,
                payload JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        print("✅ [ALPHA] Schema Initialized: actor_states, mission_journal.")
        con.close()
    except Exception as e:
        print(f"❌ [ALPHA] Initialization Failed: {e}")

if __name__ == "__main__":
    init_db()

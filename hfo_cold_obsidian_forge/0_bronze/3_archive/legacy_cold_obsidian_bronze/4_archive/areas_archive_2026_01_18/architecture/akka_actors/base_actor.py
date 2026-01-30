# Medallion: Bronze | Mutation: 0% | HIVE: I
import duckdb
import json
import os
import uuid
from typing import Dict, Any, Optional

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_unified_v88.duckdb" # Fallback to root if v2 is locked

class HardenedBaseActor:
    """
    Base Actor for HFO Mission Thread Alpha.
    Implements state persistence via DuckDB.
    """
    def __init__(self, actor_id: str, mission_thread: str = "ALPHA"):
        self.actor_id = actor_id
        self.mission_thread = mission_thread
        self.db_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
        self._ensure_tables()
        self.state: Dict[str, Any] = {}
        self.load_state()

    def _get_connection(self):
        return duckdb.connect(database=self.db_path)

    def _ensure_tables(self):
        """Ensures that the necessary tables exist in DuckDB."""
        try:
            con = self._get_connection()
            con.execute("""
                CREATE TABLE IF NOT EXISTS actor_states (
                    actor_id VARCHAR PRIMARY KEY,
                    mission_thread VARCHAR,
                    state_json VARCHAR,
                    version INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS mission_journal (
                    id INTEGER PRIMARY KEY,
                    actor_id VARCHAR,
                    event_type VARCHAR,
                    payload VARCHAR,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # DuckDB doesn't support AUTOINCREMENT directly but we can use sequences if needed.
            # mission_journal id will be handled by DuckDB if we use a sequence.
            con.close()
        except Exception as e:
            print(f"⚠️ [ACTOR-SYSTEM] Table Ensure Failed: {e}")

    def load_state(self):
        """Loads state from DuckDB actor_states table."""
        try:
            con = self._get_connection()
            result = con.execute(
                "SELECT state_json FROM actor_states WHERE actor_id = ?", 
                (self.actor_id,)
            ).fetchone()
            if result:
                self.state = json.loads(result[0])
                print(f"📖 [ACTOR-{self.actor_id}] State Loaded.")
            else:
                self.state = {"status": "INITIALIZED"}
                print(f"🐣 [ACTOR-{self.actor_id}] No previous state found. Initializing...")
            con.close()
        except Exception as e:
            print(f"⚠️ [ACTOR-{self.actor_id}] Load Failed: {e}")
            self.state = {"status": "ERROR", "error": str(e)}

    def persist_state(self):
        """Persists current state to DuckDB."""
        try:
            con = self._get_connection()
            state_str = json.dumps(self.state)
            con.execute("""
                INSERT OR REPLACE INTO actor_states (actor_id, mission_thread, state_json, version)
                VALUES (?, ?, ?, (SELECT COALESCE(MAX(version), 0) + 1 FROM actor_states WHERE actor_id = ?))
            """, (self.actor_id, self.mission_thread, state_str, self.actor_id))
            con.close()
            print(f"💾 [ACTOR-{self.actor_id}] State Persisted.")
        except Exception as e:
            print(f"❌ [ACTOR-{self.actor_id}] Persist Failed: {e}")

    def log_event(self, event_type: str, payload: Dict[str, Any]):
        """Logs an event to the mission_journal."""
        try:
            con = self._get_connection()
            payload_str = json.dumps(payload)
            con.execute("""
                INSERT INTO mission_journal (actor_id, event_type, payload)
                VALUES (?, ?, ?)
            """, (self.actor_id, event_type, payload_str))
            con.close()
            print(f"📝 [ACTOR-{self.actor_id}] Event Logged: {event_type}")
        except Exception as e:
            print(f"⚠️ [ACTOR-{self.actor_id}] Event Log Failed: {e}")

    def update_state(self, key: str, value: Any):
        """Updates a state key and persists immediately."""
        self.state[key] = value
        self.persist_state()
        self.log_event("STATE_UPDATE", {key: value})

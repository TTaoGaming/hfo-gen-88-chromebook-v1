# Medallion: Bronze | Mutation: 0% | HIVE: I
import sys
import os
from typing import Dict, Any

# Ensure we can import from the legacy base
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from versions.base import log_to_blackboard, get_last_thought
from ..ports.driven import PersistencePort

class BlackboardAdapter(PersistencePort):
    """Adapter for the existing .jsonl blackboard."""
    def log_event(self, entry: Dict[str, Any]):
        log_to_blackboard(entry)

    def read_last_event(self, phase: str) -> Dict[str, Any]:
        # Simple wrapper for now
        last_thought = get_last_thought()
        if last_thought.get("phase") == phase:
            return last_thought
        return {"status": "NOT_FOUND"}

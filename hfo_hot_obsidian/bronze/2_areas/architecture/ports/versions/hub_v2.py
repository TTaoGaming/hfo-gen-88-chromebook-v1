#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
import os
import json
import hashlib
import datetime
from .base import (
    Port0Observe, Port1Bridge, Port2Shape, Port3Inject, 
    Port4Disrupt, Port5Immunize, Port6Assimilate, Port7Navigate,
    BLACKBOARD_PATH, log_to_blackboard
)

class HubV2:
    """Version 2: Hot Bronze HIVE/8 Manifold with Prefect-style Flow Orchestration."""
    @staticmethod
    def _generate_session_id(query: str):
        return hashlib.sha256(query.encode()).hexdigest()[:12]

    @staticmethod
    def _rehydrate_session(session_id: str):
        print(f"🐝 [HUB-V2]: Rehydrating session {session_id} from blackboard...")
        thinking = {}
        states = {"H": "SCHEDULED", "I": "SCHEDULED", "V": "SCHEDULED", "E": "SCHEDULED"}
        if not os.path.exists(BLACKBOARD_PATH): return thinking, states
        try:
            with open(BLACKBOARD_PATH, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("session_id") == session_id and entry.get("hive_mode") == "HIVE/8_V2":
                        phase = entry.get("phase")
                        state = entry.get("state")
                        if phase in states and state == "COMPLETED":
                            states[phase] = "COMPLETED"
                            if "metrics" in entry: thinking.update(entry["metrics"])
        except Exception as e:
            print(f"⚠️ [REHYDRATE]: Failed to read blackboard: {e}")
        return thinking, states

    @staticmethod
    def run(query: str):
        session_id = HubV2._generate_session_id(query)
        print(f"🐝 [HUB-V2]: Initiating Stateful HIVE/8 Flow [Session: {session_id}]")
        thinking, states = HubV2._rehydrate_session(session_id)
        
        try:
            # Stage H: HUNT
            if states["H"] != "COMPLETED":
                states["H"] = "RUNNING"
                print(f"🐝 [FLOW]: Stage H (HUNT) -> Running")
                thinking["T0_OBSERVE"] = Port0Observe.execute_all(query)
                thinking["T7_NAVIGATE"] = Port7Navigate.execute_all(query)
                states["H"] = "COMPLETED"
                HubV2._sync_log(session_id, "H", states["H"], {"T0_OBSERVE": thinking["T0_OBSERVE"], "T7_NAVIGATE": thinking["T7_NAVIGATE"]})
            else:
                print(f"⏩ [FLOW]: Stage H (HUNT) -> Skipping")

            # Stage I: INTERLOCK
            if states["I"] != "COMPLETED":
                states["I"] = "RUNNING"
                print(f"🐝 [FLOW]: Stage I (INTERLOCK) -> Running")
                thinking["T1_BRIDGE"] = Port1Bridge.execute_all()
                thinking["T6_ASSIMILATE"] = Port6Assimilate.execute_all()
                states["I"] = "COMPLETED"
                HubV2._sync_log(session_id, "I", states["I"], {"T1_BRIDGE": thinking["T1_BRIDGE"], "T6_ASSIMILATE": thinking["T6_ASSIMILATE"]})
            else:
                print(f"⏩ [FLOW]: Stage I (INTERLOCK) -> Skipping")

            # Stage V: VALIDATE
            if states["V"] != "COMPLETED":
                states["V"] = "RUNNING"
                print(f"🐝 [FLOW]: Stage V (VALIDATE) -> Running")
                thinking["T2_SHAPE"] = Port2Shape.execute_all()
                thinking["T5_INTEGRITY"] = Port5Immunize.execute_all()
                states["V"] = "COMPLETED"
                HubV2._sync_log(session_id, "V", states["V"], {"T2_SHAPE": thinking["T2_SHAPE"], "T5_INTEGRITY": thinking["T5_INTEGRITY"]})
            else:
                print(f"⏩ [FLOW]: Stage V (VALIDATE) -> Skipping")

            # Stage E: EVOLVE
            if states["E"] != "COMPLETED":
                states["E"] = "RUNNING"
                print(f"🐝 [FLOW]: Stage E (EVOLVE) -> Running")
                thinking["T3_INJECT"] = Port3Inject.execute_all()
                thinking["T4_DISRUPT"] = Port4Disrupt.calculate_utility(states, thinking)
                states["E"] = "COMPLETED"
                HubV2._sync_log(session_id, "E", states["E"], {"T3_INJECT": thinking["T3_INJECT"], "T4_DISRUPT": thinking["T4_DISRUPT"]})
            else:
                print(f"⏩ [FLOW]: Stage E (EVOLVE) -> Skipping")

        except Exception as e:
            print(f"❌ [FLOW]: Critical Failure: {e}")
            for k, v in states.items():
                if v == "RUNNING": states[k] = "FAILED"
            log_to_blackboard({"session_id": session_id, "phase": "CRASH", "error": str(e), "states": states})
        return thinking

    @staticmethod
    def _sync_log(session_id: str, phase: str, state: str, data: dict):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_to_blackboard({
            "timestamp": now, "session_id": session_id, "phase": phase,
            "state": state, "hive_mode": "HIVE/8_V2", "metrics": data
        })

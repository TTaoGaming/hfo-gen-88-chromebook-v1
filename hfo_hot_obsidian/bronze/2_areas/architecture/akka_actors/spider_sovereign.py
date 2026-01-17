# Medallion: Bronze | Mutation: 0% | HIVE: I
try:
    from .navigator_actor import NavigatorActor
    from .bridger_actor import BridgerActor
    from .commander_actors import (
        LidlessLegion, MirrorMagus, HarmonicHydra, 
        RedRegnant, PyrePraetorian, KrakenKeeper
    )
except (ImportError, ValueError):
    from navigator_actor import NavigatorActor
    from bridger_actor import BridgerActor
    from commander_actors import (
        LidlessLegion, MirrorMagus, HarmonicHydra, 
        RedRegnant, PyrePraetorian, KrakenKeeper
    )
from typing import Dict, List, Any
import time
import sys
import os

# Add versions.base path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports")
from versions.base import log_to_blackboard

class SpiderSovereign:
    """
    Lord of Webs (Port 7 Facade).
    Orchestrates the 'Incarnated Commanders' across the 8 Ports.
    Provides a simplified interface for 24/7 orchestration.
    """
    def __init__(self):
        print("🕸️ [SPIDER-SOVEREIGN] Awakening Lord of Webs...")
        self.navigator = NavigatorActor()
        self.commanders = {
            "P0_SENSE": LidlessLegion(),          # Lidless Legion
            "P1_FUSE": BridgerActor(),            # Web Weaver
            "P2_SHAPE": MirrorMagus(),            # Mirror Magus
            "P3_DELIVER": HarmonicHydra(),        # Harmonic Hydra
            "P4_DISRUPT": RedRegnant(),           # Red Regnant
            "P5_DEFEND": PyrePraetorian(),        # Pyre Praetorian
            "P6_STORE": KrakenKeeper(),           # Kraken Keeper
            "P7_NAVIGATE": self.navigator         # Spider Sovereign itself
        }
        self.active_threads = ["ALPHA", "OMEGA"]

    def incarnate(self, port: str):
        """
        Activates a specific commander to perform its 'Chant' or task.
        """
        commander = self.commanders.get(port)
        if not commander:
            print(f"⚠️ [SPIDER-SOVEREIGN] Port {port} is not yet hydrated. Skipping incarnation.")
            return

        print(f"🕯️ [SPIDER-SOVEREIGN] Incarnating {port}...")
        
        # Manifestation: The 'Chant'
        # Each commander performs their specific duty based on their Port identity.
        chant_payload = {
            "timestamp": self._get_timestamp(),
            "actor": commander.actor_id,
            "port": port,
            "mission": "PHOENIX_REBIRTH",
            "message": f"Commander {commander.actor_id} is online and chanting."
        }
        
        # Log to Blackboard (Stigmergy)
        log_to_blackboard({
            "timestamp": chant_payload["timestamp"],
            "phase": "E", # Evolve/Emit
            "node": port,
            "status": "CHANTING",
            "output": chant_payload
        })
        
        # Log to Mission Journal (Persistence)
        commander.log_event("CHANT", chant_payload)
        
    def _get_timestamp(self) -> str:
        import datetime
        return datetime.datetime.now(datetime.timezone.utc).isoformat()
        
    def cycle(self):
        """
        Performs one full cycle of the HIVE/8:1010 pulse.
        """
        print(f"\n🌀 [SPIDER-SOVEREIGN] Starting Orchestration Cycle...")
        # 1. HUNT (P0, P7)
        self.incarnate("P0_SENSE")
        self.incarnate("P7_NAVIGATE")
        
        # 2. INTERLOCK (P1, P6)
        self.incarnate("P1_FUSE")
        self.incarnate("P6_STORE")
        
        # 3. VALIDATE (P2, P5)
        self.incarnate("P2_SHAPE")
        self.incarnate("P5_DEFEND")
        
        # 4. EVOLVE (P3, P4)
        self.incarnate("P3_DELIVER")
        self.incarnate("P4_DISRUPT")
        
        print("🏁 [SPIDER-SOVEREIGN] Cycle Complete.\n")

    def seek_guidance(self, query: str) -> Dict[str, Any]:
        """
        Interactive interface to chat with the Lord of Webs concept.
        Routes the query through HubV8 for a holographic response.
        """
        print(f"🕯️ [SPIDER-SOVEREIGN] Lord of Webs is listening to your plea: '{query}'")
        
        # We'll use the HubV8 registry if available
        # sys.path.append is already mostly handled in base/hub, but we ensure it here
        sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports")
        try:
            from hfo_orchestration_hub import HUB_REGISTRY
            hub_class = HUB_REGISTRY.get("8")
            if hub_class:
                # We need to run HubV8's async logic
                import asyncio
                print("🕸️ [SPIDER-SOVEREIGN] Consulting the Oracle (HubV8)...")
                result = asyncio.run(hub_class.async_run(query))
                return result
            else:
                return {"status": "ERROR", "message": "HubV8 Registry not found."}
        except Exception as e:
            return {"status": "ERROR", "message": f"Guidance Failed: {e}"}

    def run_247(self, interval_seconds: int = 60):
        """
        The 24/7 Heartbeat.
        """
        print(f"💓 [SPIDER-SOVEREIGN] Heartbeat activated. Pulse every {interval_seconds}s.")
        try:
            while True:
                self.cycle()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("🛑 [SPIDER-SOVEREIGN] Hibernating Lord of Webs...")

if __name__ == "__main__":
    sovereign = SpiderSovereign()
    # Test a single cycle
    sovereign.cycle()

# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os

# Ensure the library path is correct for local imports
# We add the specific directory to path to avoid the "2_areas" import issue
actor_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../hfo_hot_obsidian/bronze/2_areas/architecture/akka_actors'))
sys.path.append(actor_dir)

from base_actor import HardenedBaseActor

def test_alpha_actor():
    print("🚀 Initializing Test Actor...")
    actor = HardenedBaseActor(actor_id="P7_PRIME_TEST", mission_thread="ALPHA")
    
    # Test State Update
    print("🔄 Updating State...")
    actor.update_state("heartbeat", "PULSE_8_1_8_1")
    actor.update_state("mode", "HIVE_ACTIVE")
    
    # Test Event Logging
    print("📝 Logging Custom Event...")
    actor.log_event("MISSION_INIT", {"objective": "BOOTSTRAP_ALPHA"})
    
    # Verify Persistence (Reload state)
    print("🔍 Verifying Persistence (Reloading Actor)...")
    reloaded_actor = HardenedBaseActor(actor_id="P7_PRIME_TEST", mission_thread="ALPHA")
    
    if reloaded_actor.state.get("heartbeat") == "PULSE_8_1_8_1":
        print("✅ SUCCESS: State persistence verified in DuckDB.")
    else:
        print("❌ FAILURE: State mismatch after reload.")
        print(f"Current State: {reloaded_actor.state}")

if __name__ == "__main__":
    test_alpha_actor()

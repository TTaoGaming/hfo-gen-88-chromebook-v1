#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
import sys
import os

# Add the actors directory to path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/akka_actors")
try:
    from spider_sovereign import SpiderSovereign
except ImportError as e:
    print(f"❌ Failed to import SpiderSovereign: {e}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 seek_guidance.py \"Your query to the Lord of Webs\"")
        return

    query = " ".join(sys.argv[1:])
    sovereign = SpiderSovereign()
    
    print("\n🕸️  Lord of Webs is weaving a response...")
    result = sovereign.seek_guidance(query)
    
    # Check if result is a Baton
    if isinstance(result, dict) and "baton" in result:
        baton = result["baton"]
        print(f"\n✨ [HFO BATON - {result.get('status', 'STUB')}]")
        print(f"Summary: {baton.get('summary')}")
        payload = baton.get("payload", {})
        print(f"Mosaic Map: {payload.get('mosaic_map')}")
        print("Key Signals:")
        for sig in payload.get("key_nav_signals", []):
            print(f" - {sig}")
    else:
        print(f"\n🔮 [RESPONSE]: {result}")

if __name__ == "__main__":
    main()

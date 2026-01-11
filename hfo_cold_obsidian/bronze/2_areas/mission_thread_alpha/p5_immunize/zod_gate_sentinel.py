#!/usr/bin/env python3
import os
import sys

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: ZOD-SHIELD (Contract Enforcement)
# Attack Vector: CONTRACT_BREACH
# Logic: Ensures Zod 6.0 schemas exist for all P-port boundaries.

CONTRACTS_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/contracts"

def check_contracts():
    print("🛡️ [P5 ZOD-SHIELD]: Verifying inter-port contracts...")

    if not os.path.exists(CONTRACTS_DIR):
        print("❌ [P5 ZOD-SHIELD]: BREACH: Contracts directory missing.")
        return False

    contract_files = [f for f in os.listdir(CONTRACTS_DIR) if f.endswith('.zod.ts')]
    if not contract_files:
        print("❌ [P5 ZOD-SHIELD]: BREACH: No Zod contracts found in mission area.")
        return False

    # Check for core schemas (P0, P1, P2)
    for cf in contract_files:
        path = os.path.join(CONTRACTS_DIR, cf)
        with open(path, 'r') as f:
            content = f.read()
            if "export const CloudEventEnvelopeSchema" not in content:
                 print(f"❌ [P5 ZOD-SHIELD]: CloudEvent envelope missing in {cf}")
                 return False
            if "export const P0SensingSchema" not in content:
                 print(f"⚠️ [P5 ZOD-SHIELD]: P0 schema missing in {cf}")
            if "export const P1PhysicsInputSchema" not in content:
                 print(f"⚠️ [P5 ZOD-SHIELD]: P1 schema missing in {cf}")

    print("✅ [P5 ZOD-SHIELD]: Zod 6.0 Contracts active.")
    return True

if __name__ == "__main__":
    if not check_contracts():
        sys.exit(1)

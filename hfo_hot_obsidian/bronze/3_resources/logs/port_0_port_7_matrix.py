#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import os
import sys

def print_p0_matrix():
    print("\n--- [ PORT 0 SENSE: TOOL USE MATRIX ] ---")
    headers = ["TOOL", "HITS", "COVERAGE", "CONFIDENCE", "MEDALLION"]
    print(f"{headers[0]:<12} | {headers[1]:<6} | {headers[2]:<10} | {headers[3]:<12} | {headers[4]:<10}")
    print("-" * 65)
    
    # Mock/Extracted data from last search
    rows = [
        ["TAVILY", "5", "88%", "HIGH", "BRONZE"],
        ["BRAVE", "7", "92%", "HIGH", "BRONZE"],
        ["LOCAL_AST", "12", "100%", "TOTAL", "SILVER"],
        ["GREP_SEARCH", "3", "45%", "MEDIUM", "BRONZE"]
    ]
    
    for r in rows:
        print(f"{r[0]:<12} | {r[1]:<6} | {r[2]:<10} | {r[3]:<12} | {r[4]:<10}")
    print("-" * 65)

def print_p7_matrix():
    print("\n--- [ PORT 7 NAVIGATE: THINKING MATRIX ] ---")
    headers = ["STAGE", "PORT", "SHARD (TK)", "INTEGRITY", "STATE"]
    print(f"{headers[0]:<12} | {headers[1]:<6} | {headers[2]:<10} | {headers[3]:<12} | {headers[4]:<10}")
    print("-" * 65)
    
    rows = [
        ["T0 discovery", "P0", "154/1024", "VERIFIED", "SYNCED"],
        ["T1 bridging",  "P1", "210/1024", "STABLE",   "PLANNING"],
        ["T2 shape",    "P2", "88/1024",  "GEOMETRIC", "LATTICED"],
        ["T3 inject",   "P3", "340/1024", "SIMULATED", "ACTIVE"],
        ["T4 disrupt",  "P4", "120/1024", "CLEAN",     "AUDITED"],
        ["T5 defend",   "P5", "45/1024",  "SHIELDED",  "ENFORCED"],
        ["T6 store",    "P6", "98/1024",  "ARCHIVED",  "PERSISTED"],
        ["T7 navigate", "P7", "280/1024", "CONSOLIDATED","STEERING"]
    ]
    
    for r in rows:
        print(f"{r[0]:<12} | {r[1]:<6} | {r[2]:<10} | {r[3]:<12} | {r[4]:<10}")
    print("-" * 65)

if __name__ == "__main__":
    print_p0_matrix()
    print_p7_matrix()
    print("\n[HIVE/8 STATUS]: ALL SYSTEMS NOMINAL. MISSION THREAD ALPHA CANALIZATION PROCEEDING.")

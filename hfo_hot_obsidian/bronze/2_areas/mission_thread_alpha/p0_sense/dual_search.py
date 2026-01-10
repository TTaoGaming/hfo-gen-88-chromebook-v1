#!/usr/bin/env python3
import os
import sys
import json
import requests
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: H
# P0 SENSE: Dual Search (Tavily + Brave) Mandatory Tool
# Enforces the H-Phase requirement for external sensing.

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def search_tavily(query, api_key):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced"
    }
    response = requests.post(url, json=payload)
    return response.json()

def search_brave(query, api_key):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def log_receipt(query, tavily_res, brave_res):
    receipt_id = f"DUAL_SEARCH_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "phase": "H",
        "summary": f"H-Phase Dual Search Complete: {query[:30]}...",
        "p0": {
            "status": "sensing",
            "query": query,
            "receipt": receipt_id,
            "sources": ["Tavily", "Brave"]
        },
        "p7": {"status": "routing"}
    }

    with open(BLACKBOARD_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return receipt_id

def main():
    if len(sys.argv) < 2:
        print("Usage: dual_search.py '<query>'")
        sys.exit(1)

    query = sys.argv[1]
    tavily_key = os.getenv("TAVILY_API_KEY")
    brave_key = os.getenv("BRAVE_API_KEY")

    if not tavily_key or not brave_key:
        print("❌ [P0 ERROR]: Missing API keys (TAVILY_API_KEY or BRAVE_API_KEY)")
        sys.exit(1)

    print(f"🔍 [P0 SENSE]: Initializing Dual Search for: {query}")

    try:
        t_results = search_tavily(query, tavily_key)
        b_results = search_brave(query, brave_key)

        receipt = log_receipt(query, t_results, b_results)
        print(f"✅ [P0 SENSE]: Search Complete. Receipt: {receipt}")

    except Exception as e:
        print(f"❌ [P0 ERROR]: Search failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

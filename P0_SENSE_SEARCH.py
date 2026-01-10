#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: H
# P0-SENSE Hunt Tool: Dual Search (Tavily + Brave)

def load_env():
    env_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        key, value = parts
                        os.environ[key] = value

def search_tavily(query, api_key):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced"
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def search_brave(query, api_key):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    params = {"q": query}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    load_env()
    tavily_key = os.getenv("TAVILY_API_KEY")
    brave_key = os.getenv("BRAVE_API_KEY")

    query = "@mediapipe/tasks-vision vision_bundle.js script global name for FilesetResolver and GestureRecognizer"

    print(f"🔍 [P0-SENSE]: Searching Tavily...")
    tavily_results = search_tavily(query, tavily_key)

    print(f"🔍 [P0-SENSE]: Searching Brave...")
    brave_results = search_brave(query, brave_key)

    output = {
        "query": query,
        "tavily": tavily_results,
        "brave": brave_results,
        "timestamp": datetime.now().isoformat()
    }

    with open("P0_SENSE_search_results.json", "w") as f:
        json.dump(output, f, indent=2)

    # PORT 5 COMPLIANCE: Log to Blackboard
    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    receipt = f"P0_SENSE_SEARCH_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "phase": "H",
        "summary": f"P0-Sense Hunt: {query}",
        "p0": {
            "status": "complete",
            "query": query,
            "receipt": receipt,
            "data": {
                "web_tavily": tavily_results.get("results", []) if isinstance(tavily_results, dict) else [],
                "web_brave": brave_results.get("web", {}).get("results", []) if isinstance(brave_results, dict) else []
            }
        }
    }
    with open(blackboard_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"✅ [P0-SENSE]: Logged to Blackboard with receipt: {receipt}")

if __name__ == "__main__":
    main()

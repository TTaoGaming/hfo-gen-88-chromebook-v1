#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
� PORT 0 TOOLS: SENSE Infrastructure
Consolidates 8 high-fidelity sensing pillars for Apex Mission Engineering.
Failure in any pillar triggers a 'SCREAM' event.
"""

import os
import json
import sys
import datetime
from typing import List, Dict, Any

# 🏗️ Import Sensing Pillars
import arxiv
import wikipedia
import subprocess
import requests
from tavily import TavilyClient
from local_repo_indexer import RepoIndexer
from doc_denaturizer import Denaturizer

def scream(pillar_name: str, error_msg: str):
    """Loudly report a pillar failure to stderr and logs."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    scream_msg = f"‼️ [PORT 0 SCREAM] Pillar '{pillar_name}' FAILED: {error_msg}"
    sys.stderr.write(scream_msg + "\n")

    # Log scream to blackboard for P5/P7 visibility
    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    entry = {
        "timestamp": timestamp,
        "phase": "P4_DISRUPT",
        "summary": f"SCREAM: Pillar '{pillar_name}' Failure",
        "p0": {"status": "SCREAMING", "pillar": pillar_name, "error": error_msg}
    }
    with open(blackboard_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_env_manual():
    """Manually parse .env from root."""
    env_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        key, val = parts
                        os.environ[key] = val.strip('"').strip("'")

def search_tavily(query: str):
    """Pillar 1: Tavily"""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        scream("Tavily", "Missing TAVILY_API_KEY in .env")
        return None
    try:
        tavily = TavilyClient(api_key=key)
        response = tavily.search(query=query, search_depth="basic", max_results=3)
        return response.get('results', [])
    except Exception as e:
        scream("Tavily", str(e))
        return None

def search_brave(query: str):
    """Pillar 2: Brave"""
    key = os.getenv("BRAVE_API_KEY")
    if not key:
        scream("Brave", "Missing BRAVE_API_KEY in .env")
        return None
    try:
        headers = {"Accept": "application/json", "X-Subscription-Token": key}
        response = requests.get(f"https://api.search.brave.com/res/v1/web/search?q={query}&count=3", headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('web', {}).get('results', [])
    except Exception as e:
        scream("Brave", str(e))
        return None

def sense_stigmergy():
    """Pillar 3: Stigmergy (Hot/Cold Blackboards)"""
    paths = {
        "hot": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl",
        "cold": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/cold_obsidian_blackboard.jsonl"
    }
    results = {}
    for key, path in paths.items():
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    # Reading the end of the file efficiently
                    f.seek(0, 2)
                    size = f.tell()
                    # We only need the last few KB usually
                    f.seek(max(0, size - 10240))
                    chunk = f.read()
                    lines = [l for l in chunk.splitlines() if l.strip()]
                    count = 5 if key == "hot" else 3
                    tail = [json.loads(l) for l in lines[-count:]]
                    results[key] = tail
            else:
                results[key] = f"MISSING: {path}"
        except Exception as e:
            scream(f"Stigmergy {key}", str(e))
            results[key] = None
    return results

def sense_local_repo(query: str):
    """Pillar 4: Local Repo Indexer"""
    try:
        indexer = RepoIndexer("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
        # For query, we'll try to find if it matches a symbol
        symbol = indexer.find_symbol(query)
        return symbol if symbol else {"status": "no_direct_symbol_match"}
    except Exception as e:
        scream("Local Repo Indexer", str(e))
        return None

def denaturize_docs(url: str):
    """Pillar 5: Doc Denaturizer"""
    try:
        if not url.startswith("http"): return None
        return Denaturizer.fetch_and_clean(url)
    except Exception as e:
        scream("Doc Denaturizer", str(e))
        return None

def search_arxiv(query: str):
    """Pillar 6: Arxiv"""
    if not query.strip() or len(query) > 300: return None
    try:
        # Arxiv is sensitive to long or weird queries
        safe_query = query[:200]
        client = arxiv.Client()
        search = arxiv.Search(query=safe_query, max_results=3, sort_by=arxiv.SortCriterion.Relevance)
        results = client.results(search)
        return [{"title": r.title, "summary": r.summary[:200] + "...", "url": r.pdf_url} for r in results]
    except Exception as e:
        scream("Arxiv", str(e))
        return None

def search_wiki(query: str):
    """Pillar 7: Wikipedia"""
    try:
        wikipedia.set_lang("en")
        results = wikipedia.search(query)
        if results:
            summary = wikipedia.summary(results[0], sentences=2)
            return {"title": results[0], "summary": summary, "url": f"https://en.wikipedia.org/wiki/{results[0].replace(' ', '_')}"}
        return None
    except Exception as e:
        scream("Wikipedia", str(e))
        return None

def get_git_context():
    """Pillar 8: Local Git Context"""
    try:
        git_log = subprocess.check_output(["git", "log", "-n", "3", "--oneline"], text=True)
        return git_log.splitlines()
    except Exception as e:
        scream("Local Git context", str(e))
        return None

def port_0_sense(query: str):
    load_env_manual()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt_id = f"P0_SENSE_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"📡 Port 0 Tools - Sensing: {query}")

    data = {
        "p1_tavily": search_tavily(query),
        "p2_brave": search_brave(query),
        "p3_stigmergy": sense_stigmergy(),
        "p4_repo": sense_local_repo(query),
        "p5_docs": denaturize_docs(query) if query.startswith("http") else "N/A",
        "p6_arxiv": search_arxiv(query),
        "p7_wiki": search_wiki(query),
        "p8_git": get_git_context()
    }

    # Meta
    total_chars = len(json.dumps(data))

    entry = {
        "timestamp": timestamp,
        "phase": "H",
        "summary": f"Port 0 Sense: {query[:30]}",
        "p0": {
            "status": "complete",
            "query": query,
            "receipt": receipt_id,
            "payload_meta": {"chars": total_chars, "tokens": total_chars // 4},
            "data": data
        }
    }

    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    with open(blackboard_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"✅ Port 0 Sense Complete. Receipt: {receipt_id}")
    return receipt_id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: port_0_tools.py 'query'")
        sys.exit(1)
    port_0_sense(sys.argv[1])

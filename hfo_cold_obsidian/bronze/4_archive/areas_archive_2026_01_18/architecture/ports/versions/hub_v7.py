#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: H
"""
Hub V7: H-PHASE HUNT COMMANDER (8-1-8-1 BFT DOUBLE DIAMOND)
Pattern: Scatter(8 Tools) -> Gather(1 BFT Baton) -> Scatter(8 LLM Navs) -> Gather(1 BFT Baton)
Total LLM Calls: 10
"""

import os
import json
import asyncio
import hashlib
import datetime
import requests
from typing import List, Dict, Any, Set
from .base import (
    Port0ObserveV2, Port7Navigate,
    BLACKBOARD_PATH, log_to_blackboard, load_env
)

class WorkflowNode:
    def __init__(self, name: str, func, dependencies: List[str] = None):
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.state = "SCHEDULED"  # SCHEDULED, RUNNING, COMPLETED, FAILED
        self.output = None

class HubV7:
    """Version 7: H-Phase Hunt Commander with 8-1-8-1 BFT Double Diamond Orchestration."""
    
    @staticmethod
    def _generate_session_id(query: str):
        return hashlib.sha256(query.encode()).hexdigest()[:12]

    @staticmethod
    async def _execute_node(session_id: str, node: WorkflowNode, query: str, deps: Dict[str, WorkflowNode] = None):
        print(f"📡 [HUB-V7]: Starting node {node.name}...")
        try:
            import inspect
            
            # Context injection logic for P7 shards
            def wrapper():
                if deps:
                    # If this is a P7 shard, it might need the Sensing Baton from BATON_Port0
                    if "BATON_Port0" in deps and "Port7" in node.name:
                        sensing_baton = deps["BATON_Port0"].output
                        return node.func(query, deps=deps, context=json.dumps(sensing_baton))
                    try:
                        return node.func(query, deps)
                    except TypeError:
                        return node.func(query)
                return node.func(query)
            
            output = await asyncio.to_thread(wrapper)
            
            if inspect.iscoroutine(output):
                output = await output
            
            node.output = output
            
            # --- ADVERSARIAL THEATER DETECTION ---
            if isinstance(output, dict):
                content_str = str(output).lower()
                if any(x in content_str for x in ["placeholder", "stub", "todo", "ai theater"]):
                    output["ADVERSARIAL_THEATER"] = True
                    output["INTEGRITY_SIGNAL"] = "RED_TRUTH"
                    print(f"🚩 [HUB-V7]: ADVERSARIAL THEATER DETECTED in {node.name}")

            node.state = "COMPLETED"
            
            log_to_blackboard({
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                "session_id": session_id,
                "hive_mode": "HIVE/8_V7_HUNT",
                "node": node.name,
                "state": "COMPLETED",
                "output": output
            })
            print(f"✅ [HUB-V7]: Node {node.name} finished.")
        except Exception as e:
            node.state = "FAILED"
            node.output = {"error": str(e)}
            print(f"❌ [HUB-V7]: Node {node.name} FAILED: {e}")

    @staticmethod
    async def dispatch_synthesis(query: str, pheromones: Dict[str, Any], stage: str):
        """
        Generic synthesis call to OpenRouter.
        stage: 'Port0' (Diamond 1 Sensing) or 'Port7' (Diamond 2 Strategy)
        """
        load_env()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return {"error": "OPENROUTER_API_KEY not found"}

        # HFO Holographic Mapping
        mission_role = "Lidless Legion Sensing (Diamond 1)" if stage == "Port0" else "Spider Sovereign Navigation (Diamond 2)"
        
        prompt = f"""
        You are the HFO Hive/8 {mission_role} - HUB V6 (BFT-Aware Orchestrator).
        Target: H-Phase Hunt Expansion (Double Diamond) with Byzantine Fault Tolerance (BFT).

        GALOIS LATTICE ALIGNMENT:
        Every shard maps to its [Verb, Domain] coordinate. Synthesize these 'Mosaic Tiles' into a unified BFT BATON.

        BFT SYSTEM PARAMETERS:
        - Network Size (n): 8 agents
        - Fault Tolerance (f): 2 (System handles 3f+1 where n=8)
        - Quorum Threshold: 6/8 (75%) consensus. (Target consensus score: 78).

        QUERY: {query}

        PHEROMONES (Shard Data):
        {json.dumps(pheromones, indent=2)}

        BFT ANALYSIS TASK:
        1. CONVERGENCE: Identify signals present in 6 or more shards.
        2. DIVERGENCE: Identify signals that are unique, conflicting, or contradictory.
        3. QUORUM AUDIT: Explicitly state if we have at least 6 shards (n-f) agreeing on the core mission objective.
        4. ADVERSARIAL DETECTION & THEATER AUDIT: 
           - Flag any shards providing erroneous, stalled, or "hallucinated" data (e.g. error messages or empty stubs where results were expected).
           - Identify "ADVERSARIAL THEATER": Shards claiming "READY" or "PASS" when they are actually returning placeholders or deterministic stubs.
           - POLICY: VERIFIABLE TRUTH RED > MEANINGLESS GREEN. A confirmed failure (Red) is a 100% valid mission signal. A fake success (Green) is an adversarial attack.

        OUTPUT FORMAT (STRICT JSON):
        {{
            "artifact_id": "Baton_{stage}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "GREEN",
            "bft_metrics": {{
                "consensus_score": 0.0,
                "quorum_reached": true,
                "convergence_summary": "Summary of matching majority signals",
                "divergence_report": "Summary of minority/conflicting signals",
                "faulty_nodes": ["shard_name"]
            }},
            "baton": {{
                "summary": "Condensation of the holographic state.",
                "payload": {{
                    "mosaic_map": "Brief description of how the tiles fit together.",
                    "key_nav_signals": ["Signal 1", "Signal 2"]
                }}
            }}
        }}
        """

        def call_api():
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    data=json.dumps({
                        "model": "google/gemma-3-27b-it",
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": { "type": "json_object" }
                    })
                )
                return response.json()
            except Exception as e: return {"error": str(e)}

        result = await asyncio.to_thread(call_api)
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]
            try:
                if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
                return json.loads(content)
            except: return {"error": "JSON Parse Failed", "raw": content}
        return {"error": "Synthesis failed", "response": result}

    @staticmethod
    def run(query: str):
        return asyncio.run(HubV7.async_run(query))

    @staticmethod
    async def async_run(query: str):
        session_id = HubV7._generate_session_id(query)
        print(f"🛰️ [HUB-V7]: Initiating 8-1-8-1 BFT Double Diamond [Session: {session_id}]")
        
        # DIAMOND 1: SENSING (PORT 0)
        nodes = {
            "P0_shard0": WorkflowNode("P0_shard0", lambda q: Port0ObserveV2.port0_shard0_observe(q)),
            "P0_shard1": WorkflowNode("P0_shard1", lambda q: Port0ObserveV2.port0_shard1_bridge(q)),
            "P0_shard2": WorkflowNode("P0_shard2", lambda q: Port0ObserveV2.port0_shard2_shape(q)),
            "P0_shard3": WorkflowNode("P0_shard3", lambda q: Port0ObserveV2.port0_shard3_inject(q)),
            "P0_shard4": WorkflowNode("P0_shard4", lambda q: Port0ObserveV2.port0_shard4_disrupt(q)),
            "P0_shard5": WorkflowNode("P0_shard5", lambda q: Port0ObserveV2.port0_shard5_immunize(q)),
            "P0_shard6": WorkflowNode("P0_shard6", lambda q: Port0ObserveV2.port0_shard6_assimilate_v2(q)),
            "P0_shard7": WorkflowNode("P0_shard7", lambda q: Port0ObserveV2.port0_shard7_navigate(q)),

            "BATON_Port0": WorkflowNode("BATON_Port0", 
                lambda q, deps: HubV7.dispatch_synthesis(q, {k: v.output for k, v in deps.items()}, "Port0"),
                dependencies=["P0_shard0", "P0_shard1", "P0_shard2", "P0_shard3", "P0_shard4", "P0_shard5", "P0_shard6", "P0_shard7"]),

            # DIAMOND 2: STRATEGY (PORT 7)
            # These shards now wait for the BATON_Port0 baton
            "Port7_shard0": WorkflowNode("Port7_shard0", lambda q, deps=None, context="": Port7Navigate.port7_shard0_observe(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard1": WorkflowNode("Port7_shard1", lambda q, deps=None, context="": Port7Navigate.port7_shard1_bridge(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard2": WorkflowNode("Port7_shard2", lambda q, deps=None, context="": Port7Navigate.port7_shard2_shape(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard3": WorkflowNode("Port7_shard3", lambda q, deps=None, context="": Port7Navigate.port7_shard3_inject(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard4": WorkflowNode("Port7_shard4", lambda q, deps=None, context="": Port7Navigate.port7_shard4_disrupt(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard5": WorkflowNode("Port7_shard5", lambda q, deps=None, context="": Port7Navigate.port7_shard5_immunize(deps["BATON_Port0"].output, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard6": WorkflowNode("Port7_shard6", lambda q, deps=None, context="": Port7Navigate.port7_shard6_assimilate(q, context=context), dependencies=["BATON_Port0"]),
            "Port7_shard7": WorkflowNode("Port7_shard7", lambda q, deps=None, context="": Port7Navigate.port7_shard7_navigate(q, context=context), dependencies=["BATON_Port0"]),

            "BATON_Port7": WorkflowNode("BATON_Port7", 
                lambda q, deps: HubV7.dispatch_synthesis(q, {k: v.output for k, v in deps.items()}, "Port7"),
                dependencies=["Port7_shard0", "Port7_shard1", "Port7_shard2", "Port7_shard3", "Port7_shard4", "Port7_shard5", "Port7_shard6", "Port7_shard7"])
        }

        completed_nodes = set()
        while len(completed_nodes) < len(nodes):
            executable = [n for n in nodes.values() if n.state == "SCHEDULED" and all(d in completed_nodes for d in n.dependencies)]
            if not executable: break
            
            print(f"🚀 [V7]: ExecBatch: {[n.name for n in executable]}")
            tasks = [HubV7._execute_node(session_id, n, query, {d: nodes[d] for d in n.dependencies} if n.dependencies else None) for n in executable]
            await asyncio.gather(*tasks)
            for n in executable:
                if n.state == "COMPLETED": 
                    # --- BFT QUORUM AUDIT ---
                    if "BATON" in n.name and isinstance(n.output, dict):
                        bft = n.output.get("bft_metrics", {})
                        if bft:
                            reached = bft.get("quorum_reached", False)
                            score = bft.get("consensus_score", 0)
                            print(f"⚖️ [HUB-V7]: BFT Quorum Audit ({n.name}): {'✅ PASS' if reached else '❌ FAIL'} (Score: {score})")
                            log_to_blackboard({
                                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                                "phase": "BFT_AUDIT",
                                "node": n.name,
                                "quorum_reached": reached,
                                "consensus_score": score,
                                "details": bft
                            })
                    completed_nodes.add(n.name)

        return nodes["BATON_Port7"].output

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Status check"
    print(json.dumps(HubV7.run(query), indent=2))

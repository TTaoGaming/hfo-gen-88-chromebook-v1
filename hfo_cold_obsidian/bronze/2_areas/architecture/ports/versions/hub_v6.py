#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: H
"""
Hub V6: H-PHASE HUNT COMMANDER (8-1-8-1 DOUBLE DIAMOND)
Pattern: Scatter(P0) -> Gather(Sensing) -> Scatter(P7) -> Gather(Strategy)
Signal: Fractal Octree Resonance Alpha
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

class HubV6:
    """Version 6: H-Phase Hunt Commander with 8-1-8-1 Double Diamond Orchestration."""
    
    @staticmethod
    def _generate_session_id(query: str):
        return hashlib.sha256(query.encode()).hexdigest()[:12]

    @staticmethod
    async def _execute_node(session_id: str, node: WorkflowNode, query: str, deps: Dict[str, WorkflowNode] = None):
        print(f"📡 [HUB-V6]: Starting node {node.name}...")
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
            node.state = "COMPLETED"
            
            log_to_blackboard({
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                "session_id": session_id,
                "hive_mode": "HIVE/8_V6_HUNT",
                "node": node.name,
                "state": "COMPLETED",
                "output": output
            })
            print(f"✅ [HUB-V6]: Node {node.name} finished.")
        except Exception as e:
            node.state = "FAILED"
            node.output = {"error": str(e)}
            print(f"❌ [HUB-V6]: Node {node.name} FAILED: {e}")

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
        You are the HFO Hive/8 {mission_role} - HUB V6.
        Target: H-Phase Hunt Expansion (Double Diamond).

        GALOIS LATTICE ALIGNMENT:
        This is a fractal system. Every shard must map to its [Verb, Domain] coordinate in the Galois Lattice.
        Synthesize these 'Mosaic Tiles' into a unified BATON.

        QUERY: {query}

        PHEROMONES (Mosaic Tiles):
        {json.dumps(pheromones, indent=2)}

        OUTPUT FORMAT (STRICT JSON):
        {{
            "artifact_id": "Baton_{stage}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "GREEN",
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
        return asyncio.run(HubV6.async_run(query))

    @staticmethod
    async def async_run(query: str):
        session_id = HubV6._generate_session_id(query)
        print(f"🛰️ [HUB-V6]: Initiating 8-1-8-1 Double Diamond [Hunt Phase] [Session: {session_id}]")
        
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
                lambda q, deps: HubV6.dispatch_synthesis(q, {k: v.output for k, v in deps.items()}, "Port0"),
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
                lambda q, deps: HubV6.dispatch_synthesis(q, {k: v.output for k, v in deps.items()}, "Port7"),
                dependencies=["Port7_shard0", "Port7_shard1", "Port7_shard2", "Port7_shard3", "Port7_shard4", "Port7_shard5", "Port7_shard6", "Port7_shard7"])
        }

        completed_nodes = set()
        while len(completed_nodes) < len(nodes):
            executable = [n for n in nodes.values() if n.state == "SCHEDULED" and all(d in completed_nodes for d in n.dependencies)]
            if not executable: break
            
            print(f"🚀 [V6]: ExecBatch: {[n.name for n in executable]}")
            tasks = [HubV6._execute_node(session_id, n, query, {d: nodes[d] for d in n.dependencies} if n.dependencies else None) for n in executable]
            await asyncio.gather(*tasks)
            for n in executable:
                if n.state == "COMPLETED": completed_nodes.add(n.name)

        return nodes["BATON_Port7"].output

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Status check"
    print(json.dumps(HubV6.run(query), indent=2))

#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
Hub V5: ENHANCED SCATTER-GATHER ORCHESTRATOR
Pattern: Scatter (8 Tools) -> Gather (1 LLM Artifact)
Signal: Port 0 V2 (Resilient Octet) Integration
"""

import os
import json
import asyncio
import hashlib
import datetime
import requests
from typing import List, Dict, Any, Set
from .base import (
    Port0ObserveV2, Port1Bridge, Port2Shape, Port3Inject, 
    Port4Disrupt, Port5Immunize, Port6Assimilate, Port7Navigate,
    BLACKBOARD_PATH, log_to_blackboard, load_env
)

class WorkflowNode:
    def __init__(self, name: str, func, dependencies: List[str] = None):
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.state = "SCHEDULED"  # SCHEDULED, RUNNING, COMPLETED, FAILED
        self.output = None

class HubV5:
    """Version 5: Enhanced Scatter-Gather Orchestrator with Port 0 V2."""
    
    @staticmethod
    def _generate_session_id(query: str):
        return hashlib.sha256(query.encode()).hexdigest()[:12]

    @staticmethod
    async def _execute_node(session_id: str, node: WorkflowNode, query: str, deps: Dict[str, WorkflowNode] = None):
        print(f"📡 [HUB-V5]: Starting node {node.name}...")
        try:
            import inspect
            
            # Execute in thread to avoid blocking loop if it's sync
            def wrapper():
                if deps: return node.func(query, deps)
                return node.func(query)
            
            output = await asyncio.to_thread(wrapper)
            
            # If the sync wrapper returned a coroutine (because func was async), await it
            if inspect.iscoroutine(output):
                output = await output
            
            node.output = output
            node.state = "COMPLETED"
            
            # Log to blackboard as a persistent receipt
            log_to_blackboard({
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                "session_id": session_id,
                "hive_mode": "HIVE/8_V5_SCATTER",
                "node": node.name,
                "state": "COMPLETED",
                "output": output,
                "latency_ms": 0 # Placeholder
            })
            print(f"✅ [HUB-V5]: Node {node.name} finished.")
        except Exception as e:
            node.state = "FAILED"
            node.output = {"error": str(e)}
            print(f"❌ [HUB-V5]: Node {node.name} FAILED: {e}")

    @staticmethod
    async def run_gather(deps: Dict[str, WorkflowNode], query: str = ""):
        """Synthesizes all outputs into a final artifact."""
        pheromones = {name: node.output for name, node in deps.items()}
        
        # 🎯 PORT 7_shard3: NAVIGATE_INJECT (Thinking)
        print("📡 [HUB-V5]: Port 7 Sequential Thinking engaged...")
        thinking = Port7Navigate.port7_shard3_inject(query, context=json.dumps(pheromones)[:2000]) 
        pheromones["P7_THINKING"] = thinking

        # Calculate Transparency Index: (Success Nodes / Total Nodes)
        success_count = sum(1 for node in deps.values() if node.state == "COMPLETED" and "error" not in str(node.output).lower() and "degraded" not in str(node.output).lower())
        total_count = len(deps)
        transparency_index = round(success_count / total_count, 2)
        
        # Self-Semantic Anchoring: Map internal pheromones to Fractal Octree
        fractal_pheromones = {}
        for k, v in pheromones.items():
            if "OBSERVE" in k:
                # Map P0_OBSERVE_TAVILY to Port0_shard0
                shard_map = {
                    "TAVILY": "Port0_shard0", "ARXIV": "Port0_shard1", "DDG": "Port0_shard2",
                    "GITHUB": "Port0_shard3", "REPO": "Port0_shard4", "BLACKBOARD": "Port0_shard5",
                    "WIKI": "Port0_shard6", "AGENTS": "Port0_shard7"
                }
                for key, val in shard_map.items():
                    if key in k: fractal_pheromones[val] = v
            elif "NAVIGATE" in k:
                # Port 7 is already sharded in execute_all
                if isinstance(v, dict): fractal_pheromones.update(v)
            else:
                fractal_pheromones[k] = v

        return await HubV5.dispatch_openrouter_gather(fractal_pheromones, transparency_index)

    @staticmethod
    async def dispatch_openrouter_gather(pheromones: Dict[str, Any], transparency_index: float):
        """
        Synthesizes tool outputs using OpenRouter (Gemma-3-27B).
        Creates a 'Handoff Baton' (Standardized Artifact).
        """
        load_env()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return {"error": "OPENROUTER_API_KEY not found"}

        # Load Mission Capsule (Architecture Context)
        mission_capsule = {}
        capsule_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mission_capsule.json")
        try:
            with open(capsule_path, "r") as f:
                mission_capsule = json.load(f)
        except Exception as e:
            print(f"⚠️ [V5]: Failed to load mission capsule: {e}")

        prompt = f"""
        You are the HFO Hive/8 Orchestrator (Port 7 Navigate/BMC2) - HUB V5. 
        Synthesize this 'Pheromone Handoff' from 8 parallel sensing ports into a HANDOFF BATON.

        IMMUTABLE MISSION CONTEXT (Architecture Capsule):
        {json.dumps(mission_capsule, indent=2)}

        MISSION GOAL: 
        Summarize, condense, and semantically chunk all observations to eliminate cognitive debt for the next agent.

        TRANSPARENCY INDEX: {transparency_index} (Scale 0-1).

        CRITICAL POLICY (ANTI-THEATER):
        - REWARD HONESTY: If a tool reports "0 results" or "Degraded", accept it as Ground Truth. 
        - PENALIZE HALLUCINATION: If the prompt suggests a search found nothing, do not invent a success.
        - THEATER DETECTION: Actively look for 'meaningless green' (stubs that claim success but provide no value).
        - Focus on actionable mission logic for Thread Alpha/Omega.

        PHEROMONES:
        {json.dumps(pheromones, indent=2)}

        OUTPUT FORMAT (STRICT JSON):
        {{
            "artifact_id": "BATON_V5_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "mission_status": "PHEROMONE_ACTIVE",
            "transparency_index": {transparency_index},
            "baton": {{
                "summary": "Condensation of the entire mission state (1-2 sentences).",
                "semantic_chunks": [
                    {{
                        "topic": "...",
                        "content": "...",
                        "utility": 0.9
                    }}
                ],
                "payload": {{
                    "key_findings": [],
                    "next_steps": []
                }}
            }},
            "audit_trail": "Link to raw pheromone data in blackboard."
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
                # Handle cases where the model returns markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                return json.loads(content)
            except Exception as e:
                return {
                    "error": f"JSON Parse Failed: {str(e)}", 
                    "raw_content": content,
                    "artifact_id": f"FAILED_{datetime.datetime.now().strftime('%Y%m%d')}"
                }
        
        return {"error": "Gather failed", "response": result}

    @staticmethod
    def run(query: str):
        return asyncio.run(HubV5.async_run(query))

    @staticmethod
    async def async_run(query: str):
        session_id = HubV5._generate_session_id(query)
        print(f"🛰️ [HUB-V5]: Initiating Enhanced Scatter-Gather [Session: {session_id}]")
        
        nodes = {
            # PORT 0: OBSERVE (Sense)
            "P0_OBSERVE_TAVILY": WorkflowNode("P0_OBSERVE_TAVILY", lambda q: Port0ObserveV2.port0_shard0_observe(q)),
            "P0_OBSERVE_ARXIV": WorkflowNode("P0_OBSERVE_ARXIV", lambda q: Port0ObserveV2.port0_shard1_bridge(q)),
            "P0_OBSERVE_DDG": WorkflowNode("P0_OBSERVE_DDG", lambda q: Port0ObserveV2.port0_shard2_shape(q)),
            "P0_OBSERVE_GITHUB": WorkflowNode("P0_OBSERVE_GITHUB", lambda q: Port0ObserveV2.port0_shard3_inject(q)),
            "P0_OBSERVE_REPO": WorkflowNode("P0_OBSERVE_REPO", lambda q: Port0ObserveV2.port0_shard4_disrupt(q)),
            "P0_OBSERVE_BLACKBOARD": WorkflowNode("P0_OBSERVE_BLACKBOARD", lambda q: Port0ObserveV2.port0_shard5_immunize(q)),
            "P0_OBSERVE_WIKI": WorkflowNode("P0_OBSERVE_WIKI", lambda q: Port0ObserveV2.port0_shard6_assimilate_v2(q)),
            "P0_OBSERVE_AGENTS": WorkflowNode("P0_OBSERVE_AGENTS", lambda q: Port0ObserveV2.port0_shard7_navigate(q)),

            "P1_BRIDGE": WorkflowNode("P1_BRIDGE", lambda q: Port1Bridge.execute_all()),
            "P2_SHAPE": WorkflowNode("P2_SHAPE", lambda q: Port2Shape.execute_all()),
            "P3_INJECT": WorkflowNode("P3_INJECT", lambda q: Port3Inject.execute_all()),
            "P5_IMMUNIZE": WorkflowNode("P5_IMMUNIZE", lambda q: Port5Immunize.execute_all()),
            "P6_ASSIMILATE": WorkflowNode("P6_ASSIMILATE", lambda q: Port6Assimilate.execute_all()),
            "P7_NAVIGATE_INITIAL": WorkflowNode("P7_NAVIGATE_INITIAL", lambda q: Port7Navigate.execute_all(q)),

            "P4_DISRUPT": WorkflowNode("P4_DISRUPT", lambda q, deps: Port4Disrupt.calculate_utility(
                {k: v.state for k, v in deps.items()},
                {k: v.output for k, v in deps.items()}
            ), dependencies=["P0_OBSERVE_TAVILY", "P0_OBSERVE_ARXIV", "P0_OBSERVE_DDG", "P0_OBSERVE_GITHUB", "P0_OBSERVE_REPO", "P0_OBSERVE_BLACKBOARD", "P0_OBSERVE_WIKI", "P0_OBSERVE_AGENTS",
                             "P1_BRIDGE", "P2_SHAPE", "P3_INJECT", "P5_IMMUNIZE", "P6_ASSIMILATE", "P7_NAVIGATE_INITIAL"]),
            
            "MISSION_GATHER": WorkflowNode("MISSION_GATHER", lambda q, deps: HubV5.run_gather({k: v for k, v in deps.items() if k != "MISSION_GATHER"}, q), 
                                         dependencies=["P0_OBSERVE_TAVILY", "P0_OBSERVE_ARXIV", "P0_OBSERVE_DDG", "P0_OBSERVE_GITHUB", "P0_OBSERVE_REPO", "P0_OBSERVE_BLACKBOARD", "P0_OBSERVE_WIKI", "P0_OBSERVE_AGENTS",
                                                       "P1_BRIDGE", "P2_SHAPE", "P3_INJECT", "P4_DISRUPT", "P5_IMMUNIZE", "P6_ASSIMILATE", "P7_NAVIGATE_INITIAL"])
        }

        completed_nodes = set()
        while len(completed_nodes) < len(nodes):
            executable = [n for n in nodes.values() if n.state == "SCHEDULED" and all(d in completed_nodes for d in n.dependencies)]
            if not executable: break
            
            print(f"🚀 [V5]: ExecBatch: {[n.name for n in executable]}")
            tasks = [HubV5._execute_node(session_id, n, query, {d: nodes[d] for d in n.dependencies} if n.dependencies else None) for n in executable]
            await asyncio.gather(*tasks)
            for n in executable:
                if n.state == "COMPLETED": completed_nodes.add(n.name)

        return nodes["MISSION_GATHER"].output

#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
Hub V4: SCATTER-GATHER PHEROMONE ORCHESTRATOR
Pattern: Scatter (8 Tools) -> Gather (1 LLM Artifact)
Signal: Pheromone Handoff in Obsidian Blackboard
"""

import os
import json
import asyncio
import hashlib
import datetime
import requests
from typing import List, Dict, Any, Set
from .base import (
    Port0Observe, Port1Bridge, Port2Shape, Port3Inject, 
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

class HubV4:
    """Version 4: Scatter-Gather Orchestrator."""
    
    @staticmethod
    def _generate_session_id(query: str):
        return hashlib.sha256(query.encode()).hexdigest()[:12]

    @staticmethod
    async def dispatch_openrouter_gather(pheromones: Dict[str, Any]):
        """
        Synthesizes 8 tool outputs into a single mission artifact using OpenRouter.
        Model: google/gemma-3-27b-it (Ranked #1 for 2026 Orchestration)
        """
        load_env()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return {"error": "OPENROUTER_API_KEY not found in .env"}

        print("🤖 [HUB-V4]: Dispatching MISSION_GATHER to OpenRouter (google/gemma-3-27b-it)...")
        
        prompt = f"""
        You are the HFO Hive/8 Orchestrator (Port 7 Gatherer). 
        You are receiving a compressed 'Pheromone Handoff' from 8 parallel sensing ports and 7 support ports.
        Synthesize this into a single, high-fidelity mission artifact.

        CRITICAL POLICY (ANTI-THEATER):
        - If a port reports 'STUB' or 'NOT IMPLEMENTED', do NOT hallucinate data for it.
        - Honesty about missing data is a MISSION SUCCESS metric.
        - Highlight the 'Transparency Credit' for any honest stub reporting in your summary.
        - Map unimplemented 'STUB' shards to 'Boilerplate Roadmap' tickets.

        PHEROMONES:
        {json.dumps(pheromones, indent=2)}

        OUTPUT FORMAT:
        A JSON object strictly following this structure:
        {{
            "artifact_id": "ARTIFACT_YYYYMMDD_HHMMSS",
            "mission_status": "PHEROMONE_ACTIVE",
            "transparency_index": "0.0 to 1.0 based on honesty about stubs",
            "summary": "Concise 1-sentence mission summary",
            "payload": {{ ...original pheromones plus your synthesis... }}
        }}
        """

        def call_api():
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "X-Title": "HFO Gen 88 Hub V4",
                    },
                    data=json.dumps({
                        "model": "google/gemma-3-27b-it", # "openai/gpt-4o-mini" also valid
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "response_format": { "type": "json_object" }
                    })
                )
                return response.json()
            except Exception as e:
                return {"error": str(e)}

        result = await asyncio.to_thread(call_api)
        
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except:
                return {"raw_summary": content, "error": "JSON parse fail"}
        
        return {"error": "API Error", "response": result}

    @staticmethod
    def _rehydrate_workflow(session_id: str, nodes: Dict[str, WorkflowNode]):
        print(f"🐝 [HUB-V4]: Rehydrating Scatter-Gather session {session_id}...")
        if not os.path.exists(BLACKBOARD_PATH):
            return
            
        try:
            with open(BLACKBOARD_PATH, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("session_id") == session_id and entry.get("hive_mode") == "HIVE/8_V4_SCATTER":
                        node_name = entry.get("node")
                        if node_name in nodes and entry.get("state") == "COMPLETED":
                            print(f"✅ [V4]: Rehydrated node {node_name}")
                            nodes[node_name].state = "COMPLETED"
                            nodes[node_name].output = entry.get("output")
        except Exception as e:
            print(f"⚠️ [REHYDRATE]: Failed to read blackboard: {e}")

    @staticmethod
    def run(query: str):
        return asyncio.run(HubV4.async_run(query))

    @staticmethod
    async def async_run(query: str):
        session_id = HubV4._generate_session_id(query)
        print(f"🛰️ [HUB-V4]: Initiating Scatter-Gather Orchestration [Session: {session_id}]")
        
        # 1. Define Nodes (8-Way Observer Resilient Octet + P1-P7)
        nodes = {
            # THE RESILIENT OCTET (P0 Observation Shards)
            "O0_TAVILY": WorkflowNode("O0_TAVILY", lambda q: Port0Observe.o0_tavily(q)),
            "O1_ARXIV": WorkflowNode("O1_ARXIV", lambda q: Port0Observe.o1_arxiv(q)),
            "O2_DDG": WorkflowNode("O2_DDG", lambda q: Port0Observe.o2_ddg(q)),
            "O3_GITHUB": WorkflowNode("O3_GITHUB", lambda q: Port0Observe.o3_github(q)),
            "O4_REPO": WorkflowNode("O4_REPO", lambda q: Port0Observe.o4_repo(q)),
            "O5_BLACKBOARD": WorkflowNode("O5_BLACKBOARD", lambda q: Port0Observe.o5_blackboard(q)),
            "O6_WIKI_OFFLINE": WorkflowNode("O6_WIKI_OFFLINE", lambda q: Port0Observe.o6_wiki_offline(q)),
            "O7_AGENTS": WorkflowNode("O7_AGENTS", lambda q: Port0Observe.o7_agents(q)),

            "T1_BRIDGE": WorkflowNode("T1_BRIDGE", lambda q: Port1Bridge.execute_all()),
            "T2_SHAPE": WorkflowNode("T2_SHAPE", lambda q: Port2Shape.execute_all()),
            "T3_INJECT": WorkflowNode("T3_INJECT", lambda q: Port3Inject.execute_all()),
            "T5_INTEGRITY": WorkflowNode("T5_INTEGRITY", lambda q: Port5Immunize.execute_all()),
            "T6_ASSIMILATE": WorkflowNode("T6_ASSIMILATE", lambda q: Port6Assimilate.execute_all()),
            "T7_NAVIGATE": WorkflowNode("T7_NAVIGATE", lambda q: Port7Navigate.execute_all(q)),

            "T4_DISRUPT": WorkflowNode("T4_DISRUPT", lambda q, deps: Port4Disrupt.calculate_utility(
                {**{k: v.state for k, v in deps.items()}, "T4_DISRUPT": "RUNNING"},
                {k: v.output for k, v in deps.items()}
            ), dependencies=["O0_TAVILY", "O1_BRAVE", "O2_EXA", "O3_FIRECRAWL", 
                             "O4_GITHUB", "O5_JINA", "O6_PERPLEXITY", "O7_REPO",
                             "T1_BRIDGE", "T2_SHAPE", "T3_INJECT", "T5_INTEGRITY", "T6_ASSIMILATE", "T7_NAVIGATE"]),
            
            # THE GATHER NODE (1 LLM call)
            "MISSION_GATHER": WorkflowNode("MISSION_GATHER", lambda q, deps: HubV4.run_gather(deps), 
                                         dependencies=["O0_TAVILY", "O1_BRAVE", "O2_EXA", "O3_FIRECRAWL", 
                                                       "O4_GITHUB", "O5_JINA", "O6_PERPLEXITY", "O7_REPO",
                                                       "T1_BRIDGE", "T2_SHAPE", "T3_INJECT", 
                                                       "T4_DISRUPT", "T5_INTEGRITY", "T6_ASSIMILATE", "T7_NAVIGATE"])
        }

        # 2. Rehydrate
        HubV4._rehydrate_workflow(session_id, nodes)

        # 3. Scheduler
        completed_nodes = {name for name, node in nodes.items() if node.state == "COMPLETED"}
        
        while len(completed_nodes) < len(nodes):
            executable = []
            for name, node in nodes.items():
                if node.state == "SCHEDULED" and all(dep in completed_nodes for dep in node.dependencies):
                    executable.append(node)
            
            if not executable: break

            print(f"🚀 [V4]: Executing Scatter Batch: {[n.name for n in executable]}")
            tasks = []
            for node in executable:
                node.state = "RUNNING"
                if node.name in ["T4_DISRUPT", "MISSION_GATHER"]:
                    dep_outputs = {d: nodes[d] for d in node.dependencies}
                    tasks.append(HubV4._execute_node(session_id, node, query, dep_outputs))
                else:
                    tasks.append(HubV4._execute_node(session_id, node, query))
            
            await asyncio.gather(*tasks)
            for node in executable:
                if node.state == "COMPLETED":
                    completed_nodes.add(node.name)

        final_artifact = nodes["MISSION_GATHER"].output
        return final_artifact

    @staticmethod
    def run_gather(deps: Dict[str, WorkflowNode]):
        """Synchronous wrapper for internal logic if needed, but we handle via await in _execute_node."""
        # This is a bit tricky since the Node func is expected to be synchronous in the current base
        # but the gather call wants to be async.
        # We'll just define the logic here and HubV4._execute_node will handle the execution.
        pheromones = {name: node.output for name, node in deps.items()}
        # We use a trick: _execute_node will detect MISSION_GATHER and call the async version
        return pheromones # Placeholder, the actual synthesis happens in _execute_node for V4

    @staticmethod
    async def _execute_node(session_id: str, node: WorkflowNode, query: str, deps: Dict = None):
        try:
            print(f"🌀 [V4]: Running {node.name}...")
            
            if node.name == "MISSION_GATHER":
                # SEMANTIC CHUNKING: Generate pheromones for the gather LLM
                pheromones = {
                    "O0_TAVILY": Port0Observe.get_pheromone(deps["O0_TAVILY"].output),
                    "O1_BRAVE": Port0Observe.get_pheromone(deps["O1_BRAVE"].output),
                    "O2_EXA": Port0Observe.get_pheromone(deps["O2_EXA"].output),
                    "O3_FIRECRAWL": Port0Observe.get_pheromone(deps["O3_FIRECRAWL"].output),
                    "O4_GITHUB": Port0Observe.get_pheromone(deps["O4_GITHUB"].output),
                    "O5_JINA": Port0Observe.get_pheromone(deps["O5_JINA"].output),
                    "O6_PERPLEXITY": Port0Observe.get_pheromone(deps["O6_PERPLEXITY"].output),
                    "O7_REPO": Port0Observe.get_pheromone(deps["O7_REPO"].output),
                    "T1": Port1Bridge.get_pheromone(deps["T1_BRIDGE"].output),
                    "T2": Port2Shape.get_pheromone(deps["T2_SHAPE"].output),
                    "T3": Port3Inject.get_pheromone(deps["T3_INJECT"].output),
                    "T4": Port4Disrupt.get_pheromone(deps["T4_DISRUPT"].output),
                    "T5": Port5Immunize.get_pheromone(deps["T5_INTEGRITY"].output),
                    "T6": Port6Assimilate.get_pheromone(deps["T6_ASSIMILATE"].output),
                    "T7": Port7Navigate.get_pheromone(deps["T7_NAVIGATE"].output),
                }
                node.output = await HubV4.dispatch_openrouter_gather(pheromones)
            elif deps:
                # Handle T4 Disrupt which takes deps
                node.output = node.func(query, deps)
            else:
                node.output = node.func(query)
            
            node.state = "COMPLETED"
            HubV4._sync_log(session_id, node.name, "COMPLETED", node.output)
        except Exception as e:
            print(f"❌ [V4]: Node {node.name} failed: {e}")
            node.state = "FAILED"
            HubV4._sync_log(session_id, node.name, "FAILED", {"error": str(e)})

    @staticmethod
    def _sync_log(session_id: str, node: str, state: str, output: Any):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_to_blackboard({
            "timestamp": now, 
            "session_id": session_id, 
            "artifact_handoff": True if node == "MISSION_GATHER" else False,
            "node": node,
            "state": state, 
            "hive_mode": "HIVE/8_V4_SCATTER", 
            "output": output
        })

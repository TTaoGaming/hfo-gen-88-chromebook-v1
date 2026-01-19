# Medallion: Bronze | Mutation: 0% | HIVE: V

# 🧭 HFO Mission Briefing: Pareto Frontier Evaluation Harness

**Date**: January 11, 2026
**Medallion**: Bronze | **Mission**: Thread Alpha (Bootstrapping)
**Author**: HFO-Hive8 (Port 7 Sovereign)

## 🏗️ Executive Summary

To scale the **HFO Orchestration Hub** to "Power of Eight" swarms without token bankruptcy, we must transition from high-cost models (Gemini 1.5 Pro, Claude 3.5 Sonnet) to a **Map-Elites Archive** of ultra-cheap, mission-fit models. This report defines the architecture for an **Agentic Eval Harness** designed to evaluate the Pareto Frontier of open-source and low-cost provider models.

---

## 🗺️ 1. The Map-Elites Archive for HFO

Instead of a single "best" model, HFO requires a **Quality-Diversity (QD)** archive that maps models to specific niches in the 8-port architecture.

### **Behavioral Descriptors (Axes)**

1. **Reasoning Depth (X-Axis)**: Score on logic/coding benchmarks (e.g., LiveCodeBench, GPQA).
2. **Latency / Rate Limit Ceiling (Y-Axis)**: Tokens per second vs. Request Per Minute (RPM).
3. **Tool-Use Precision (Z-Axis)**: Zod 6.0 schema adherence and JSON reliability.

### **Fitness Function**

* **Mission Fitness Score (MFS)**: `(SuccessRate * 0.6) + (1/TokenCost * 0.3) + (1/Latency * 0.1)`.

### **HFO Niches**

| Port Role | Model Category | Target Elite |
| :--- | :--- | :--- |
| **P0 SENSE** | Fast/Transactional | **Llama-4-8B-Instruct** (Groq) |
| **P1 FUSE** | Schema Rigid | **Qwen-3-7B-Coder** |
| **P7 NAVIGATE** | Multi-step Reasoning | **Gemma-3-27B-IT** |
| **P5 DEFEND** | Zero-Trust Auditor | **DeepSeek-V3.5** |

---

## 📈 2. Jan 2026 Pareto Frontier (Ultra-Cheap Category)

Current cost/performance leaders on OpenRouter/Groq (<$0.50 per 1M tokens):

1. **Gemma 3 (27B)**: The "Orchestration King." Exceptional logic-to-cost ratio. Ideal for the Gather/Synthesis phase (Diamond 2).
2. **Llama 4 (8B)**: The "Atomic Reflex." Highly optimized for sub-100ms tool calls. Best for the Scatter/Observe phase (Diamond 1).
3. **DeepSeek V3.5**: The "Coding Apex." Outperforms many 70B+ models in recursive logic and BFT Quorum audits.
4. **Qwen 3 (7B Coder)**: The "Structure Specialist." Absolute reliability in generating valid JSON and strictly adhering to Zod 6.0 contracts.

---

## 🛠️ 3. Proposed Eval Harness: "The Forensic Gauntlet"

To eliminate **AI Theater** (models claiming success while returning stubs), the harness must integrate with the **P5 Sentinel**.

### **Recommended Frameworks**

* **Inspect (UK ASI)**: Used for the primary execution loop. It supports "sandboxed" tool-use evaluation.
* **DSPy (Prompter Optimization)**: For the "Scatter" phase. We don't just test the model; we test the *Model + Optimized Prompt* combination.
* **MAE-Bench (Multi-Agent Eval)**: Evaluates the "Convergence Score" specifically for the HFO 8-1-8-1 BFT pattern.

### **Double Diamond Evaluation Strategy (8-1-8-1)**

1. **Scatter (Phase 1)**: Parallel evaluation of all 8 sharding logic paths.
2. **BFT Audit (Phase 2)**: Test the ability of the synthesizer (e.g., Gemma 3) to identify and reject "Byzantine" output (hallucinated data) injected into the shards by the harness.

---

## 🛰️ 4. Immediate Recommendations

1. **Initialize `hfo_evals/`**: A new directory for `inspect-ai` test suites.
2. **BFT Sensitivity Test**: Run the current `hub_v7.py` against a dataset of "Known Faulty Shards" to see if the **BFT Quorum Audit** correctly flags them.
3. **Rate Limit Managed Pools**: Implement a "Pulse Queue" in Port 7 to handle thousands of pulses without triggering OpenRouter's 429 breakers.

---
*Spider Sovereign (Port 7) | Pareto Frontier Secured | Phoenix Project V7.1*

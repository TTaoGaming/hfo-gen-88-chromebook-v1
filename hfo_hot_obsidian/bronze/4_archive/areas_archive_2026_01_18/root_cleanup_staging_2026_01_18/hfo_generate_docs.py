# Medallion: Bronze | Mutation: 0% | HIVE: V
import duckdb
import os
import json
from datetime import datetime

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
OUTPUT_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/MISSION_CONTROL"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_executive_summary(conn):
    print("📝 Generating Executive Summary...")
    stats = conn.execute("""
        SELECT 
            count(*), 
            min(modified_at), 
            max(modified_at), 
            sum(case when score > 20 then 1 else 0 end)
        FROM file_system
    """).fetchone()
    
    # Top Concepts based on score
    top_files = conn.execute("""
        SELECT path, score, modified_at 
        FROM file_system 
        ORDER BY score DESC, modified_at DESC 
        LIMIT 10
    """).fetchall()

    md_content = f"""# 🛰️ Mission Control: Executive Summary
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 Hive Intelligence Status
- **Total Files Indexed**: {stats[0]:,}
- **Timeline Coverage**: {stats[1].strftime('%Y-%m-%d')} to {stats[2].strftime('%Y-%m-%d')}
- **High-Density Nodes (Score > 20)**: {stats[3]}

## 💎 Logic Survivors & Priority Anchors
| Score | Path | Last Modified |
|-------|------|---------------|
"""
    for f in top_files:
        filename = os.path.basename(f[0])
        md_content += f"| {f[1]} | {filename} | {f[2].strftime('%Y-%m-%d')} |\n"
    
    with open(f"{OUTPUT_DIR}/EXECUTIVE_SUMMARY.md", "w") as f:
        f.write(md_content)

def generate_mermaid_timeline(conn):
    print("🧜 Generating Mermaid Timeline...")
    # Group file counts by week to show evolution spikes
    timeline = conn.execute("""
        SELECT 
            strftime(modified_at, '%Y-%W') as week,
            count(*) as count
        FROM file_system
        GROUP BY 1 ORDER BY 1
    """).fetchall()

    mermaid = "## 📅 Evolution Intensity (Weekly)\n\n```mermaid\ngraph LR\n"
    prev_week = None
    for row in timeline:
        week_label = f"Week_{row[0].replace('-', '_')}"
        mermaid += f"    {week_label}[{row[0]}: {row[1]} files]\n"
        if prev_week:
            mermaid += f"    {prev_week} --> {week_label}\n"
        prev_week = week_label
    mermaid += "```\n"
    
    with open(f"{OUTPUT_DIR}/TIMELINE_FLOW.md", "w") as f:
        f.write("# ⏳ Project Evolution Timeline\n" + mermaid)

def generate_force_graph_json(conn):
    print("🕸️ Generating Force Graph Data (Concept Links)...")
    # For a visualization tool, we output nodes (files) and edges (shared hashes)
    # We limit to high-score files to avoid cluttering 130k nodes
    nodes_data = conn.execute("""
        SELECT fs.path, fs.hash, fs.score, b.size
        FROM file_system fs
        JOIN blobs b ON fs.hash = b.hash
        WHERE fs.score > 15
        LIMIT 200
    """).fetchall()

    nodes = []
    links = []
    hash_map = {}

    for i, row in enumerate(nodes_data):
        node_id = f"node_{i}"
        nodes.append({
            "id": node_id,
            "name": os.path.basename(row[0]),
            "group": 1 if "active" in row[0] else 2,
            "score": row[2]
        })
        
        # Link files that share the same hash
        h = row[1]
        if h in hash_map:
            links.append({"source": hash_map[h], "target": node_id, "type": "shared_logic"})
        hash_map[h] = node_id

    graph = {"nodes": nodes, "links": links}
    with open(f"{OUTPUT_DIR}/CONCEPT_GRAPH.json", "w") as f:
        json.dump(graph, f, indent=2)

def main():
    conn = duckdb.connect(DB_PATH)
    generate_executive_summary(conn)
    generate_mermaid_timeline(conn)
    generate_force_graph_json(conn)
    print(f"✅ Visualizations and Docs generated in {OUTPUT_DIR}")
    conn.close()

if __name__ == "__main__":
    main()

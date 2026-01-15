import duckdb
import os
import json
from datetime import datetime

DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_unified_v88.duckdb"
OUTPUT_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/HIVE_DASHBOARD.html"

def generate_dashboard():
    conn = duckdb.connect(DB_PATH)
    
    # 1. Stats
    stats = conn.execute("SELECT count(*), count(DISTINCT hash) FROM file_system").fetchone()
    score_stats = conn.execute("SELECT count(*) FROM file_system WHERE score > 20").fetchone()
    
    # 2. Timeline Data
    timeline_data = conn.execute("""
        SELECT strftime(modified_at, '%Y-%m-%d') as day, count(*) 
        FROM file_system 
        GROUP BY 1 ORDER BY 1
    """).fetchall()
    days = [r[0] for r in timeline_data]
    counts = [r[1] for r in timeline_data]

    # 3. Top Survivors (Logic Survivors - High Density)
    survivors = conn.execute("""
        SELECT 
            fs.path, 
            fs.score, 
            b.size,
            fs.modified_at,
            fs.hash
        FROM file_system fs
        JOIN blobs b ON fs.hash = b.hash
        WHERE b.size > 0
        ORDER BY fs.score DESC, fs.modified_at DESC
        LIMIT 500
    """).fetchall()

    survivor_json = []
    for s in survivors:
        survivor_json.append({
            "path": s[0],
            "name": os.path.basename(s[0]),
            "score": s[1],
            "size": f"{s[2]/1024:.1f} KB",
            "date": s[3].strftime('%Y-%m-%d %H:%M'),
            "hash": s[4][:12]
        })

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HFO Hive Dashboard - Gen88 Mission Control</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #1a202c; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #4a5568; border-radius: 10px; }}
    </style>
</head>
<body class="bg-gray-900 text-gray-100 font-sans">
    <div class="container mx-auto p-6">
        <header class="flex justify-between items-center mb-10 border-b border-gray-700 pb-6">
            <div>
                <h1 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
                    HIVE DATA ARCHIVE
                </h1>
                <p class="text-gray-400">Mission Thread: Omega Gen4 V26 | Status: Backfilling...</p>
            </div>
            <div class="text-right">
                <div class="text-sm text-gray-500">Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div class="text-cyan-400 font-mono text-xl">{stats[0]:,} Files Indexed</div>
            </div>
        </header>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                <div class="text-gray-400 text-sm uppercase">Deduplicated Blobs</div>
                <div class="text-3xl font-bold text-white">{stats[1]:,}</div>
                <div class="text-xs text-green-400 mt-2">Dedupe Ratio: {1 - (stats[1]/stats[0]):.1%}</div>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                <div class="text-gray-400 text-sm uppercase">High-Density Nodes</div>
                <div class="text-3xl font-bold text-cyan-400">{score_stats[0]}</div>
                <div class="text-xs text-gray-500 mt-2">Score > 20 Priority</div>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                <div class="text-gray-400 text-sm uppercase">Timeline Span</div>
                <div class="text-2xl font-bold text-white">{days[0] if days else 'N/A'}</div>
                <div class="text-xs text-gray-500 mt-2">Earliest record</div>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                <div class="text-gray-400 text-sm uppercase">Current Logic Front</div>
                <div class="text-2xl font-bold text-white">{days[-1] if days else 'N/A'}</div>
                <div class="text-xs text-gray-500 mt-2">Latest activity</div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
            <!-- Left: Search & Table -->
            <div class="lg:col-span-2 bg-gray-800 rounded-2xl border border-gray-700 p-6 shadow-xl">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold flex items-center">
                        <span class="mr-2">💎</span> Logic Survivors & Golden Records
                    </h2>
                    <input type="text" id="searchInput" placeholder="Search paths or concepts..." 
                           class="bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500 w-64">
                </div>
                
                <div class="overflow-x-auto custom-scrollbar h-[600px]">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 bg-gray-800 border-b border-gray-700">
                            <tr>
                                <th class="py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Score</th>
                                <th class="py-3 px-4 text-xs font-semibold text-gray-400 uppercase">File Name</th>
                                <th class="py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Last Modified</th>
                                <th class="py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Hash</th>
                            </tr>
                        </thead>
                        <tbody id="survivorTable">
                            <!-- JS Inject -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right: Chart & Legend -->
            <div class="space-y-10">
                <div class="bg-gray-800 rounded-2xl border border-gray-700 p-6 shadow-xl">
                    <h2 class="text-xl font-bold mb-4">📈 Activity Intensity</h2>
                    <canvas id="intensityChart" class="w-full"></canvas>
                </div>

                <div class="bg-gray-800 rounded-2xl border border-gray-700 p-6 shadow-xl">
                    <h2 class="text-xl font-bold mb-4">🧱 Priority Weighting</h2>
                    <ul class="space-y-4 text-sm">
                        <li class="flex justify-between">
                            <span class="text-gray-400">Grimoire / Galois</span>
                            <span class="text-cyan-400 font-bold">+10 pts</span>
                        </li>
                        <li class="flex justify-between">
                            <span class="text-gray-400">Quine / Gem / Seed</span>
                            <span class="text-blue-400 font-bold">+5 pts</span>
                        </li>
                        <li class="flex justify-between">
                            <span class="text-gray-400">Folder: /active/</span>
                            <span class="text-green-400 font-bold">+10 pts</span>
                        </li>
                        <li class="flex justify-between">
                            <span class="text-gray-400">Age Penalty</span>
                            <span class="text-red-400 font-bold">Variable Decay</span>
                        </li>
                    </ul>
                </div>

                <div class="bg-blue-900/20 rounded-2xl border border-blue-500/30 p-6">
                    <h3 class="text-blue-300 font-bold mb-2 uppercase text-xs tracking-widest">Gen88 Logic Frontier</h3>
                    <p class="text-sm text-blue-100 leading-relaxed">
                        Currently backfilling archives. High density nodes are surfaced here. Duplicate hashes across history indicate logic that has resisted AI degradation.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const survivorData = {json.dumps(survivor_json)};
        const chartDays = {json.dumps(days)};
        const chartCounts = {json.dumps(counts)};

        function renderTable(data) {{
            const table = document.getElementById('survivorTable');
            table.innerHTML = data.map(s => `
                <tr class="border-b border-gray-700 hover:bg-gray-700/50 transition-colors">
                    <td class="py-4 px-4">
                        <span class="px-2 py-1 rounded ${{s.score > 30 ? 'bg-cyan-900/50 text-cyan-300 border border-cyan-500/30' : 'bg-gray-900 text-gray-400'}} text-xs font-bold">
                            ${{s.score}}
                        </span>
                    </td>
                    <td class="py-4 px-4 overflow-hidden max-w-xs">
                        <div class="font-bold text-sm text-white truncate" title="${{s.path}}">${{s.name}}</div>
                        <div class="text-[10px] text-gray-500 truncate">${{s.path}}</div>
                    </td>
                    <td class="py-4 px-4 text-xs text-gray-400 font-mono">${{s.date}}</td>
                    <td class="py-4 px-4 text-[10px] text-gray-600 font-mono">${{s.hash}}...</td>
                </tr>
            `).join('');
        }}

        // Initial Render
        renderTable(survivorData);

        // Search Filter
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            const filtered = survivorData.filter(s => 
                s.path.toLowerCase().includes(term) || 
                s.name.toLowerCase().includes(term)
            );
            renderTable(filtered);
        }});

        // Chart.js
        const ctx = document.getElementById('intensityChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: chartDays,
                datasets: [{{
                    label: 'Files Modified',
                    data: chartCounts,
                    borderColor: '#22d3ee',
                    backgroundColor: 'rgba(34, 211, 238, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: '#2d3748' }}, ticks: {{ color: '#a0aec0' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#a0aec0', maxRotation: 45, minRotation: 45 }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
    """
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(html_template)
    
    conn.close()
    return OUTPUT_PATH

if __name__ == "__main__":
    path = generate_dashboard()
    print(f"✅ Dashboard generated at: {{path}}")

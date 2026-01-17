import os
import json
import time
from pathlib import Path

def get_file_metadata(file_path):
    stat = os.stat(file_path)
    return {
        "path": str(file_path),
        "name": file_path.name,
        "last_modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
        "mtime": stat.st_mtime,
        "size_bytes": stat.st_size
    }

def consolidate_threads():
    root = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
    alpha_files = []
    omega_files = []
    
    # Define patterns for Alpha and Omega
    # Alpha: mission_thread_alpha, alpha_, hfo_akka_mcp_refactor_alpha
    # Omega: mission_thread_omega, omega_, OMEGA_
    
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        
        # Skip hidden, venv, node_modules
        if any(part.startswith('.') for part in path.parts) or "node_modules" in path.parts or ".venv" in path.parts:
            continue

        lower_name = path.name.lower()
        full_path_str = str(path).lower()
        
        is_alpha = "alpha" in lower_name or "alpha" in full_path_str
        is_omega = "omega" in lower_name or "omega" in full_path_str
        
        if is_alpha:
            alpha_files.append(get_file_metadata(path))
        if is_omega:
            omega_files.append(get_file_metadata(path))

    # Sort by timestamp for timeline
    alpha_files.sort(key=lambda x: x["mtime"])
    omega_files.sort(key=lambda x: x["mtime"])

    with open("mission_thread_alpha_consolidation.json", "w") as f:
        json.dump({"thread": "Alpha", "count": len(alpha_files), "files": alpha_files}, f, indent=4)
        
    with open("mission_thread_omega_consolidation.json", "w") as f:
        json.dump({"thread": "Omega", "count": len(omega_files), "files": omega_files}, f, indent=4)

    print(f"Consolidated {len(alpha_files)} Alpha files and {len(omega_files)} Omega files.")

if __name__ == "__main__":
    consolidate_threads()

import json
import os
import time

# Medallion: Bronze | Mutation: 0% | HIVE: I

def get_file_data(path):
    try:
        if not os.path.exists(path):
            return None
        
        stat = os.stat(path)
        modified_at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(stat.st_mtime))
        
        with open(path, 'r') as f:
            content = f.read()
            
        return {
            "path": path,
            "modified_at": modified_at,
            "content": content
        }
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None

def main():
    index_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/pending_silver_promotion/mission_threads_ssot_index.json"
    output_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/pending_silver_promotion/"
    
    with open(index_path, 'r') as f:
        index = json.load(f)
        
    for thread_key in ["mission_thread_alpha", "mission_thread_omega"]:
        consolidated = []
        thread_data = index[thread_key]
        
        # Flatten all lists in the thread categories
        all_paths = []
        for category in thread_data:
            all_paths.extend(thread_data[category])
            
        for path in all_paths:
            full_path = os.path.join("/home/tommytai3/active/hfo_gen_88_chromebook_v_1", path)
            data = get_file_data(full_path)
            if data:
                consolidated.append(data)
                
        output_name = f"{thread_key}_consolidated.json"
        output_path = os.path.join(output_dir, output_name)
        
        with open(output_path, 'w') as f:
            json.dump(consolidated, f, indent=2)
            
        print(f"Stored {len(consolidated)} entries in {output_path}")

if __name__ == "__main__":
    main()

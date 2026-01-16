import os
import re

def immunize_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern for the legacy OpenFeature initialization
    legacy_pattern = r'if \(window\.OpenFeature\) \{\s+window\.OpenFeature\.setProvider\(HFOFeatureProvider\);\s+\}'
    
    # "Armored" replacement logic
    armored_replacement = """        // 🛡️ [HFO] Initialize OpenFeature (Local UMD Bridge)
        const OF_ROOT = window.OpenFeature || {};
        const api = OF_ROOT.OpenFeature || OF_ROOT.default || OF_ROOT;

        if (typeof api.setProvider === 'function') {
            api.setProvider(HFOFeatureProvider);
            console.log("🚀 [HFO] OpenFeature Hardened (Offline Ready)");
        } else {
            console.warn("⚠️ [HFO] OpenFeature API not found in expected UMD location.");
        }"""

    # Also handle the part where featureClient is initialized
    legacy_client_pattern = r'const featureClient = window\.OpenFeature \? window\.OpenFeature\.getClient\(\) : \{'
    armored_client_replacement = '        const featureClient = typeof api.getClient === \'function\' ? api.getClient() : {'

    new_content = re.sub(legacy_pattern, armored_replacement, content)
    new_content = re.sub(legacy_client_pattern, armored_client_replacement, new_content)

    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dirs = [
        "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4",
        "hfo_cold_obsidian/bronze/2_areas/mission_thread_omega_gen_4"
    ]
    
    modified_count = 0
    for base_dir in base_dirs:
        abs_base = os.path.join(os.getcwd(), base_dir)
        if not os.path.exists(abs_base):
            continue
            
        for root, _, files in os.walk(abs_base):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    if immunize_file(file_path):
                        print(f"✅ Immunized: {file}")
                        modified_count += 1
                        
    print(f"\nTotal files immunized: {modified_count}")

if __name__ == "__main__":
    main()

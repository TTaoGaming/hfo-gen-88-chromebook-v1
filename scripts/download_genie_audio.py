# Medallion: Bronze | Mutation: 0% | HIVE: I
import os
import requests
import json

BASE_URL = "https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus/"
DEST_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/assets/piano_genie/sgm_plus/"

def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return
    print(f"Downloading {url}...")
    r = requests.get(url)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        print(f"Failed to download {url}: {r.status_code}")

def main():
    # 1. Download soundfont.json
    download_file(BASE_URL + "soundfont.json", os.path.join(DEST_DIR, "soundfont.json"))
    
    # 2. Download acoustic_grand_piano instrument.json
    piano_dir = "acoustic_grand_piano/"
    download_file(BASE_URL + piano_dir + "instrument.json", os.path.join(DEST_DIR, piano_dir, "instrument.json"))
    
    # 3. Download samples (Usually 1 velocity is enough for a lite demo, or 100 which is what player uses)
    # Magenta SoundFontPlayer uses specific velocity mappings. 
    # Let's try to download p[21-108]_v[velocity].mp3
    # Based on instrument.json, valid velocities are [15, 31, 47, 63, 79, 95, 111, 127]
    # The Player class uses velocity 100 by default, which usually maps to the closest one (95 or 111).
    chosen_velocity = 79 # Common middle-ground
    
    for pitch in range(21, 109):
        filename = f"p{pitch}_v{chosen_velocity}.mp3"
        url = BASE_URL + piano_dir + filename
        path = os.path.join(DEST_DIR, piano_dir, filename)
        download_file(url, path)

if __name__ == "__main__":
    print(f"Starting download to {DEST_DIR}...")
    main()
    print("Download script finished.")

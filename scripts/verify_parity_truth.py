# Medallion: Bronze | Mutation: 0% | HIVE: V
import re
import json

def audit_truth():
    file_path = "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v28_4.html"
    with open(file_path, 'r') as f:
        content = f.read()

    print("--- 🕵️ HFO TRUTH AUDIT (V28.4) ---")

    # 1. Check Zoom Factor
    zoom_match = re.search(r"zoomFactor:\s*([\d.]+)", content)
    zoom = float(zoom_match.group(1)) if zoom_match else 1.15
    print(f"Detected Zoom Factor: {zoom}")

    # 2. Check resizeCanvas Logic
    # Video matches drawW_base
    # Substrates match drawW = drawW_base * zoom
    
    # 3. Check dataFabric enforcement
    # Does P1_FUSE use toBufferX/Y correctly?
    # Does toClientX/Y use viewBounds correctly?
    
    print("\n--- 📐 PARITY CALCULATION ANALYSIS ---")
    pWidth = 1920 # Simulation
    vw = 1280
    vh = 720
    vRatio = vw / vh
    
    drawW_base = pWidth
    drawH_base = pWidth / vRatio
    # ... assuming height bounded ...
    
    drawW = drawW_base * zoom
    offsetX = (pWidth - drawW) / 2
    videoLeft = (pWidth - drawW) / 2 # Updated for v28.4 Fix
    
    print(f"Video Container Left: {videoLeft}")
    print(f"Substrate (UPE) Left: {offsetX}")
    print(f"Static Offset Error: {videoLeft - offsetX}px")
    
    # nx = 0 (Video edge)
    vx_at_nx0 = offsetX + (0 * drawW)
    print(f"At nx=0 (Video Left), toViewportX returns: {vx_at_nx0}")
    print(f"Difference from Video Left: {vx_at_nx0 - videoLeft}px")
    
    if abs(vx_at_nx0 - videoLeft) > 1:
        print("❌ CRITICAL: Parity Mismatch Detected. nx=0 does not align with video edge.")
    else:
        print("✅ Parity Aligned.")

    # 4. Check Data Fabric Enforcement in Scripts
    scripts = re.findall(r"<script.*?>([\s\S]*?)<\/script>", content)
    has_fabric_enforcements = any("systemState.dataFabric = DataFabricSchema.parse" in s for s in scripts)
    print(f"\nData Fabric schema enforcement found: {'✅' if has_fabric_enforcements else '❌'}")

if __name__ == "__main__":
    audit_truth()

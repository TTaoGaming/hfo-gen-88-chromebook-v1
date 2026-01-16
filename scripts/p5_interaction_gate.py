#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import re
import os

def audit_interaction_conflicts(file_path):
    print(f"🧬 [P5-INTERACT]: Auditing Interaction Conflicts for {file_path}...")
    if not os.path.exists(file_path):
        print(f"❌ [P5-INTERACT]: File not found: {file_path}")
        return False

    with open(file_path, 'r') as f:
        content = f.read()

    errors = []

    # 1. Detect 'pointer-events: none' on critical overlays
    # Pattern: id="..." style="..." contains pointer-events: none
    # Especially for Excalidraw which we know needs injection
    overlay_none_matches = re.finditer(r'id=["\'](excalidraw[^"\']*overlay)["\'][^>]*style=["\'][^"\']*pointer-events:\s*none', content, re.IGNORECASE)
    for match in overlay_none_matches:
        overlay_id = match.group(1)
        # Check if Port 3 injection logic (elementFromPoint) exists in the same file
        if "elementFromPoint" in content:
            errors.append(f"CRITICAL CONFLICT: Overlay '{overlay_id}' has 'pointer-events: none', which blocks 'elementFromPoint' injection used in Port 3.")

    # 2. General check for elementFromPoint usage vs top-level fixed/absolute elements with pointer-events: none
    # If a file uses elementFromPoint but has a global-ish div/container that blocks events, it's a smell.
    if "elementFromPoint" in content:
        if "pointer-events: none" in content:
            # Look for large overlays (width: 100% AND height: 100%)
            large_overlays = re.finditer(r'<div[^>]*style=["\'][^"\']*(width:\s*100%|height:\s*100%|width:\s*100vw|height:\s*100vh)[^"\']*(position:\s*absolute|position:\s*fixed)[^"\']*pointer-events:\s*none', content, re.IGNORECASE)
            for m in large_overlays:
                div_tag = m.group(0)
                # Specific exclusions for known passthrough layers
                if 'babylon-juice-overlay' not in div_tag and 'overlay-canvas' not in div_tag and 'video-feed' not in div_tag:
                    # If it has an ID, report it
                    id_match = re.search(r'id=["\']([^"\']+)["\']', div_tag)
                    id_str = id_match.group(1) if id_match else "unnamed div"
                    errors.append(f"POTENTIAL CONFLICT: Overlay '{id_str}' has 'pointer-events: none'. Large 'none' layers block 'elementFromPoint' search for interactive targets behind them.")

    if errors:
        print(f"❌ [P5-INTERACT]: Found {len(errors)} interaction conflicts:")
        for err in errors:
            print(f"  - {err}")
        return False

    print(f"✅ [P5-INTERACT]: No critical interaction conflicts detected.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 p5_interaction_gate.py <file_path>")
        sys.exit(1)
    
    success = True
    for arg in sys.argv[1:]:
        if not audit_interaction_conflicts(arg):
            success = False
    
    if not success:
        sys.exit(1)
    sys.exit(0)

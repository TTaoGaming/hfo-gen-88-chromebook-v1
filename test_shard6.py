
import sys
import os

# Add the ports directory to path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports")

from versions.base import Port0ObserveV2

print("Testing P0 Shard 6 (DuckDB)...")
result = Port0ObserveV2.port0_shard6_assimilate_v2("Python programming language")
print(f"Result: {result}")

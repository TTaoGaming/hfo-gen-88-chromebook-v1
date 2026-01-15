import re
import sys

def audit_file(file_path):
    print(f"Auditing {file_path} for Schema Parity...")
    with open(file_path, 'r') as f:
        content = f.read()

    # Check for DataFabricSchema
    if "const DataFabricSchema = z.object({" not in content:
        print("❌ MISSING: DataFabricSchema definition.")
    else:
        print("✅ FOUND: DataFabricSchema.")

    # Check for multiple definitions of FusionSchema or DataFabricSchema
    fusion_defs = len(re.findall(r"const FusionSchema = z\.object\(", content))
    data_fabric_defs = len(re.findall(r"const DataFabricSchema = z\.object\(", content))

    if fusion_defs > 1:
        print(f"⚠️ WARNING: Multiple FusionSchema definitions found ({fusion_defs}).")
    if data_fabric_defs > 1:
        print(f"⚠️ WARNING: Multiple DataFabricSchema definitions found ({data_fabric_defs}).")

    # Check if landmarks are present in FusionSchema
    if "landmarks: z.array(z.object({ x: z.number(), y: z.number(), z: z.number() })).optional()" in content:
        print("✅ VERIFIED: landmarks included in FusionSchema contract.")
    else:
        print("❌ FAILED: landmarks missing or malformed in FusionSchema contract.")

    # Check for "Hacking": Search for local landmark mappings that bypass the scheme
    hacks = re.findall(r"landmarks:\s*lm\.map", content)
    if len(hacks) > 1:
        print(f"⚠️ WARNING: Potential hacking detected. Multiple landmark mappings found ({len(hacks)}).")

    print("Audit Complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 schema_audit.py <file_path>")
    else:
        audit_file(sys.argv[1])

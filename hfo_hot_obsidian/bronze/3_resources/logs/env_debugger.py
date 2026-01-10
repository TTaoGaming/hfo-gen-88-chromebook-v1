# Medallion: Bronze | Mutation: 0% | HIVE: I
import os
def load_env_manual():
    env_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.env"
    print(f"Checking path: {env_path}")
    if os.path.exists(env_path):
        print("Found .env file.")
        with open(env_path, "r") as f:
            lines = f.readlines()
            print(f"Read {len(lines)} lines.")
            for line in lines:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    print(f"Setting key: {key}")
                    os.environ[key] = val.strip('\"').strip("'")
    else:
        print(".env NOT FOUND at path.")

load_env_manual()
print(f"TAVILY_API_KEY in os.environ: {'TAVILY_API_KEY' in os.environ}")

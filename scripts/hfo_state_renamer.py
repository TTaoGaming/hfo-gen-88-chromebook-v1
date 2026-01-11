import re

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v44.html'

with open(filepath, 'r') as f:
    content = f.read()

# Mappings
mappings = [
    (r"'ARMING'", r"'PORT_0_READY_DWELL'"),
    (r"'ARMED'", r"'PORT_0_POINTER_READY'"),
    (r"'COMMITTING'", r"'PORT_7_COMMIT_PENDING'"),
    (r"'COMMITTED'", r"'PORT_7_POINTER_COMMITTED'"),
    (r"'RELEASING'", r"'PORT_7_RELEASE_PENDING'"),
    (r"state === 'ARMING'", r"state === 'PORT_0_READY_DWELL'"),
    (r"state === 'ARMED'", r"state === 'PORT_0_POINTER_READY'"),
    (r"state === 'COMMITTING'", r"state === 'PORT_7_COMMIT_PENDING'"),
    (r"state === 'COMMITTED'", r"state === 'PORT_7_POINTER_COMMITTED'"),
    (r"state === 'RELEASING'", r"state === 'PORT_7_RELEASE_PENDING'"),
    (r"this\.state === 'COMMITTED'", r"this.state === 'PORT_7_POINTER_COMMITTED'"),
]

for old, new in mappings:
    content = re.sub(old, new, content)

with open(filepath, 'w') as f:
    f.write(content)

print("Renaming complete.")

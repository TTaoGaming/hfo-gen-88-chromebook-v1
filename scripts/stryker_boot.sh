#!/bin/bash

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Resource-Aware Stryker Bootstrapper

# 1. Run Port 0 Hardware Sensor
HW_DATA=$(python3 /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe/port_0_hardware_sensor.py | grep -A 15 "{" | head -n 16)

# 2. Extract Suggested Concurrency
CONCURRENCY=$(echo "$HW_DATA" | grep "suggested_concurrency" | awk -F: '{print $2}' | tr -d ' ,')

if [ -z "$CONCURRENCY" ]; then
    CONCURRENCY=1
fi

echo "🚀 [HFO STRATEGY]: Running Stryker with concurrency: $CONCURRENCY"

# 3. Execute Stryker
npx stryker run --concurrency $CONCURRENCY "$@"

# monitor_node.py
# Copyright 2026 Kapbotics
# SPDX-License-Identifier: Apache-2.0

import sen

ownship_query = None
radar_query = None

# Track the last printed state to avoid spam
last_ownship_summary = None
last_radar_summary = None

def run():
    global ownship_query, radar_query
    
    # 1. Use the exact class names as required by SEN SQL documentation
    ownship_query = sen.api.open('SELECT * FROM tactical.bus WHERE name = "VIPER_1"')
    radar_query = sen.api.open('SELECT * FROM tactical.bus WHERE name = "RADAR_NODE"')        
    print("\n===================================================")
    print("[BUS MONITOR] Node initialized. Monitoring for bus changes...")
    print("====================================================\n")

def update():
    global ownship_query, radar_query, last_ownship_summary, last_radar_summary
    
    status_parts = []
    
    # 1. Always get the latest F-16 State
    if len(ownship_query) > 0:
        obj = ownship_query[0]
        status_parts.append(f"F-16 [Lat: {obj.lat:.4f}, Lon: {obj.lon:.4f}, Alt: {int(obj.altM)}m]")
        
    # 2. Always get the latest Radar State
    if len(radar_query) > 0:
        obj = radar_query[0]
        state = "DETECTED" if obj.isDetected else "LOST"
        status_parts.append(f"RADAR [Range: {int(obj.rangeM)}m, {state}]")       
            
    # 3. Use carriage return (\r) to overwrite the same line in the console
    if status_parts:
        output = f"[MONITOR][BUS UPDATE] {' | '.join(status_parts)}"
        # end="" prevents a new line; \r moves the cursor back to the start
        print(f"\r{output}", end="", flush=True)
        
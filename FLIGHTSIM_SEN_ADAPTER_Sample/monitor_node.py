import sen

ownship_query = None
radar_query = None

def run():
    global ownship_query, radar_query
    
    # 1. Use the exact class names as required by SEN SQL documentation
    ownship_query = sen.api.open('SELECT sim_interface.Ownship FROM tactical.bus')
    radar_query = sen.api.open('SELECT sim_interface.RadarReport FROM tactical.bus')
    
    print("\n=================================================")
    print("[MONITOR] Node initialized. Listening to tactical.bus...")
    print("=================================================\n")

def update():
    global ownship_query, radar_query
    
    status_parts = []
    
    # 2. Extract F-16 State
    if len(ownship_query) > 0:
        obj = ownship_query[0]
        status_parts.append(f"F-16 [Lat: {obj.lat:.4f}, Lon: {obj.lon:.4f}, Alt: {int(obj.altM)}m]")
        
    # 3. Extract Radar State
    if len(radar_query) > 0:
        obj = radar_query[0]
        state = "DETECTED" if obj.isDetected else "LOST"
        status_parts.append(f"RADAR [Range: {int(obj.rangeM)}m, {state}]")
        
    # 4. Standard print to ensure visibility in the SEN Kernel window
    if status_parts:
        print(f"[BUS] {' | '.join(status_parts)}", flush=True)

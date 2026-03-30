# se_node.py
# Copyright 2026 Kapbotics
# SPDX-License-Identifier: Apache-2.0

import sen

radar_report = None
ownship_query = None
tactical_bus = None 

def run():
    global radar_report, ownship_query, tactical_bus
    radar_report = sen.api.make("simulation_interface_package.RadarReportImpl", "RADAR_NODE")
    
    # Save to global variable to prevent garbage collection
    tactical_bus = sen.api.getBus("tactical.bus")
    tactical_bus.add(radar_report)
    
    # Query for the F-16 instance
    ownship_query = sen.api.open('SELECT * FROM tactical.bus WHERE name = "VIPER_1"')
    
    print("[T_SE_NODE] Initialized: Pure Local Dummy Mode")

def update():
    global radar_report, ownship_query
    
    if len(ownship_query) > 0:
        target = ownship_query[0]
        
        # Dummy Logic: Detect if target altitude is above 600m
        is_detected = target.altM > 600.0
        radar_report.setDetection(
            "DUMMY_SAM", 
            2000.0, 
            is_detected
        )

def stop():
    pass
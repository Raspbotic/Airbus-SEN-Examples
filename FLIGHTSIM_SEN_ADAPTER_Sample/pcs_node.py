# pcs_node.py
# Copyright 2026 Kapbotics
# SPDX-License-Identifier: Apache-2.0

import sen
import math

ownship = None
tactical_bus = None  # CRITICAL: Keep the bus alive
tick = 0

def run():
    global ownship, tactical_bus
    ownship = sen.api.make("simulation_interface_package.OwnshipImpl", "VIPER_1")
    
    # FIX: Save to global variable to prevent garbage collection
    tactical_bus = sen.api.getBus("tactical.bus")
    tactical_bus.add(ownship)
    
    print("\n[PCS_NODE] Initialized: Pure Local Dummy Mode")

def update():
    global ownship, tick
    tick += 1
    
    # Generate dummy flight data: Circular path around Munich
    radius = 0.02
    lat = 48.3418 + radius * math.cos(tick * 0.05)
    lon = 11.7639 + radius * math.sin(tick * 0.05)
    alt = 500.0 + (tick * 0.5)
    
    ownship.updateState(
        "VIPER_1", 
        float(lat), 
        float(lon), 
        float(alt), 
        float(tick % 360), # Heading
        0.0, # Pitch
        0.0  # Roll
    )

def stop():
    pass
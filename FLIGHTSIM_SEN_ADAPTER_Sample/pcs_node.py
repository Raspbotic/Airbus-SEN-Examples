# pcs_node.py
import sen
import socket
import json

ownship = None
udp_rx = None
radar_query = None
udp_tx = None

def run():
    global ownship, udp_rx, radar_query, udp_tx
    ownship = sen.api.make("simulation_interface_package.OwnshipImpl", "VIPER_1")
    sen.api.getBus("tactical.bus").add(ownship)
    
    # 1. NEW: Subscribe to radar data published by se_node
    radar_query = sen.api.open('SELECT sim_interface.RadarReport FROM tactical.bus')
   
    print("\n=================================================")
    print("[PCS_NODE] Initializing Full-Duplex Bridge...")
    
    try:
        # Receiver: F-16 -> SEN
        udp_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_rx.bind(("127.0.0.1", 5006))
        udp_rx.setblocking(False)
        
        # Transmitter: SEN -> F-16 Map
        udp_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print("[PCS_NODE] SUCCESS: UDP pipes initialized.", flush=True)
    except Exception as e:
        print(f"[PCS_NODE] FATAL ERROR: {e}", flush=True)
        
    print("=================================================\n")

def update():
    global ownship, udp_rx, radar_query, udp_tx
    
    # 2. PART A: Receive Telemetry (F-16 -> Bus)
    try:
        while True:
            data, _ = udp_rx.recvfrom(2048)
            msg = json.loads(data.decode())
            
            ownship.ownshipId = "VIPER_1"
            ownship.lat = float(msg['lat'])
            ownship.lon = float(msg['lon'])
            ownship.altM = float(msg['alt_m'])
            ownship.hdg = float(msg['heading_deg'])
            ownship.pitch = float(msg['pitch_deg'])
            ownship.roll = float(msg['roll_deg'])
    except (BlockingIOError, socket.error, KeyError, ValueError):
        pass

    # 3. PART B: Transmit Detections (Bus -> F-16 UI)
    if radar_query and len(radar_query) > 0:
        report = radar_query[0]
        payload = {
            "emitterId": report.emitterId,
            "rangeM": report.rangeM,
            "isDetected": report.isDetected
        }
        try:
            udp_tx.sendto(json.dumps(payload).encode(), ("127.0.0.1", 6006))
        except Exception:
            pass

def stop():
    global udp_rx, udp_tx
    for s in [udp_rx, udp_tx]:
        if s: s.close()
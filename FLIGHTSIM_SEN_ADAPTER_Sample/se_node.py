import sen
import socket
import json

radar_report = None
ownship_query = None
udp_sock = None

def run():
    global radar_report, ownship_query, udp_sock
    radar_report = sen.api.make("simulation_interface_package.RadarReportImpl", "RADAR_NODE")
    sen.api.getBus("tactical.bus").add(radar_report)
    
    print("\n=================================================")
    print("[SE_NODE] Initializing UDP bridge...")

    # SQL query syntax as per SEN STL definitions
    ownship_query = sen.api.open('SELECT sim_interface.Ownship FROM tactical.bus WHERE name = "VIPER_1"')
    
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(("127.0.0.1", 5007))
        udp_sock.setblocking(False)
        print("[SE_NODE] SUCCESS: Bound to UDP port 5007", flush=True)
    except Exception as e:
        print(f"[SE_NODE] FATAL ERROR: Could not bind 5007: {e}", flush=True)

    print("=================================================\n")

def update():
    global radar_report, ownship_query, udp_sock
    
    # DIAGNOSTIC: Prove if se_node even sees the F-16 on the bus
    if len(ownship_query) > 0:
        target = ownship_query[0]
        print(f"[SE BUS CHECK] Found Ownship: {target.ownshipId}", flush=True)
    
    if len(ownship_query) > 0:
        target = ownship_query[0]
        payload = {
            "id": target.ownshipId, 
            "lat": target.lat, 
            "lon": target.lon, 
            "alt": target.altM,
            "hdg": target.hdg
        }
        try:
            udp_sock.sendto(json.dumps(payload).encode(), ("127.0.0.1", 6007))
        except Exception:
            pass

    try:
        while True:
            data, _ = udp_sock.recvfrom(1024)
            msg = json.loads(data.decode())
            
            # DIRECT ASSIGNMENT (As per official documentation)
            radar_report.emitterId = str(msg['emitterId'])
            radar_report.rangeM = float(msg['rangeM'])
            radar_report.isDetected = bool(msg['isDetected'])
            
    except (BlockingIOError, socket.error, KeyError, ValueError):
        pass

def stop():
    global udp_sock
    if udp_sock is not None:
        try:
            udp_sock.close()
        except Exception:
            pass
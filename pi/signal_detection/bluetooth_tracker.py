# pi/signal_detection/bluetooth_tracker.py
from bluepy.btle import Scanner

def detect_bluetooth_signals():
    scanner = Scanner()
    devices = scanner.scan(10.0)
    signals = []
    for dev in devices:
        signals.append({
            "mac": dev.addr,
            "rssi": dev.rssi,
            # Add more details as needed
        })
    return signals

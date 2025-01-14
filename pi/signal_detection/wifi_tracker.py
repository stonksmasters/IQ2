# pi/signal_detection/wifi_tracker.py
import subprocess
import re

def detect_wifi_signals():
    result = subprocess.run(['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE)
    cells = result.stdout.decode().split('Cell ')
    signals = []
    for cell in cells[1:]:
        mac = re.search(r'Address: ([\w:]+)', cell).group(1)
        signal = re.search(r'Signal level=(-\d+) dBm', cell)
        rssi = int(signal.group(1)) if signal else None
        signals.append({
            "mac": mac,
            "rssi": rssi,
        })
    return signals

# pi/signal_detection/bluetooth_tracker.py

import asyncio
from bluepy.btle import Scanner

async def detect_bluetooth_signals():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, scan_bluetooth)

def scan_bluetooth():
    scanner = Scanner()
    devices = scanner.scan(10.0)  # Scan for 10 seconds

    # Process devices as needed
    signal_data = []
    for dev in devices:
        signal_data.append({
            'address': dev.addr,
            'rssi': dev.rssi,
            'services': [s.uuid for s in dev.getScanData()]
        })

    return signal_data

# pi/signal_detection/signal_detection.py

import asyncio
from bluetooth_tracker import detect_bluetooth_signals
from wifi_tracker import detect_wifi_signals

async def send_signals():
    while True:
        bluetooth_signals = await detect_bluetooth_signals()
        wifi_signals = await detect_wifi_signals()

        # Process and send signals as needed
        # For example, send to a remote server or update a shared resource
        print("Bluetooth Signals:", bluetooth_signals)
        print("WiFi Signals:", wifi_signals)

        await asyncio.sleep(5)  # Adjust the interval as needed

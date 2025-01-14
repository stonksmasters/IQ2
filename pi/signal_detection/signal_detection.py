# pi/signal_detection/signal_detection.py

import asyncio
import websockets
import json
from .bluetooth_tracker import detect_bluetooth_signals
from wifi_tracker import detect_wifi_signals
from flipper_zero_interface import detect_flipper_signals
from utils.config import SERVER_URI

async def send_signals():
    async with websockets.connect(SERVER_URI) as websocket:
        while True:
            bluetooth = detect_bluetooth_signals()
            wifi = detect_wifi_signals()
            flipper = detect_flipper_signals()
            all_signals = {
                "bluetooth": bluetooth,
                "wifi": wifi,
                "flipper": flipper,
            }
            await websocket.send(json.dumps(all_signals))
            await asyncio.sleep(0.1)  # Adjust the frequency as needed

if __name__ == "__main__":
    try:
        asyncio.run(send_signals())
    except KeyboardInterrupt:
        print("Signal detection stopped.")

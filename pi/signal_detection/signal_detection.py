# pi/signal_detection/signal_detection.py
import asyncio
import websockets
import json
from bluetooth_tracker import detect_bluetooth_signals
from wifi_tracker import detect_wifi_signals
from flipper_zero_interface import detect_flipper_signals

async def send_signals():
    uri = "ws://computer_ip:8765/signals"
    async with websockets.connect(uri) as websocket:
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
            await asyncio.sleep(0.1)  # Adjust frequency as needed

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_signals())

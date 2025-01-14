# computer/server/websocket_server.py
import asyncio
import websockets
import json

connected = set()

async def signals_handler(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            signal_data = json.loads(message)
            # Process signal data (e.g., triangulation)
            processed_data = process_signals(signal_data)
            # Broadcast to all connected frontend clients
            await broadcast(json.dumps(processed_data))
    finally:
        connected.remove(websocket)

async def broadcast(message):
    if connected:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([ws.send(message) for ws in connected])

start_server = websockets.serve(signals_handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

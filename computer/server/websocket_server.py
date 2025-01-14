# computer/server/websocket_server.py

import asyncio
import websockets
import json
from triangulation import process_signals
from utils.logger import setup_logger

logger = setup_logger('websocket_server', 'websocket_server.log')

connected_clients = set()

async def handle_client(websocket, path):
    logger.info(f"Client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            logger.info(f"Received signal data: {data}")
            processed_data = process_signals(data)
            # Broadcast processed data to all connected frontend clients
            await broadcast(json.dumps(processed_data))
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client disconnected: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

async def start_websocket_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    logger.info("WebSocket server started on port 8765")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        logger.info("WebSocket server stopped.")

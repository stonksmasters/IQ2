# computer/server/video_server.py

import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay
import websockets
import json
from utils.logger import setup_logger

logger = setup_logger('video_server', 'video_server.log')
relay = MediaRelay()
pcs = set()

async def signaling_handler(websocket, path):
    logger.info(f"Video client connected: {websocket.remote_address}")
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        logger.info(f"ICE connection state: {pc.iceConnectionState}")
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "offer":
                offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await pc.setRemoteDescription(offer)
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await websocket.send(json.dumps({
                    "type": pc.localDescription.type,
                    "sdp": pc.localDescription.sdp
                }))
    except websockets.exceptions.ConnectionClosed:
        logger.info("Video client disconnected.")
    finally:
        await pc.close()
        pcs.discard(pc)

async def start_video_server():
    server = await websockets.serve(signaling_handler, "0.0.0.0", 9000)
    logger.info("Video WebSocket server started on port 9000")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(start_video_server())
    except KeyboardInterrupt:
        logger.info("Video server stopped.")

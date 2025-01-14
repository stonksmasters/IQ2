# pi/camera_stream/stream.py

import asyncio
from aiortc import RTCPeerConnection, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaRelay
import cv2
import numpy as np

relay = MediaRelay()

class VideoTransformTrack(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()  # Initialize base class
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        # Here you can apply transformations to the frame if needed
        return frame

async def run(pc, signaling):
    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        async def on_message(message):
            print(f"Received message from client: {message}")
            # Implement HUD control commands here
            # For example, adjust which signals to track based on message

    # Assuming signaling is handled elsewhere
    await signaling.connect()

    # Add video track
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting ...")
            break
        # Convert the image to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert to aiortc VideoFrame
        video_frame = VideoStreamTrack.from_ndarray(frame, format="rgb24")
        await pc.addTrack(video_frame)
        await asyncio.sleep(0.03)  # Approx ~30fps

async def main():
    pc = RTCPeerConnection()
    await run(pc, None)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Video streaming stopped.")

# pi/camera_stream/stream.py

import asyncio
import cv2
from aiohttp import web

# Global variable to hold the latest frame
latest_frame = None

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

async def video_stream(request):
    global latest_frame

    async def stream():
        while True:
            if latest_frame is None:
                await asyncio.sleep(0.1)
                continue

            # Encode frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', latest_frame)
            if not ret:
                continue

            # Convert to bytes
            frame_bytes = jpeg.tobytes()

            # Yield multipart data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            await asyncio.sleep(0.03)  # Approx ~30fps

    return web.Response(body=stream(), content_type='multipart/x-mixed-replace; boundary=frame')

async def capture_frames():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            await asyncio.sleep(0.1)
            continue

        # Optional: Apply any frame transformations here
        # For example, convert to RGB
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        latest_frame = frame
        await asyncio.sleep(0.03)  # Approx ~30fps

async def init_app():
    app = web.Application()
    app.router.add_get('/video_feed', video_stream)
    return app

async def main():
    # Start frame capture
    frame_task = asyncio.create_task(capture_frames())

    # Initialize and run the web server
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()

    print("Video streaming server started at http://0.0.0.0:8000/video_feed")

    # Keep the main coroutine running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Video streaming stopped.")
    finally:
        cap.release()

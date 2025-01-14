# pi/main.py

import asyncio
from signal_detection.signal_detection import send_signals
from camera_stream.stream import main as video_stream_main

async def main():
    # Create tasks for different components
    send_signals_task = asyncio.create_task(send_signals())
    video_stream_task = asyncio.create_task(video_stream_main())

    # Run tasks concurrently
    await asyncio.gather(
        send_signals_task,
        video_stream_task
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped.")

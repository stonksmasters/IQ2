# pi/main.py

import asyncio
from camera_stream.stream import main as stream_main
from signal_detection.signal_detection import send_signals

async def main():
    await asyncio.gather(
        stream_main(),
        send_signals()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Main script stopped.")

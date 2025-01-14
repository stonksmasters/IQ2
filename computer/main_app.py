# computer/main_app.py

import asyncio
from server.websocket_server import start_websocket_server
from server.video_server import start_video_server

async def main():
    await asyncio.gather(
        start_websocket_server(),
        start_video_server(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Main application stopped.")
